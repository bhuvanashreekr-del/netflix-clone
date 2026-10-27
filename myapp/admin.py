from django.contrib import admin
from .models import Genre, Movie, Watchlist, Review, FAQ, ErrorCode, SupportTicket, RequestLog

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


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'order', 'is_active', 'created_at')
    list_filter = ('category', 'is_active')
    search_fields = ('question', 'answer')
    list_editable = ('order', 'is_active')

@admin.register(ErrorCode)
class ErrorCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'category', 'is_site_specific')
    list_filter = ('category', 'is_site_specific')
    search_fields = ('code', 'title', 'description', 'troubleshooting')

@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_id', 'subject', 'name', 'status', 'priority', 'created_by_ai', 'created_at')
    list_filter = ('status', 'priority', 'created_by_ai')
    search_fields = ('ticket_id', 'subject', 'description', 'name', 'email')

@admin.register(RequestLog)
class RequestLogAdmin(admin.ModelAdmin):
    list_display = ('method', 'path', 'status_code', 'duration_ms', 'ip_address', 'timestamp')
    list_filter = ('status_code', 'method')
    search_fields = ('path', 'ip_address')
