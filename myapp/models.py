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


class FAQ(models.Model):
    CATEGORY_CHOICES = [
        ('general', 'General & Account'),
        ('streaming', 'Streaming & Quality'),
        ('billing', 'Billing & Subscriptions'),
        ('troubleshooting', 'Troubleshooting & Errors'),
        ('ai_concierge', 'FlixAI Assistant'),
    ]

    question = models.CharField(max_length=300)
    answer = models.TextField()
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='general')
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'category', 'id']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'

    def __str__(self):
        return self.question


class ErrorCode(models.Model):
    code = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=120)
    category = models.CharField(max_length=30, default='HTTP Client Error')
    description = models.TextField()
    common_causes = models.TextField()
    troubleshooting = models.TextField()
    is_site_specific = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['code']
        verbose_name = 'Error Code'
        verbose_name_plural = 'Error Codes'

    def __str__(self):
        return f'{self.code} - {self.title}'


class SupportTicket(models.Model):
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
        ('CLOSED', 'Closed'),
    ]
    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('URGENT', 'Urgent'),
    ]

    ticket_id = models.CharField(max_length=30, unique=True, blank=True)
    name = models.CharField(max_length=120, default='Streaming User')
    email = models.EmailField(default='support-request@example.com')
    subject = models.CharField(max_length=200)
    description = models.TextField()
    error_code = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='MEDIUM')
    created_by_ai = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.ticket_id:
            import random, time
            timestamp = int(time.time()) % 100000
            rand = random.randint(100, 999)
            self.ticket_id = f'TICK-{timestamp}{rand}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'[{self.ticket_id}] {self.subject} ({self.status})'


class RequestLog(models.Model):
    path = models.CharField(max_length=300)
    method = models.CharField(max_length=10)
    status_code = models.IntegerField()
    duration_ms = models.FloatField(default=0.0)
    ip_address = models.CharField(max_length=60, default='127.0.0.1')
    user_agent = models.CharField(max_length=300, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.method} {self.path} -> {self.status_code} ({self.duration_ms:.1f}ms)'
