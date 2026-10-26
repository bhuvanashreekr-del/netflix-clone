from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tv-shows/', views.series_view, name='series'),
    path('movies/', views.movies_view, name='movies'),
    path('my-list/', views.my_list_view, name='my_list'),
    path('search/', views.search_view, name='search'),
    path('api/watchlist/toggle/<int:movie_id>/', views.toggle_watchlist_api, name='toggle_watchlist'),
    path('api/movie/<int:movie_id>/', views.movie_detail_api, name='movie_detail'),
    path('api/movie/<int:movie_id>/review/', views.add_review_api, name='add_review'),
]
