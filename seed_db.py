import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

import django
django.setup()

from myapp.models import Genre, Movie, Review, FAQ, ErrorCode, SupportTicket

def seed():
    if Movie.objects.count() >= 10:
        print(f"[Seed] Database already has {Movie.objects.count()} movies. Skipping seed.")
        return

    print("[Seed] Populating initial StreamFlix catalog...")

    genres_data = [
        ("Action", "action"),
        ("Sci-Fi", "sci-fi"),
        ("Thriller", "thriller"),
        ("Anime", "anime"),
        ("Drama", "drama"),
        ("Fantasy", "fantasy"),
        ("Crime", "crime"),
        ("Adventure", "adventure"),
    ]

    genre_map = {}
    for name, slug in genres_data:
        g, _ = Genre.objects.get_or_create(name=name, slug=slug)
        genre_map[slug] = g

    movies_data = [
        {
            "title": "Cyberpunk: Neon Horizon",
            "tagline": "In a city of neon shadows, humanity has a price tag.",
            "description": "In 2099 Night Metropolis, a rogue cyber-detective uncovers an underground AI syndicate manipulating human consciousness. As corporate mercenaries close in, the boundary between memory and code begins to unravel.",
            "content_type": "series",
            "release_year": 2026,
            "duration": "3 Seasons",
            "rating": 9.4,
            "match_percentage": 99,
            "age_rating": "A 18+",
            "quality": "4K Ultra HD",
            "genres": ["sci-fi", "action", "thriller"],
            "thumbnail_url": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=600&auto=format&fit=crop&q=80",
            "backdrop_url": "https://images.unsplash.com/photo-1508739773434-c26b3d09e071?w=1600&auto=format&fit=crop&q=80",
            "trailer_youtube_id": "L6P3nI6VnlY",
            "is_featured_hero": True,
            "is_trending": True,
            "is_top_10": True,
            "top_10_rank": 1,
            "is_netflix_original": True,
            "cast": "Keanu Reeves, Ana de Armas, Hiroyuki Sanada",
            "director": "Denis Villeneuve",
        },
        {
            "title": "Interstellar: Beyond Event Horizon",
            "tagline": "Mankind was born on Earth. It was never meant to die here.",
            "description": "A team of deep-space pioneers embarks on humanity's farthest expedition through an anomalous wormhole, racing against relativistic time dilation to find a habitable sanctuary before Earth's biosphere collapses.",
            "content_type": "movie",
            "release_year": 2025,
            "duration": "2h 49m",
            "rating": 9.2,
            "match_percentage": 98,
            "age_rating": "U/A 13+",
            "quality": "4K Ultra HD",
            "genres": ["sci-fi", "adventure", "drama"],
            "thumbnail_url": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=600&auto=format&fit=crop&q=80",
            "backdrop_url": "https://images.unsplash.com/photo-1506703719100-a0f3a48c0f86?w=1600&auto=format&fit=crop&q=80",
            "trailer_youtube_id": "zSWdZVtXT7E",
            "is_featured_hero": False,
            "is_trending": True,
            "is_top_10": True,
            "top_10_rank": 2,
            "is_netflix_original": True,
            "cast": "Matthew McConaughey, Jessica Chastain, Michael Caine",
            "director": "Christopher Nolan",
        },
        {
            "title": "Stranger Echoes",
            "tagline": "When dark portals open, Hawkins will never sleep again.",
            "description": "When a local student vanishes without a trace in a quiet Midwestern town, four childhood friends uncover top-secret government experiments, terrifying supernatural forces, and a mysterious girl with telekinetic powers.",
            "content_type": "series",
            "release_year": 2026,
            "duration": "5 Seasons",
            "rating": 9.1,
            "match_percentage": 97,
            "age_rating": "U/A 16+",
            "quality": "4K Ultra HD",
            "genres": ["thriller", "fantasy", "drama"],
            "thumbnail_url": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=600&auto=format&fit=crop&q=80",
            "backdrop_url": "https://images.unsplash.com/photo-1517604931442-7e0c8ed2963c?w=1600&auto=format&fit=crop&q=80",
            "trailer_youtube_id": "b9EkMc79ZSU",
            "is_featured_hero": False,
            "is_trending": True,
            "is_top_10": True,
            "top_10_rank": 3,
            "is_netflix_original": True,
            "cast": "Millie Bobby Brown, David Harbour, Winona Ryder",
            "director": "The Duffer Brothers",
        },
        {
            "title": "Shadow Protocol: Extraction",
            "tagline": "No backup. No extraction plan. Only instinct.",
            "description": "A black-ops mercenary is recruited for an impossible rescue operation across the narrow alleys of Dhaka. Betrayed by corrupt handlers, he must fight his way through army barricades to protect an innocent hostage.",
            "content_type": "movie",
            "release_year": 2025,
            "duration": "2h 08m",
            "rating": 8.7,
            "match_percentage": 96,
            "age_rating": "A 18+",
            "quality": "4K Ultra HD",
            "genres": ["action", "thriller"],
            "thumbnail_url": "https://images.unsplash.com/photo-1579783900882-c0d3dad7b119?w=600&auto=format&fit=crop&q=80",
            "backdrop_url": "https://images.unsplash.com/photo-1534447677768-be436bb09401?w=1600&auto=format&fit=crop&q=80",
            "trailer_youtube_id": "L6P3nI6VnlY",
            "is_featured_hero": False,
            "is_trending": True,
            "is_top_10": True,
            "top_10_rank": 4,
            "is_netflix_original": True,
            "cast": "Chris Hemsworth, Golshifteh Farahani, Randeep Hooda",
            "director": "Sam Hargrave",
        },
        {
            "title": "Attack on Titan: The Final Legacy",
            "tagline": "To win total freedom, sacrifices must be made.",
            "description": "Centuries after giant humanoid Titans forced humanity into fortified walled cities, Eren Yeager unlocks the ultimate primordial power of the Founding Titan, launching the catastrophic Rumbling that shakes the world.",
            "content_type": "series",
            "release_year": 2025,
            "duration": "4 Seasons",
            "rating": 9.5,
            "match_percentage": 99,
            "age_rating": "A 18+",
            "quality": "4K Ultra HD",
            "genres": ["anime", "action", "fantasy"],
            "thumbnail_url": "https://images.unsplash.com/photo-1578632767115-351597cf2477?w=600&auto=format&fit=crop&q=80",
            "backdrop_url": "https://images.unsplash.com/photo-1563089145-599997674d42?w=1600&auto=format&fit=crop&q=80",
            "trailer_youtube_id": "M_OauHnAFc8",
            "is_featured_hero": False,
            "is_trending": True,
            "is_top_10": True,
            "top_10_rank": 5,
            "is_netflix_original": False,
            "cast": "Yuki Kaji, Yui Ishikawa, Hiroshi Kamiya",
            "director": "Tetsuro Araki",
        },
        {
            "title": "The Queen's Gambit: Masterclass",
            "tagline": "Genius has a dark, brilliant price.",
            "description": "Orphaned at nine, prodigy Beth Harmon discovers a miraculous talent for chess while developing an addiction to state-provided tranquilizers. Driven to conquer the male-dominated Soviet chess empire, she battles her inner demons.",
            "content_type": "series",
            "release_year": 2025,
            "duration": "Limited Series",
            "rating": 9.0,
            "match_percentage": 95,
            "age_rating": "U/A 16+",
            "quality": "4K Ultra HD",
            "genres": ["drama"],
            "thumbnail_url": "https://images.unsplash.com/photo-1529699211952-734e80c4d42b?w=600&auto=format&fit=crop&q=80",
            "backdrop_url": "https://images.unsplash.com/photo-1586165368502-1bad197a6461?w=1600&auto=format&fit=crop&q=80",
            "trailer_youtube_id": "oZn3qSgmLqI",
            "is_featured_hero": False,
            "is_trending": True,
            "is_top_10": True,
            "top_10_rank": 6,
            "is_netflix_original": True,
            "cast": "Anya Taylor-Joy, Bill Camp, Marielle Heller",
            "director": "Scott Frank",
        },
        {
            "title": "Quantum Heist",
            "tagline": "They are not stealing money. They are stealing time itself.",
            "description": "A high-stakes syndicate of rogue physicists and master thieves plans an unprecedented robbery inside the world's most guarded subatomic particle accelerator in Geneva to seize the prototype quantum tachyon drive.",
            "content_type": "movie",
            "release_year": 2026,
            "duration": "2h 14m",
            "rating": 8.8,
            "match_percentage": 94,
            "age_rating": "U/A 13+",
            "quality": "4K Ultra HD",
            "genres": ["sci-fi", "thriller", "action"],
            "thumbnail_url": "https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=600&auto=format&fit=crop&q=80",
            "backdrop_url": "https://images.unsplash.com/photo-1507499739999-097706ad8914?w=1600&auto=format&fit=crop&q=80",
            "trailer_youtube_id": "YoHD9XEInc0",
            "is_featured_hero": False,
            "is_trending": True,
            "is_top_10": True,
            "top_10_rank": 7,
            "is_netflix_original": True,
            "cast": "Tom Hardy, Michael Fassbender, Rebecca Ferguson",
            "director": "Christopher Nolan",
        },
        {
            "title": "Midnight Tokyo: Demon Slayer",
            "tagline": "When night falls over Shibuya, steel meets spiritual blood.",
            "description": "In modern-day Tokyo where ancient demons disguise themselves as corporate moguls, a covert brotherhood of katana wielders defends human civilization beneath the neon glow of rain-drenched rooftops.",
            "content_type": "series",
            "release_year": 2026,
            "duration": "2 Seasons",
            "rating": 9.3,
            "match_percentage": 98,
            "age_rating": "A 18+",
            "quality": "4K Ultra HD",
            "genres": ["anime", "action", "fantasy"],
            "thumbnail_url": "https://images.unsplash.com/photo-1569701813229-33284b643e3c?w=600&auto=format&fit=crop&q=80",
            "backdrop_url": "https://images.unsplash.com/photo-1542051841857-5f90071e7989?w=1600&auto=format&fit=crop&q=80",
            "trailer_youtube_id": "VQGCKyvzIM4",
            "is_featured_hero": False,
            "is_trending": True,
            "is_top_10": True,
            "top_10_rank": 8,
            "is_netflix_original": True,
            "cast": "Natsuki Hanae, Akari Kito, Hiro Shimono",
            "director": "Haruo Sotozaki",
        },
        {
            "title": "The Iron Vanguard",
            "tagline": "Courage tested in fire, brother against brother.",
            "description": "During the bleak winter warfare on a desolate European front line, a trapped armored tank battalion must hold a strategic mountain bridge against overwhelming odds to save thousands of retreating civilians.",
            "content_type": "movie",
            "release_year": 2025,
            "duration": "2h 21m",
            "rating": 8.9,
            "match_percentage": 93,
            "age_rating": "A 18+",
            "quality": "4K Ultra HD",
            "genres": ["action", "drama"],
            "thumbnail_url": "https://images.unsplash.com/photo-1542204165-65bf26472b9b?w=600&auto=format&fit=crop&q=80",
            "backdrop_url": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=1600&auto=format&fit=crop&q=80",
            "trailer_youtube_id": "F-eMt3SrfFU",
            "is_featured_hero": False,
            "is_trending": True,
            "is_top_10": True,
            "top_10_rank": 9,
            "is_netflix_original": False,
            "cast": "Brad Pitt, Shia LaBeouf, Logan Lerman",
            "director": "David Ayer",
        },
        {
            "title": "Solaris: The Deep Frontier",
            "tagline": "The ocean remembers everything you wished to forget.",
            "description": "Psychologist Kris Kelvin is dispatched to an isolated research orbital station hovering above the enigmatic sentient oceanic planet Solaris. He soon discovers the ocean has manifested the physical ghosts of his past.",
            "content_type": "movie",
            "release_year": 2025,
            "duration": "2h 32m",
            "rating": 8.7,
            "match_percentage": 92,
            "age_rating": "U/A 16+",
            "quality": "4K Ultra HD",
            "genres": ["sci-fi", "drama", "thriller"],
            "thumbnail_url": "https://images.unsplash.com/photo-1534447677768-be436bb09401?w=600&auto=format&fit=crop&q=80",
            "backdrop_url": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1600&auto=format&fit=crop&q=80",
            "trailer_youtube_id": "zSWdZVtXT7E",
            "is_featured_hero": False,
            "is_trending": True,
            "is_top_10": True,
            "top_10_rank": 10,
            "is_netflix_original": True,
            "cast": "George Clooney, Natascha McElhone, Jeremy Davies",
            "director": "Steven Soderbergh",
        },
        {
            "title": "Narcos: The Cartel Empire",
            "tagline": "There is no business like blood business.",
            "description": "A gritty, documentary-style chronicle tracing the ruthless ascension and devastating collapse of Colombia's most notorious drug empires and the DEA agents who sacrificed everything to bring them down.",
            "content_type": "series",
            "release_year": 2025,
            "duration": "3 Seasons",
            "rating": 9.2,
            "match_percentage": 96,
            "age_rating": "A 18+",
            "quality": "4K Ultra HD",
            "genres": ["crime", "drama", "thriller"],
            "thumbnail_url": "https://images.unsplash.com/photo-1517604931442-7e0c8ed2963c?w=600&auto=format&fit=crop&q=80",
            "backdrop_url": "https://images.unsplash.com/photo-1508739773434-c26b3d09e071?w=1600&auto=format&fit=crop&q=80",
            "trailer_youtube_id": "xl8zdCY-abw",
            "is_featured_hero": False,
            "is_trending": True,
            "is_top_10": False,
            "top_10_rank": 0,
            "is_netflix_original": True,
            "cast": "Wagner Moura, Pedro Pascal, Boyd Holbrook",
            "director": "Jose Padilha",
        },
        {
            "title": "Spirited Realms: The Lost Shrine",
            "tagline": "Step across the bridge into the domain of forgotten gods.",
            "description": "After stumbling into an ancient spiritual sanctuary nestled in misty mountain valleys, a determined young apprentice must master celestial elemental alchemy to lift a dark curse threatening both mortal and spirit worlds.",
            "content_type": "movie",
            "release_year": 2026,
            "duration": "2h 05m",
            "rating": 9.3,
            "match_percentage": 98,
            "age_rating": "U",
            "quality": "4K Ultra HD",
            "genres": ["anime", "fantasy", "adventure"],
            "thumbnail_url": "https://images.unsplash.com/photo-1578632767115-351597cf2477?w=600&auto=format&fit=crop&q=80",
            "backdrop_url": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=1600&auto=format&fit=crop&q=80",
            "trailer_youtube_id": "ByXuk9QqQkk",
            "is_featured_hero": False,
            "is_trending": True,
            "is_top_10": False,
            "top_10_rank": 0,
            "is_netflix_original": False,
            "cast": "Rumi Hiiragi, Miyu Irino, Mari Natsuki",
            "director": "Hayao Miyazaki",
        }
    ]

    for data in movies_data:
        genre_slugs = data.pop("genres")
        movie = Movie.objects.create(**data)
        for slug in genre_slugs:
            if slug in genre_map:
                movie.genres.add(genre_map[slug])

        Review.objects.create(
            movie=movie,
            user_name="Aarav Sharma",
            rating=5,
            comment=f"Absolute masterpiece! The cinematography and sound design in {movie.title} are next level."
        )
        Review.objects.create(
            movie=movie,
            user_name="Priya Patel",
            rating=5 if movie.rating >= 9.0 else 4,
            comment="Binge-watched this in one sitting. Can't wait for the next season / sequel!"
        )

    print(f"[Seed] Completed! {Movie.objects.count()} movies populated.")

