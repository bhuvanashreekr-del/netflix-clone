import os
import re
import json
import requests
from django.db.models import Q
from .models import Movie, Genre

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')

# Predefined Mood Profiles with curated thematic keywords
MOOD_PROFILES = {
    'mind-bending': {
        'title': 'Mind-Bending & Paradoxes 🤯',
        'keywords': ['wormhole', 'time', 'quantum', 'dream', 'subatomic', 'physics', 'relativity', 'simulation', 'dimension', 'cyber'],
        'genres': ['sci-fi', 'thriller'],
        'tagline': 'Reality is merely an illusion. Prepare to question everything.',
    },
    'adrenaline': {
        'title': 'High Adrenaline & Combat ⚡',
        'keywords': ['mercenary', 'extraction', 'action', 'warfare', 'combat', 'sniper', 'explosive', 'assassin', 'frontline'],
        'genres': ['action', 'thriller'],
        'tagline': 'Pulse-pounding stunts, relentless pacing, and explosive action.',
    },
    'dark-thrills': {
        'title': 'Dark Mystery & Suspense 🕵️',
        'keywords': ['supernatural', 'disappears', 'cartel', 'syndicate', 'investigation', 'secrets', 'conspiracy', 'shadows'],
        'genres': ['thriller', 'crime', 'drama'],
        'tagline': 'Unravel dangerous conspiracies where nobody is who they seem.',
    },
    'anime-fantasy': {
        'title': 'Mythic Anime & Fantasy 🏮',
        'keywords': ['titan', 'katana', 'demons', 'spiritual', 'curse', 'alchemy', 'sanctuary', 'shrine', 'ancient'],
        'genres': ['anime', 'fantasy', 'adventure'],
        'tagline': 'Step through mystical gateways into stunning animated worlds.',
    },
    'cerebral-drama': {
        'title': 'Deep Character & Genius ♟️',
        'keywords': ['chess', 'prodigy', 'master', 'psychologist', 'solaris', 'sentient', 'obsession', 'talent', 'inner demons'],
        'genres': ['drama'],
        'tagline': 'Intense character studies and the price of extraordinary genius.',
    }
}

def analyze_user_prompt(prompt, available_movies):
    """
    Intelligent Hybrid AI Recommender:
    Attempts Gemini API if key is set, otherwise utilizes built-in Cinematic NLP Engine.
    """
    prompt_clean = prompt.strip().lower()

    if GEMINI_API_KEY:
        try:
            return _call_gemini_recommender(prompt, available_movies)
        except Exception as e:
            print(f"[FlixAI] Gemini call failed ({e}), falling back to internal NLP engine.")

    return _internal_nlp_recommender(prompt_clean, available_movies)

def _call_gemini_recommender(prompt, available_movies):
    """Call Google Gemini Generative API with structured movie catalog context."""
    catalog_summary = []
    for m in available_movies[:15]:
        genres = ", ".join([g.name for g in m.genres.all()])
        catalog_summary.append(f"ID:{m.id} | Title:{m.title} | Genres:{genres} | Year:{m.release_year} | Director:{m.director} | Synopsis:{m.description[:120]}")

    catalog_text = "\n".join(catalog_summary)

    system_instruction = (
        "You are FlixAI, the world-class cinema AI concierge for StreamFlix (a Netflix clone). "
        "Recommend the most fitting titles from our catalog based on the user's mood, taste, or request. "
        "Return a valid JSON object with two fields:\n"
        "1. 'reply': A warm, witty, cinema-literate response explaining why these fit (approx 2-3 sentences).\n"
        "2. 'recommended_ids': A list of integer IDs of the recommended movies from the catalog (top 1 to 4 IDs).\n"
        "Output ONLY raw JSON, no markdown formatting."
    )

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    payload = {
        "contents": [{
            "parts": [
                {"text": f"{system_instruction}\n\nCATALOG:\n{catalog_text}\n\nUSER REQUEST: {prompt}"}
            ]
        }],
        "generationConfig": {
            "temperature": 0.4,
            "maxOutputTokens": 400
        }
    }

    resp = requests.post(url, json=payload, timeout=8)
    if resp.status_code == 200:
        data = resp.json()
        raw_text = data['candidates'][0]['content']['parts'][0]['text']
        raw_text = re.sub(r'```json\s*', '', raw_text)
        raw_text = re.sub(r'```\s*', '', raw_text).strip()
        parsed = json.loads(raw_text)
        return {
            'reply': parsed.get('reply', 'Here are our top hand-picked recommendations for you!'),
            'recommended_ids': parsed.get('recommended_ids', [])
        }

    raise ValueError(f"Gemini API returned status {resp.status_code}")

