import json
import time
from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.db import connection

from .models import Genre, Movie, Watchlist, Review, FAQ, ErrorCode, SupportTicket, RequestLog
from .ai_engine import analyze_user_prompt
from .mongo_db import save_feedback, get_mongo_status
from .third_party import fetch_external_quote_with_fallback

# Global start time for uptime tracking
SERVER_START_TIME = time.time()

def get_session_watchlist_ids(request):
    """Retrieve list of movie IDs currently watchlisted in the user's session."""
    if not request.session.session_key:
        request.session.create()
    return list(Watchlist.objects.filter(session_key=request.session.session_key).values_list('movie_id', flat=True))

def home(request):
    """Netflix-style billboard hero and categorized carousels."""
    watchlist_ids = get_session_watchlist_ids(request)
    hero_movie = Movie.objects.filter(is_featured_hero=True).first() or Movie.objects.first()

    trending_movies = Movie.objects.filter(is_trending=True)
    top_10_movies = Movie.objects.filter(is_top_10=True).order_by('top_10_rank')[:10]
    sci_fi_movies = Movie.objects.filter(genres__slug='sci-fi').distinct()
    action_movies = Movie.objects.filter(genres__slug='action').distinct()
    drama_movies = Movie.objects.filter(genres__slug='drama').distinct()
    anime_movies = Movie.objects.filter(genres__slug='anime').distinct()

    # Third-party API quote with fallback
    daily_quote = fetch_external_quote_with_fallback(timeout_seconds=2.0)

    context = {
        'hero_movie': hero_movie,
        'trending_movies': trending_movies,
        'top_10_movies': top_10_movies,
        'sci_fi_movies': sci_fi_movies,
        'action_movies': action_movies,
        'drama_movies': drama_movies,
        'anime_movies': anime_movies,
        'watchlist_ids': watchlist_ids,
        'daily_quote': daily_quote,
        'page_title': 'Home - Watch TV Shows Online, Watch Movies Online'
    }
    return render(request, 'myapp/home.html', context)

def faqs_view(request):
    """Dedicated FAQ page displaying 10+ SQL-stored FAQs with category filtering."""
    category = request.GET.get('category', '').strip()
    query = request.GET.get('q', '').strip()

    faqs = FAQ.objects.filter(is_active=True)
    if category:
        faqs = faqs.filter(category=category)
    if query:
        faqs = faqs.filter(Q(question__icontains=query) | Q(answer__icontains=query))

    categories = FAQ.CATEGORY_CHOICES
    context = {
        'faqs': faqs,
        'categories': categories,
        'selected_category': category,
        'search_query': query,
        'total_faqs': FAQ.objects.filter(is_active=True).count(),
        'page_title': 'Frequently Asked Questions & Help Center'
    }
    return render(request, 'myapp/faqs.html', context)

def error_codes_view(request):
    """Dedicated Error Codes reference page (400, 401, 403, 404, 429, 500, 503, FLIX-402)."""
    error_codes = ErrorCode.objects.all().order_by('code')
    context = {
        'error_codes': error_codes,
        'total_errors': error_codes.count(),
        'page_title': 'System & HTTP Error Codes Reference'
    }
    return render(request, 'myapp/error_codes.html', context)

def support_view(request):
    """Support Tickets dashboard and creation portal (SQL-stored)."""
    if request.method == 'POST':
        name = request.POST.get('name', 'Anonymous User').strip() or 'Anonymous User'
        email = request.POST.get('email', 'support@streamflix.local').strip()
        subject = request.POST.get('subject', '').strip()
        description = request.POST.get('description', '').strip()
        error_code = request.POST.get('error_code', '').strip()
        priority = request.POST.get('priority', 'MEDIUM')

        if subject and description:
            ticket = SupportTicket.objects.create(
                name=name,
                email=email,
                subject=subject,
                description=description,
                error_code=error_code,
                priority=priority
            )
            return redirect(f'/support/?created={ticket.ticket_id}')

    tickets = SupportTicket.objects.all()[:20]
    created_id = request.GET.get('created', '')
    context = {
        'tickets': tickets,
        'created_id': created_id,
        'total_tickets': SupportTicket.objects.count(),
        'page_title': 'Support Center & Ticket Tracker'
    }
    return render(request, 'myapp/support.html', context)