def seed_faqs():
    print("Seeding FAQs (minimum 10 required)...")
    faqs_data = [
        {
            "question": "How do I upgrade or manage my StreamFlix subscription?",
            "answer": "You can manage your subscription under Account Settings > Membership & Billing. StreamFlix offers Standard (HD, 2 screens) and Premium (4K Ultra HD + HDR, 4 screens) tiers with cancel-anytime flexibility.",
            "category": "billing",
            "order": 1
        },
        {
            "question": "What internet speed is required to stream in 4K Ultra HD?",
            "answer": "A stable internet connection speed of at least 15 Mbps to 25 Mbps is recommended for smooth 4K Ultra HD playback. For Full HD (1080p), a 5 Mbps connection is sufficient.",
            "category": "streaming",
            "order": 2
        },
        {
            "question": "Can I download movies and TV shows for offline viewing?",
            "answer": "Yes! On supported mobile devices and tablets, tap the Download icon next to any movie title. Downloaded titles remain available offline in 'My Downloads' for up to 30 days.",
            "category": "streaming",
            "order": 3
        },
        {
            "question": "How does the FlixAI Concierge recommend content?",
            "answer": "FlixAI uses hybrid NLP and mood-intent semantic ranking to analyze your preferences, natural language mood descriptors (e.g. 'adrenaline rush', 'relaxing comedy'), and watch history to curate tailored lists.",
            "category": "ai_concierge",
            "order": 4
        },
        {
            "question": "How do I add a title to My Watchlist?",
            "answer": "Hover over any movie or series card and click the '+' (Plus) icon, or open the movie details modal and select 'Add to My List'. You can view your saved items anytime on the /my-list/ page.",
            "category": "general",
            "order": 5
        },
        {
            "question": "Why am I seeing an error message while streaming?",
            "answer": "Streaming errors are usually caused by temporary network interruptions, browser cache conflicts, or rate limits. Check our dedicated Error Codes page (/error-codes/) or ask our AI assistant to diagnose your specific error code.",
            "category": "troubleshooting",
            "order": 6
        },
        {
            "question": "How do I report a playback glitch or request support?",
            "answer": "You can ask the AI assistant in the chat widget on any page to create an automated support ticket, or manually submit your ticket on the /support/ page. Tickets are tracked in real-time.",
            "category": "troubleshooting",
            "order": 7
        },
        {
            "question": "Does StreamFlix support Spatial Audio and Dolby Atmos?",
            "answer": "Yes, Premium tier titles badged with 'Dolby Atmos' or '5.1 Surround' support multi-channel spatial audio on compatible smart TVs, AV receivers, and headphones.",
            "category": "streaming",
            "order": 8
        },
        {
            "question": "How do I reset my account password or update my email?",
            "answer": "Navigate to the Login page, click 'Forgot Password', and enter your registered email. A secure one-time reset link will be dispatched immediately.",
            "category": "general",
            "order": 9
        },
        {
            "question": "Are parental controls available to restrict mature content?",
            "answer": "Yes. You can configure age-rating filters (U/A 7+, U/A 13+, U/A 16+, A) and protect adult profiles with a 4-digit PIN under Account > Profile & Parental Controls.",
            "category": "general",
            "order": 10
        },
        {
            "question": "What is Error FLIX-402?",
            "answer": "FLIX-402 is a site-specific code indicating that the title is restricted to VIP subscribers or that the maximum simultaneous streaming quota for your current tier has been reached.",
            "category": "troubleshooting",
            "order": 11
        },
        {
            "question": "Where are chat logs and feedback stored?",
            "answer": "In accordance with modern microservices architecture, chat conversations and feedback are stored in a scalable NoSQL MongoDB cluster, while user accounts and tickets are stored in SQL.",
            "category": "ai_concierge",
            "order": 12
        }
    ]

    for item in faqs_data:
        FAQ.objects.update_or_create(
            question=item['question'],
            defaults=item
        )
    print(f"✓ Total FAQs in DB: {FAQ.objects.count()}")