def _internal_nlp_recommender(prompt, available_movies):
    """
    Built-in Natural Language Understanding & Scoring Engine.
    Requires no external API keys and provides human-like recommendations.
    """
    scored = []

    # Tokenize words
    words = set(re.findall(r'\b[a-z]{3,}\b', prompt))

    # Identify explicit mood or intent
    matched_mood = None
    for key, profile in MOOD_PROFILES.items():
        if any(kw in prompt for kw in profile['keywords']) or key in prompt:
            matched_mood = profile
            break

    for movie in available_movies:
        score = 0
        search_blob = f"{movie.title} {movie.tagline} {movie.description} {movie.cast} {movie.director} ".lower()
        movie_genres = [g.slug for g in movie.genres.all()]

        # Keyword matching
        for w in words:
            if w in movie.title.lower():
                score += 15
            elif w in movie.director.lower() or w in movie.cast.lower():
                score += 10
            elif w in search_blob:
                score += 4
            if w in movie_genres:
                score += 8

        # Mood profile boost
        if matched_mood:
            if any(g in movie_genres for g in matched_mood['genres']):
                score += 6
            if any(kw in search_blob for kw in matched_mood['keywords']):
                score += 5

        # General quality & match score weighting
        score += float(movie.rating) * 0.5
        score += (movie.match_percentage / 100.0) * 2.0

        if score > 5:
            scored.append((score, movie))

    # Sort descending
    scored.sort(key=lambda x: x[0], reverse=True)
    top_movies = [m for _, m in scored[:4]]

    # If no high matches, provide top-rated trending fallback
    if not top_movies:
        top_movies = list(available_movies.filter(is_trending=True)[:3])

    # Generate cinema concierge commentary
    if any(k in prompt for k in ['scifi', 'sci-fi', 'space', 'quantum', 'future', 'mind', 'twist']):
        reply = (
            f"🚀 For mind-bending concepts and cosmic horizons, you are going to love "
            f"**{top_movies[0].title}**! It pairs high-concept science with edge-of-your-seat drama. "
            f"Here are our curated top picks for your request:"
        )
    elif any(k in prompt for k in ['action', 'fight', 'war', 'thrill', 'shoot', 'fast']):
        reply = (
            f"💥 Strap in! If you're craving relentless adrenaline, **{top_movies[0].title}** "
            f"delivers top-tier stunt choreography and intense tactical pacing. Check these out:"
        )
    elif any(k in prompt for k in ['anime', 'titan', 'demon', 'japan', 'animation']):
        reply = (
            f"🏮 Excellent choice! For breathtaking world-building and epic battles, "
            f"**{top_movies[0].title}** is an absolute tour de force in modern animation:"
        )
    elif any(k in prompt for k in ['mystery', 'crime', 'cartel', 'detective', 'dark']):
        reply = (
            f"🕵️ If you're drawn to gritty shadows, high-stakes investigations, and plot twists, "
            f"**{top_movies[0].title}** will keep you guessing until the final seconds:"
        )
    else:
        reply = (
            f"✨ Based on your request, FlixAI has analyzed our catalog and matched you with "
            f"**{top_movies[0].title}** ({top_movies[0].match_percentage}% Match) along with these top-rated titles:"
        )

    return {
        'reply': reply,
        'recommended_ids': [m.id for m in top_movies]
    }

def get_mood_movies(mood_key):
    """Retrieve movies aligned with a specific mood profile."""
    profile = MOOD_PROFILES.get(mood_key, MOOD_PROFILES['mind-bending'])
    genre_slugs = profile['genres']

    movies = Movie.objects.filter(
        Q(genres__slug__in=genre_slugs) |
        Q(is_trending=True)
    ).distinct()[:8]

    return {
        'profile': profile,
        'movies': movies
    }

def generate_movie_insights(movie):
    """Generate AI insights and highlights for a movie modal."""
    genres_list = [g.name for g in movie.genres.all()]

    highlights = [
        f"Director {movie.director} crafts an immersive atmosphere with stunning 4K visuals.",
        f"Critically praised lead performances from {movie.cast.split(',')[0]} and the ensemble cast.",
        f"Masterful sound design and pacing tailored for {', '.join(genres_list)} enthusiasts."
    ]

    vibe_tags = [f"#{g.replace(' ', '')}" for g in genres_list]
    vibe_tags.extend(["#HighStakes", f"#{movie.quality.replace(' ', '')}", f"#Rating_{int(movie.rating)}Star"])

    similar = Movie.objects.filter(genres__in=movie.genres.all()).exclude(id=movie.id).distinct()[:3]

    return {
        'why_watch': f"Why you'll love {movie.title}: {movie.tagline or movie.description[:100]}...",
        'highlights': highlights,
        'vibe_tags': vibe_tags[:5],
        'similar_ids': [m.id for m in similar]
    }
