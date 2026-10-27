import os
import re
import json
import logging
from .models import FAQ, ErrorCode, SupportTicket, Movie
from .mongo_db import save_chat_log

logger = logging.getLogger('myapp.ai')

def match_error_code(prompt):
    """Detects if prompt queries an HTTP or site-specific error code."""
    # Look for 3-digit numbers or site-specific codes like FLIX-402
    patterns = [
        r'\b(400|401|403|404|429|500|503)\b',
        r'\b(flix[-_]?402|stream[-_]?402|402)\b',
        r'\b(bad request|unauthorized|forbidden|not found|rate limit|too many requests|server error|service unavailable)\b'
    ]
    
    prompt_lower = prompt.lower()
    
    # Check direct code
    code_match = re.search(r'\b(400|401|403|404|429|500|503)\b', prompt)
    if code_match:
        code = code_match.group(1)
        err = ErrorCode.objects.filter(code=code).first()
        if err:
            return err

    if 'flix' in prompt_lower or 'site-specific' in prompt_lower or 'custom' in prompt_lower:
        err = ErrorCode.objects.filter(is_site_specific=True).first()
        if err:
            return err

    # Check textual keywords
    keyword_map = {
        'bad request': '400',
        'unauthorized': '401',
        'forbidden': '403',
        'not found': '404',
        'too many requests': '429',
        'rate limit': '429',
        'server error': '500',
        'internal error': '500',
        'service unavailable': '503',
        'offline': '503',
    }
    for kw, c in keyword_map.items():
        if kw in prompt_lower:
            err = ErrorCode.objects.filter(code=c).first()
            if err:
                return err

    return None

def match_faq(prompt):
    """Searches SQL FAQ database using keyword relevance matching."""
    prompt_words = set(re.findall(r'\w+', prompt.lower()))
    stop_words = {'what', 'is', 'how', 'do', 'i', 'can', 'the', 'a', 'an', 'to', 'in', 'for', 'of', 'and', 'my', 'please', 'tell', 'me'}
    keywords = prompt_words - stop_words

    if not keywords:
        return None

    faqs = FAQ.objects.filter(is_active=True)
    best_faq = None
    best_score = 0

    for faq in faqs:
        q_words = set(re.findall(r'\w+', faq.question.lower()))
        a_words = set(re.findall(r'\w+', faq.answer.lower()))
        
        # Calculate overlap score
        q_overlap = len(keywords & q_words) * 3  # Question match weighted 3x
        a_overlap = len(keywords & a_words) * 1
        score = q_overlap + a_overlap

        if score > best_score:
            best_score = score
            best_faq = faq

    # Threshold for a confident answer
    if best_score >= 3:
        return best_faq
    return None

def should_escalate_to_ticket(prompt):
    """Determines whether a question cannot be answered and requires ticket creation."""
    escalation_phrases = [
        'create ticket', 'raise ticket', 'support ticket', 'open ticket',
        'complaint', 'not working', 'broken', 'issue', 'human',
        'agent', 'customer care', 'refund', 'charged twice', 'billing problem',
        'bug', 'error', 'failed', 'cannot login', 'cannot watch', 'black screen'
    ]
    prompt_lower = prompt.lower()
    return any(p in prompt_lower for p in escalation_phrases)

def create_support_ticket_from_prompt(prompt, session_key='', error_code=''):
    """Creates a support ticket in SQL database when AI cannot resolve or user asks."""
    import random
    subject = prompt[:100] if len(prompt) > 10 else "User Support Request via AI Assistant"
    
    # Priority determination
    priority = "MEDIUM"
    if any(w in prompt.lower() for w in ['urgent', 'emergency', 'asap', 'broken', 'charged', 'refund']):
        priority = "HIGH"
    elif any(w in prompt.lower() for w in ['crash', 'down', 'critical', '500', '503']):
        priority = "URGENT"

    ticket = SupportTicket.objects.create(
        name="StreamFlix User",
        email="user@streamflix.local",
        subject=subject,
        description=prompt,
        error_code=error_code,
        priority=priority,
        created_by_ai=True
    )
    return ticket