def seed_error_codes():
    print("Seeding Error Codes (8 required: 400, 401, 403, 404, 429, 500, 503 + 1 site-specific)...")
    error_data = [
        {
            "code": "400",
            "title": "Bad Request",
            "category": "HTTP Client Error",
            "description": "The server could not understand the request due to malformed syntax, invalid JSON payload, or missing mandatory headers.",
            "common_causes": "Syntax errors in client API requests, missing query parameters, expired browser cookies, or corrupted file uploads.",
            "troubleshooting": "1. Verify payload formatting (ensure JSON is valid).\n2. Clear browser cookies and cache.\n3. Check API parameter names and types.",
            "is_site_specific": False
        },
        {
            "code": "401",
            "title": "Unauthorized",
            "category": "HTTP Client Error",
            "description": "The client must authenticate itself to get the requested response. Valid login credentials or an active session token are required.",
            "common_causes": "Expired authentication session, missing Bearer token, incorrect password, or invalid session key.",
            "troubleshooting": "1. Log into your account.\n2. Refresh your authentication token.\n3. Ensure cookies are enabled in your browser.",
            "is_site_specific": False
        },
        {
            "code": "403",
            "title": "Forbidden",
            "category": "HTTP Client Error",
            "description": "The client identity is known, but the server refuses authorization. Unlike 401, re-authenticating does not grant access.",
            "common_causes": "Attempting to access admin-only views without staff permissions, geographic content licensing restrictions, or CSRF token mismatch.",
            "troubleshooting": "1. Check your user account permission level.\n2. Ensure CSRF tokens are included on POST requests.\n3. Contact an administrator to request elevated permissions.",
            "is_site_specific": False
        },
        {
            "code": "404",
            "title": "Not Found",
            "category": "HTTP Client Error",
            "description": "The server cannot find the requested resource. The endpoint or movie URL does not exist or has been deleted.",
            "common_causes": "Typo in the URL bar, an expired link, or deleted catalog media.",
            "troubleshooting": "1. Double-check the URL spelling.\n2. Return to the Home page or browse categories.\n3. Click 'Ask the Assistant' on the 404 error page to get immediate help.",
            "is_site_specific": False
        },
        {
            "code": "429",
            "title": "Too Many Requests",
            "category": "HTTP Client Error",
            "description": "The user has sent too many requests in a given amount of time (Rate Limiting).",
            "common_causes": "Rapidly spamming API endpoints, continuous search queries without debouncing, or automated scraping bots.",
            "troubleshooting": "1. Wait a few moments (usually 30–60 seconds) before retrying.\n2. Implement client-side debounce on search inputs.\n3. Avoid automated scrapers.",
            "is_site_specific": False
        },
        {
            "code": "500",
            "title": "Internal Server Error",
            "category": "HTTP Server Error",
            "description": "The server encountered an unexpected condition that prevented it from fulfilling the request.",
            "common_causes": "Unhandled Python exceptions, database lockups, unapplied database migrations, or misconfigured middleware.",
            "troubleshooting": "1. Check server-side logs (`python manage.py runserver` or Render runtime logs).\n2. Verify database connectivity and migrations.\n3. Submit a support ticket so our engineers can investigate.",
            "is_site_specific": False
        },
        {
            "code": "503",
            "title": "Service Unavailable",
            "category": "HTTP Server Error",
            "description": "The server is currently unable to handle the request due to a temporary overload, cold-start booting, or maintenance.",
            "common_causes": "Server restarting after a deployment, upstream microservice failure, or traffic spike exceeding host limits.",
            "troubleshooting": "1. Wait 30 seconds and refresh the page.\n2. Check the system status at /health/.\n3. Verify that upstream cloud workers are online.",
            "is_site_specific": False
        },
        {
            "code": "FLIX-402",
            "title": "VIP Tier Concurrency Limit Exceeded",
            "category": "Site-Specific Application Code",
            "description": "StreamFlix proprietary error indicating your account has reached its concurrent 4K stream limit or requires a VIP tier upgrade.",
            "common_causes": "Streaming on more devices simultaneously than allowed by your subscription plan, or attempting to view 4K Ultra HD content on a Basic tier.",
            "troubleshooting": "1. Stop streaming on other household devices.\n2. Upgrade your membership plan in Account Settings.\n3. Ask the FlixAI Assistant to reset active device sessions.",
            "is_site_specific": True
        }
    ]

    for item in error_data:
        ErrorCode.objects.update_or_create(
            code=item['code'],
            defaults=item
        )
    print(f"✓ Total Error Codes in DB: {ErrorCode.objects.count()}")