def health_check_view(request):
    """
    Health check page validating:
    - System Uptime & Status
    - SQL Database Connectivity (SQLite)
    - MongoDB Connection / Fallback Status
    - Third-party API with Timeout and Fallback
    - Request Logging counts
    """
    start = time.time()

    # 1. Check SQL Database
    db_ok = True
    db_latency = 0.0
    try:
        t0 = time.time()
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")
            cursor.fetchone()
        db_latency = round((time.time() - t0) * 1000, 2)
    except Exception as e:
        db_ok = False

    # 2. Check MongoDB
    mongo_status = get_mongo_status()

    # 3. Check Third-party API with timeout
    third_party_res = fetch_external_quote_with_fallback(timeout_seconds=1.5)

    # 4. Request Logging statistics
    total_logs = RequestLog.objects.count()
    recent_logs = RequestLog.objects.all()[:10]

    uptime_seconds = int(time.time() - SERVER_START_TIME)
    uptime_formatted = f"{uptime_seconds // 3600}h {(uptime_seconds % 3600) // 60}m {uptime_seconds % 60}s"

    overall_status = "HEALTHY" if db_ok else "DEGRADED"

    health_data = {
        'status': overall_status,
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'uptime': uptime_formatted,
        'checks': {
            'sql_database': {
                'status': 'OPERATIONAL' if db_ok else 'FAILED',
                'engine': 'SQLite 3 (Django ORM)',
                'latency_ms': db_latency,
                'faqs_count': FAQ.objects.count(),
                'tickets_count': SupportTicket.objects.count(),
                'error_codes_count': ErrorCode.objects.count(),
            },
            'mongodb': mongo_status,
            'third_party_api': third_party_res,
            'request_logging': {
                'status': 'ACTIVE',
                'middleware': 'myapp.middleware.RequestLoggingMiddleware',
                'total_requests_logged': total_logs
            }
        }
    }

    # Support JSON output via query param or Accept header
    if request.GET.get('format') == 'json' or 'application/json' in request.META.get('HTTP_ACCEPT', ''):
        return JsonResponse(health_data, status=200 if db_ok else 503)

    return render(request, 'myapp/health.html', {
        'health': health_data,
        'recent_logs': recent_logs,
        'page_title': 'System Status & Health Check'
    })

def custom_404(request, exception=None):
    """Custom 404 page with direct 'Ask the Assistant' CTA."""
    context = {
        'page_title': '404 - Lost Your Way?',
        'requested_path': request.path
    }
    return render(request, '404.html', context, status=404)

def custom_500(request):
    """Custom 500 page with direct 'Ask the Assistant' CTA."""
    context = {
        'page_title': '500 - Internal Server Glitch'
    }
    return render(request, '500.html', context, status=500)

def series_view(request):
    watchlist_ids = get_session_watchlist_ids(request)
    series_list = Movie.objects.filter(content_type='series')
    return render(request, 'myapp/browse_category.html', {
        'title': 'TV Shows & Original Series',
        'movies': series_list,
        'watchlist_ids': watchlist_ids,
        'page_title': 'TV Shows - StreamFlix'
    })

def movies_view(request):
    watchlist_ids = get_session_watchlist_ids(request)
    movies_list = Movie.objects.filter(content_type='movie')
    return render(request, 'myapp/browse_category.html', {
        'title': 'Blockbuster Movies',
        'movies': movies_list,
        'watchlist_ids': watchlist_ids,
        'page_title': 'Movies - StreamFlix'
    })

def my_list_view(request):
    watchlist_ids = get_session_watchlist_ids(request)
    movies = Movie.objects.filter(id__in=watchlist_ids)
    return render(request, 'myapp/my_list.html', {
        'movies': movies,
        'watchlist_ids': watchlist_ids,
        'page_title': 'My List - StreamFlix'
    })

def ai_assistant_view(request):
    return render(request, 'myapp/ai_assistant.html', {
        'page_title': 'FlixAI - Intelligent Movie & Support Concierge'
    })

def search_view(request):
    query = request.GET.get('q', '').strip()
    watchlist_ids = get_session_watchlist_ids(request)
    movies = []
    if query:
        movies = Movie.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(cast__icontains=query) |
            Q(genres__name__icontains=query)
        ).distinct()

    return render(request, 'myapp/search.html', {
        'query': query,
        'movies': movies,
        'watchlist_ids': watchlist_ids,
        'page_title': f'Search: {query} - StreamFlix'
    })

# ========================================================
# REST APIs
# ========================================================

@csrf_exempt
def toggle_watchlist_api(request, movie_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=400)

    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    movie = get_object_or_404(Movie, id=movie_id)

    item = Watchlist.objects.filter(session_key=session_key, movie=movie).first()
    if item:
        item.delete()
        in_watchlist = False
        message = f"Removed '{movie.title}' from My List"
    else:
        Watchlist.objects.create(session_key=session_key, movie=movie)
        in_watchlist = True
        message = f"Added '{movie.title}' to My List"

    total = Watchlist.objects.filter(session_key=session_key).count()
    return JsonResponse({
        'success': True,
        'in_watchlist': in_watchlist,
        'total_count': total,
        'message': message,
        'movie_id': movie.id
    })

