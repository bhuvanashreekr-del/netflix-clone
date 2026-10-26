from django.contrib import admin
from .models import Genre, Movie, Watchlist, Review

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'content_type', 'release_year', 'rating', 'is_featured_hero', 'is_trending', 'is_top_10')
    list_filter = ('content_type', 'is_featured_hero', 'is_trending', 'is_top_10', 'is_netflix_original', 'genres')
    search_fields = ('title', 'description', 'cast', 'director')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('genres',)

@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('session_key', 'movie', 'added_at')
    search_fields = ('session_key', 'movie__title')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('movie', 'user_name', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user_name', 'comment', 'movie__title')