def analyze_user_prompt(prompt, all_movies=None, session_id='guest_session'):
    """
    Main AI Orchestrator:
    1. Explains Error Codes (400, 401, 403, 404, 429, 500, 503, FLIX-402)
    2. Answers from SQL FAQ Knowledge Base
    3. Escalates & Creates SQL Support Ticket when unanswerable
    4. Provides Movie Recommendations
    5. Saves chat logs to MongoDB
    """
    prompt_clean = prompt.strip()
    result = {
        'reply': '',
        'intent': 'general',
        'recommended_ids': [],
        'ticket_id': None,
        'matched_error': None,
        'matched_faq': None
    }

    # 1. Check for Error Code query
    err = match_error_code(prompt_clean)
    if err:
        site_badge = " [Site-Specific Custom Code]" if err.is_site_specific else ""
        reply = (
            f"⚠️ **Error {err.code}: {err.title}**{site_badge}\n\n"
            f"**Description:**\n{err.description}\n\n"
            f"**Common Causes:**\n{err.common_causes}\n\n"
            f"**How to Resolve:**\n{err.troubleshooting}"
        )
        result['reply'] = reply
        result['intent'] = 'error_code_explanation'
        result['matched_error'] = err.code
        save_chat_log(session_id, prompt_clean, reply, intent='error_code_explanation', metadata={'code': err.code})
        return result

    # 2. Check if user needs support ticket or issue escalation
    if should_escalate_to_ticket(prompt_clean):
        ticket = create_support_ticket_from_prompt(prompt_clean, session_key=session_id)
        reply = (
            f"🎫 **Support Ticket Created Successfully!**\n\n"
            f"I have automatically escalated this issue to our technical support team:\n\n"
            f"• **Ticket ID:** `{ticket.ticket_id}`\n"
            f"• **Status:** `OPEN`\n"
            f"• **Priority:** `{ticket.priority}`\n"
            f"• **Subject:** _{ticket.subject}_\n\n"
            f"Our engineers have been alerted. You can track this in real-time on our [Support Desk](/support/)!"
        )
        result['reply'] = reply
        result['intent'] = 'ticket_escalation'
        result['ticket_id'] = ticket.ticket_id
        save_chat_log(session_id, prompt_clean, reply, intent='ticket_escalation', metadata={'ticket_id': ticket.ticket_id})
        return result

    # 3. Check for FAQ query
    faq = match_faq(prompt_clean)
    if faq:
        reply = (
            f"💡 **Frequently Asked Question** ({faq.get_category_display()}):\n\n"
            f"**Q: {faq.question}**\n\n"
            f"{faq.answer}\n\n"
            f"_For more assistance or account settings, visit our [FAQ Page](/faqs/) or ask me to open a support ticket!_"
        )
        result['reply'] = reply
        result['intent'] = 'faq_answer'
        result['matched_faq'] = faq.id
        save_chat_log(session_id, prompt_clean, reply, intent='faq_answer', metadata={'faq_id': faq.id})
        return result



    # 4. Fallback to Movie Recommendation / Cinematic Concierge if query is about watching/movies
    movie_keywords = ['movie', 'watch', 'show', 'film', 'series', 'recommend', 'sci-fi', 'action', 'thriller', 'comedy', 'drama', 'anime', 'vibe']
    is_movie_query = any(k in prompt_clean.lower() for k in movie_keywords)

    if is_movie_query and all_movies is not None:
        rec_movies = []
        for m in all_movies:
            # Simple keyword match
            if any(k in m.description.lower() or k in m.title.lower() for k in prompt_clean.lower().split()):
                rec_movies.append(m)
        if not rec_movies:
            rec_movies = list(all_movies[:3])

        rec_titles = [m.title for m in rec_movies[:3]]
        rec_ids = [m.id for m in rec_movies[:3]]
        reply = (
            f"🎬 Here are my top cinematic recommendations for you:\n\n"
            f"• **{rec_titles[0]}** - Highly rated for this vibe!\n"
            + ("\n".join([f"• **{t}**" for t in rec_titles[1:]])) +
            f"\n\nEnjoy your stream on StreamFlix!"
        )
        result['reply'] = reply
        result['intent'] = 'movie_recommendation'
        result['recommended_ids'] = rec_ids
        save_chat_log(session_id, prompt_clean, reply, intent='movie_recommendation', metadata={'rec_ids': rec_ids})
        return result

    # 5. General unanswerable fallback -> create ticket or offer help
    ticket = create_support_ticket_from_prompt(prompt_clean, session_key=session_id)
    reply = (
        f"🤖 I searched our FAQ and system documentation, but couldn't find a direct answer to: *\"{prompt_clean}\"*.\n\n"
        f"To ensure you get help right away, I have automatically created a support ticket for our developer support team:\n\n"
        f"• **Ticket Reference:** `{ticket.ticket_id}`\n"
        f"• **Priority:** `{ticket.priority}`\n"
        f"• **Logged:** Database records & MongoDB audit trail\n\n"
        f"You can also explore our [FAQ Page](/faqs/) or inspect [System Error Codes](/error-codes/)."
    )
    result['reply'] = reply
    result['intent'] = 'ticket_escalation'
    result['ticket_id'] = ticket.ticket_id
    save_chat_log(session_id, prompt_clean, reply, intent='ticket_escalation', metadata={'ticket_id': ticket.ticket_id})
    return result