def seed_sample_tickets():
    print("Seeding Sample Support Tickets...")
    tickets = [
        {
            "ticket_id": "TICK-104921",
            "name": "Sarah Connor",
            "email": "sarah@cyberdyne.org",
            "subject": "Audio desync on Cyberpunk: Neon Horizon 4K",
            "description": "The Dolby Atmos audio track drifts by approx 500ms when playing on Chrome browser with 120Hz monitor.",
            "error_code": "FLIX-402",
            "status": "IN_PROGRESS",
            "priority": "HIGH",
            "created_by_ai": True
        },
        {
            "ticket_id": "TICK-104922",
            "name": "Alex Mercer",
            "email": "alex@mercer-tech.io",
            "subject": "Question about offline download DRM limits",
            "description": "I would like clarification on how many offline devices are permitted per user account.",
            "error_code": "",
            "status": "OPEN",
            "priority": "LOW",
            "created_by_ai": True
        }
    ]
    for t in tickets:
        SupportTicket.objects.update_or_create(
            ticket_id=t['ticket_id'],
            defaults=t
        )
    print(f"✓ Total Support Tickets in DB: {SupportTicket.objects.count()}")


if __name__ == '__main__':
    seed()
    seed_faqs()
    seed_error_codes()
    seed_sample_tickets()
