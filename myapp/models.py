from django.db import models
from django.utils.text import slugify

class Genre(models.Model):
    name = models.CharField(max_length=60, unique=True)
    slug = models.SlugField(max_length=60, unique=True, blank=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Movie(models.Model):
    CONTENT_TYPE_CHOICES = [
        ('movie', 'Movie'),
        ('series', 'TV Show'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    tagline = models.CharField(max_length=250, blank=True)
    description = models.TextField()
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPE_CHOICES, default='movie')
    release_year = models.IntegerField(default=2025)
    duration = models.CharField(max_length=50, default='2h 15m')
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=8.8)
    match_percentage = models.IntegerField(default=98)
    age_rating = models.CharField(max_length=15, default='U/A 16+')
    quality = models.CharField(max_length=20, default='4K Ultra HD')

    genres = models.ManyToManyField(Genre, related_name='movies')

    # Media
    thumbnail_url = models.URLField(max_length=600)
    backdrop_url = models.URLField(max_length=600)
    trailer_youtube_id = models.CharField(max_length=50, default='YoHD9XEInc0')

    # Curation Flags
    is_featured_hero = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)
    is_top_10 = models.BooleanField(default=False)
    top_10_rank = models.IntegerField(default=0, blank=True)
    is_netflix_original = models.BooleanField(default=True)

    cast = models.CharField(max_length=300, default='Pedro Pascal, Florence Pugh, Cillian Murphy')
    director = models.CharField(max_length=150, default='Christopher Nolan')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_featured_hero', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.release_year})"

class Watchlist(models.Model):
    session_key = models.CharField(max_length=50, db_index=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='watchlisted_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('session_key', 'movie')
        ordering = ['-added_at']

    def __str__(self):
        return f"Watchlist {self.session_key} - {self.movie.title}"

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    user_name = models.CharField(max_length=100)
    rating = models.IntegerField(default=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user_name} on {self.movie.title} ({self.rating}/5)"
