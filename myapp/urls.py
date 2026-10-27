from django.urls import path
from . import views

urlpatterns = [
    # Core Application & Assessment Pages
    path('', views.home, name='home'),
    path('faqs/', views.faqs_view, name='faqs'),
    path('error-codes/', views.error_codes_view, name='error_codes'),
    path('support/', views.support_view, name='support'),
    path('health/', views.health_check_view, name='health'),
    path('tv-shows/', views.series_view, name='series'),
    path('movies/', views.movies_view, name='movies'),
    path('my-list/', views.my_list_view, name='my_list'),
    path('ai-assistant/', views.ai_assistant_view, name='ai_assistant'),
    path('search/', views.search_view, name='search'),

    # RESTful APIs
    path('api/watchlist/toggle/<int:movie_id>/', views.toggle_watchlist_api, name='toggle_watchlist'),
    path('api/movie/<int:movie_id>/', views.movie_detail_api, name='movie_detail'),
    path('api/movie/<int:movie_id>/review/', views.add_review_api, name='add_review'),
    path('api/ai/chat/', views.ai_chat_api, name='ai_chat'),
    path('api/feedback/submit/', views.submit_feedback_api, name='submit_feedback'),
    path('api/quote/', views.third_party_quote_api, name='third_party_quote'),
    path('404/', views.custom_404, name='preview_404'),
    path('500/', views.custom_500, name='preview_500'),
]