def movie_detail_api(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    reviews = movie.reviews.all()[:10]
    return JsonResponse({
        'id': movie.id,
        'title': movie.title,
        'tagline': movie.tagline,
        'description': movie.description,
        'release_year': movie.release_year,
        'duration': movie.duration,
        'rating': str(movie.rating),
        'match_percentage': movie.match_percentage,
        'age_rating': movie.age_rating,
        'quality': movie.quality,
        'genres': [g.name for g in movie.genres.all()],
        'cast': movie.cast,
        'director': movie.director,
        'thumbnail_url': movie.thumbnail_url,
        'backdrop_url': movie.backdrop_url,
        'trailer_url': f"https://www.youtube-nocookie.com/embed/{movie.trailer_youtube_id}?autoplay=1&rel=0",
        'reviews': [{
            'user_name': r.user_name,
            'rating': r.rating,
            'comment': r.comment,
            'created_at': r.created_at.strftime('%b %d, %Y')
        } for r in reviews]
    })

@csrf_exempt
def add_review_api(request, movie_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=400)

    movie = get_object_or_404(Movie, id=movie_id)
    data = {}
    if request.content_type == 'application/json':
        try:
            data = json.loads(request.body.decode('utf-8'))
        except Exception:
            data = {}
    else:
        data = request.POST

    user_name = str(data.get('user_name', '')).strip() or 'Movie Lover'
    try:
        rating = int(data.get('rating', 5))
    except (ValueError, TypeError):
        rating = 5
    comment = str(data.get('comment', '')).strip()

    if not comment:
        return JsonResponse({'error': 'Comment cannot be empty'}, status=400)

    review = Review.objects.create(
        movie=movie,
        user_name=user_name,
        rating=max(1, min(5, rating)),
        comment=comment
    )

    return JsonResponse({
        'success': True,
        'message': 'Review submitted successfully!',
        'review': {
            'user_name': review.user_name,
            'rating': review.rating,
            'comment': review.comment,
            'created_at': review.created_at.strftime('%b %d, %Y')
        }
    })

@csrf_exempt
def ai_chat_api(request):
    """
    Full AI Assistant API:
    - Explains error codes
    - Answers FAQ queries
    - Escalates & creates support tickets in SQL
    - Recommends movies
    - Records conversation logs into MongoDB
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=400)

    try:
        if request.content_type == 'application/json':
            body = json.loads(request.body.decode('utf-8'))
            prompt = body.get('prompt', '')
        else:
            prompt = request.POST.get('prompt', '')
    except Exception:
        prompt = request.POST.get('prompt', '')

    prompt = prompt.strip()
    if not prompt:
        return JsonResponse({'error': 'Prompt cannot be empty'}, status=400)

    if not request.session.session_key:
        request.session.create()
    session_id = request.session.session_key or 'guest_session'

    all_movies = Movie.objects.all()
    ai_result = analyze_user_prompt(prompt, all_movies=all_movies, session_id=session_id)

    rec_ids = ai_result.get('recommended_ids', [])
    recommended_movies = Movie.objects.filter(id__in=rec_ids)

    movies_data = [{
        'id': m.id,
        'title': m.title,
        'tagline': m.tagline,
        'backdrop_url': m.backdrop_url,
        'rating': float(m.rating),
        'match_percentage': m.match_percentage,
        'release_year': m.release_year,
        'quality': m.quality,
        'genres': [g.name for g in m.genres.all()]
    } for m in recommended_movies]

    return JsonResponse({
        'success': True,
        'reply': ai_result.get('reply', ''),
        'intent': ai_result.get('intent', 'general'),
        'ticket_id': ai_result.get('ticket_id'),
        'matched_error': ai_result.get('matched_error'),
        'matched_faq': ai_result.get('matched_faq'),
        'movies': movies_data,
        'recommended_movies': movies_data
    })

@csrf_exempt
def submit_feedback_api(request):
    """Receives user feedback rating & comments, storing into MongoDB."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=400)

    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body.decode('utf-8'))
        else:
            data = request.POST
    except Exception:
        data = request.POST

    if not request.session.session_key:
        request.session.create()
    session_id = request.session.session_key or 'guest_session'

    rating = data.get('rating', 5)
    comment = data.get('comment', '').strip()
    user_name = data.get('user_name', 'Streaming User').strip()

    res = save_feedback(session_id, rating, comment=comment, user_name=user_name)
    return JsonResponse({
        'success': True,
        'message': 'Thank you! Your feedback has been stored in MongoDB.',
        'result': res
    })

def third_party_quote_api(request):
    """Direct API endpoint demonstrating third-party API with timeout and fallback."""
    timeout_val = float(request.GET.get('timeout', 2.0))
    result = fetch_external_quote_with_fallback(timeout_seconds=timeout_val)
    return JsonResponse(result)
