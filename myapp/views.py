import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .models import Genre, Movie, Watchlist, Review
from .ai_engine import analyze_user_prompt, get_mood_movies, generate_movie_insights, MOOD_PROFILES

def _get_session_key(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key

def _get_user_watchlist_ids(request):
    session_key = _get_session_key(request)
    return set(Watchlist.objects.filter(session_key=session_key).values_list('movie_id', flat=True))

def home(request):
    featured = Movie.objects.filter(is_featured_hero=True).first()
    if not featured:
        featured = Movie.objects.first()

    trending_movies = Movie.objects.filter(is_trending=True)[:10]
    top_10_movies = Movie.objects.filter(is_top_10=True).order_by('top_10_rank')[:10]
    action_movies = Movie.objects.filter(genres__slug='action')[:10]
    scifi_movies = Movie.objects.filter(genres__slug='sci-fi')[:10]
    series_list = Movie.objects.filter(content_type='series')[:10]
    anime_list = Movie.objects.filter(genres__slug='anime')[:10]

    watchlist_ids = _get_user_watchlist_ids(request)
    my_list = Movie.objects.filter(id__in=watchlist_ids)
    genres = Genre.objects.all()

    return render(request, 'myapp/home.html', {
        'page_title': 'Watch TV Shows & Movies Online',
        'active_nav': 'home',
        'featured': featured,
        'trending_movies': trending_movies,
        'top_10_movies': top_10_movies,
        'action_movies': action_movies,
        'scifi_movies': scifi_movies,
        'series_list': series_list,
        'anime_list': anime_list,
        'my_list': my_list,
        'watchlist_ids': watchlist_ids,
        'genres': genres,
        'mood_profiles': MOOD_PROFILES,
    })

def series_view(request):
    watchlist_ids = _get_user_watchlist_ids(request)
    series = Movie.objects.filter(content_type='series')
    featured = series.filter(is_featured_hero=True).first() or series.first()

    return render(request, 'myapp/browse_category.html', {
        'page_title': 'TV Shows - StreamFlix',
        'active_nav': 'series',
        'category_name': 'TV Shows & Web Series',
        'featured': featured,
        'movies': series,
        'watchlist_ids': watchlist_ids,
    })

def movies_view(request):
    watchlist_ids = _get_user_watchlist_ids(request)
    movies = Movie.objects.filter(content_type='movie')
    featured = movies.filter(is_featured_hero=True).first() or movies.first()

    return render(request, 'myapp/browse_category.html', {
        'page_title': 'Movies - StreamFlix',
        'active_nav': 'movies',
        'category_name': 'Blockbuster Movies',
        'featured': featured,
        'movies': movies,
        'watchlist_ids': watchlist_ids,
    })

def my_list_view(request):
    watchlist_ids = _get_user_watchlist_ids(request)
    movies = Movie.objects.filter(id__in=watchlist_ids)

    return render(request, 'myapp/my_list.html', {
        'page_title': 'My List - StreamFlix',
        'active_nav': 'my_list',
        'movies': movies,
        'watchlist_ids': watchlist_ids,
    })

def ai_assistant_view(request):
    watchlist_ids = _get_user_watchlist_ids(request)
    selected_mood = request.GET.get('mood', 'mind-bending')
    mood_data = get_mood_movies(selected_mood)

    return render(request, 'myapp/ai_assistant.html', {
        'page_title': 'FlixAI Movie Concierge - StreamFlix',
        'active_nav': 'ai_assistant',
        'mood_profiles': MOOD_PROFILES,
        'selected_mood': selected_mood,
        'active_profile': mood_data['profile'],
        'mood_movies': mood_data['movies'],
        'watchlist_ids': watchlist_ids,
    })

def search_view(request):
    query = request.GET.get('q', '').strip()
    watchlist_ids = _get_user_watchlist_ids(request)

    results = []
    if query:
        results = Movie.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(cast__icontains=query) |
            Q(director__icontains=query) |
            Q(genres__name__icontains=query)
        ).distinct()

    return render(request, 'myapp/search.html', {
        'page_title': f'Search: {query}' if query else 'Search Titles',
        'active_nav': 'search',
        'query': query,
        'results': results,
        'watchlist_ids': watchlist_ids,
    })

# API Endpoints
def toggle_watchlist_api(request, movie_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=400)

    movie = get_object_or_404(Movie, id=movie_id)
    session_key = _get_session_key(request)

    entry = Watchlist.objects.filter(session_key=session_key, movie=movie).first()
    if entry:
        entry.delete()
        in_watchlist = False
        message = f"Removed '{movie.title}' from My List"
    else:
        Watchlist.objects.create(session_key=session_key, movie=movie)
        in_watchlist = True
        message = f"Added '{movie.title}' to My List"

    total_count = Watchlist.objects.filter(session_key=session_key).count()
    return JsonResponse({
        'success': True,
        'in_watchlist': in_watchlist,
        'total_count': total_count,
        'message': message,
        'movie_id': movie.id,
    })

def movie_detail_api(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    watchlist_ids = _get_user_watchlist_ids(request)
    reviews = movie.reviews.all()[:10]

    review_data = [{
        'user_name': r.user_name,
        'rating': r.rating,
        'comment': r.comment,
        'created_at': r.created_at.strftime('%b %d, %Y')
    } for r in reviews]

    genres_list = [g.name for g in movie.genres.all()]
    ai_insights = generate_movie_insights(movie)

    return JsonResponse({
        'id': movie.id,
        'title': movie.title,
        'tagline': movie.tagline,
        'description': movie.description,
        'content_type': movie.get_content_type_display(),
        'release_year': movie.release_year,
        'duration': movie.duration,
        'rating': float(movie.rating),
        'match_percentage': movie.match_percentage,
        'age_rating': movie.age_rating,
        'quality': movie.quality,
        'genres': genres_list,
        'thumbnail_url': movie.thumbnail_url,
        'backdrop_url': movie.backdrop_url,
        'trailer_youtube_id': movie.trailer_youtube_id,
        'cast': movie.cast,
        'director': movie.director,
        'is_netflix_original': movie.is_netflix_original,
        'in_watchlist': movie.id in watchlist_ids,
        'reviews': review_data,
        'ai_insights': ai_insights,
    })

def add_review_api(request, movie_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=400)

    movie = get_object_or_404(Movie, id=movie_id)
    user_name = request.POST.get('user_name', '').strip() or 'Movie Lover'
    rating = int(request.POST.get('rating', 5))
    comment = request.POST.get('comment', '').strip()

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

# AI Chat API
def ai_chat_api(request):
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

    all_movies = Movie.objects.all()
    ai_result = analyze_user_prompt(prompt, all_movies)

    rec_ids = ai_result.get('recommended_ids', [])
    recommended_movies = Movie.objects.filter(id__in=rec_ids)

    movies_data = [{
        'id': m.id,
        'title': m.title,
        'tagline': m.tagline,
        'backdrop_url': m.backdrop_url,
        'rating': float(m.rating),
        'match_percentage': m.match_percentage,
        'duration': m.duration,
        'trailer_youtube_id': m.trailer_youtube_id,
        'genres': [g.name for g in m.genres.all()]
    } for m in recommended_movies]

    return JsonResponse({
        'success': True,
        'reply': ai_result.get('reply', 'Here are your personalized recommendations!'),
        'recommended_movies': movies_data,
        'count': len(movies_data),
    })
