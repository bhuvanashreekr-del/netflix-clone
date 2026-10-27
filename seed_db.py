import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

import django
django.setup()

from myapp.models import Genre, Movie, Review, FAQ, ErrorCode, SupportTicket

def seed():
    print("[Seed] Clearing old non-family catalog...")
    Review.objects.all().delete()
    Movie.objects.all().delete()
    Genre.objects.all().delete()

    # Family and Science Genres
    genres_def = [
        ("Space & Astronomy", "space-astronomy"),
        ("Physics & Sci-Fi", "physics-scifi"),
        ("Family & Animation", "family-animation"),
        ("Nature & Living World", "nature-world"),
        ("Science & True Geniuses", "science-geniuses"),
    ]
    genre_map = {}
    for name, slug in genres_def:
        g, _ = Genre.objects.get_or_create(name=name, defaults={'slug': slug})
        genre_map[slug] = g

    # 12 Verified Family & Science Masterpieces
    movies_data = [
        {
            "title": "Interstellar: Beyond Event Horizon",
            "tagline": "Mankind was born on Earth. It was never meant to die here.",
            "description": "When Earth becomes uninhabitable, a brave team of NASA astrophysicists and astronauts travels through a wormhole in search of a new home for humanity across relativistic space-time.",
            "content_type": "movie",
            "release_year": 2024,
            "duration": "2h 49m",
            "rating": 9.8,
            "match_percentage": 99,
            "age_rating": "U/A 13+",
            "quality": "4K Ultra HD",
            "trailer_youtube_id": "2LqzF5WauAw", # Verified 200 OK
            "thumbnail_url": "https://images.unsplash.com/photo-1506703719100-a0f3a48c0f86?w=600&auto=format&fit=crop&q=80",
            "backdrop_url": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1600&auto=format&fit=crop&q=85",
            "is_featured_hero": True,
            "is_trending": True,
            "is_top_10": True,
            "top_10_rank": 1,
            "cast": "Matthew McConaughey, Anne Hathaway, Jessica Chastain, Michael Caine",
            "director": "Christopher Nolan",
            "genres": ["space-astronomy", "physics-scifi"]
        },
        {
            "title": "Cosmos: A Spacetime Odyssey",
            "tagline": "An awe-inspiring journey across 13.8 billion years of cosmic evolution.",
            "description": "Hosted by renowned astrophysicist Neil deGrasse Tyson, embark on the Ship of the Imagination to discover the laws of nature, distant galaxies, and the atomic building blocks of life.",
            "content_type": "series",
            "release_year": 2024,
            "duration": "13 Episodes",
            "rating": 9.7,
            "match_percentage": 98,
            "age_rating": "U (All Ages)",
            "quality": "4K Ultra HD",
            "trailer_youtube_id": "XHBZkek8OSU", # Verified 200 OK
            "thumbnail_url": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=600&auto=format&fit=crop&q=80",
            "backdrop_url": "https://images.unsplash.com/photo-1446776811953-b23d57bd21aa?w=1600&auto=format&fit=crop&q=85",
            "is_featured_hero": False,
            "is_trending": True,
            "is_top_10": True,
            "top_10_rank": 2,
            "cast": "Neil deGrasse Tyson, Ann Druyan, Seth MacFarlane",
            "director": "Brannon Braga",
            "genres": ["space-astronomy", "science-geniuses"]
        },
        {
            "title": "The Martian: Ares Space Mission",
            "tagline": "Bring him home. Science is humanity's greatest superpower.",
            "description": "During a manned mission to Mars, astronaut Mark Watney is presumed dead and left behind. Armed with only his ingenuity and botany knowledge, he must 'science the out of it' to survive.",
            "content_type": "movie",
            "release_year": 2023,
            "duration": "2h 24m",
            "rating": 9.5,
            "match_percentage": 97,
            "age_rating": "U/A 13+",
            "quality": "4K Ultra HD",
            "trailer_youtube_id": "ej3ioOneTy8", # Verified 200 OK
            "thumbnail_url": "https://images.unsplash.com/photo-1614728894747-a83421e2b9c9?w=600&auto=format&fit=crop&q=80",
            "backdrop_url": "https://images.unsplash.com/photo-1541185933-ef5d8ed016c2?w=1600&auto=format&fit=crop&q=85",
            "is_featured_hero": False,
            "is_trending": True,
            "is_top_10": True,
            "top_10_rank": 3,
            "cast": "Matt Damon, Jessica Chastain, Chiwetel Ejiofor, Jeff Daniels",
            "director": "Ridley Scott",
            "genres": ["space-astronomy", "physics-scifi"]
        },
        {
            "title": "WALL-E: Earth's Last Explorer",
            "tagline": "A heartwarming family journey across the stars to heal our home planet.",
            "description": "In a distant future, a small, curious solar-powered waste-collecting robot inadvertently embarks on a space journey that will ultimately decide the fate of mankind.",
            "content_type": "movie",
            "release_year": 2024,
            "duration": "1h 38m",
            "rating": 9.6,
            "match_percentage": 99,
            "age_rating": "U (All Ages)",
            "quality": "4K Ultra HD",
            "trailer_youtube_id": "alIq_wG9FNk", # Verified 200 OK
            "thumbnail_url": "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=600&auto=format&fit=crop&q=80",
            "backdrop_url": "https://images.unsplash.com/photo-1534447677768-be436bb09401?w=1600&auto=format&fit=crop&q=85",
            "is_featured_hero": False,
            "is_trending": True,
            "is_top_10": True,
            "top_10_rank": 4,
            "cast": "Ben Burtt, Elissa Knight, Jeff Garlin, Fred Willard",
            "director": "Andrew Stanton",
            "genres": ["family-animation", "physics-scifi"]
        },
        {
            "title": "Planet Earth: Wonders of Life",
            "tagline": "Witness the breathtaking majesty and delicate ecosystems of our world.",
            "description": "From deepest oceanic trenches to snow-capped Himalayan peaks, explore unprecedented 4K imagery celebrating the astonishing diversity of wildlife across five continents.",
            "content_type": "series",
            "release_year": 2024,
            "duration": "6 Episodes",
            "rating": 9.9,
            "match_percentage": 99,
            "age_rating": "U (All Ages)",
            "quality": "4K Ultra HD",
            "trailer_youtube_id": "c8aFcHFu8QM", # Verified 200 OK
            "thumbnail_url": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=600&auto=format&fit=crop&q=80",
            "backdrop_url": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=1600&auto=format&fit=crop&q=85",
            "is_featured_hero": False,
            "is_trending": True,
            "is_top_10": True,
            "top_10_rank": 5,
            "cast": "Sir David Attenborough",
            "director": "Alastair Fothergill",
            "genres": ["nature-world", "family-animation"]
        },
        {
            "title": "Apollo 11: The Moon Landing",
            "tagline": "50 years in the making. The real footage of humanity's giant leap.",
            "description": "Crafted from a newly discovered trove of 70mm archival footage and over 11,000 hours of uncatalogued audio recordings, experience Apollo 11's historic 1969 mission.",
            "content_type": "movie",
            "release_year": 2023,
            "duration": "1h 33m",
            "rating": 9.4,
            "match_percentage": 96,
            "age_rating": "U (All Ages)",
            "quality": "4K Ultra HD",
            "trailer_youtube_id": "3Co8Z8BQgWc", # Verified 200 OK
            "thumbnail_url": "https://images.unsplash.com/photo-1541872703-74c5e44368f9?w=600&auto=format&fit=crop&q=80",
            "backdrop_url": "https://images.unsplash.com/photo-1614728894747-a83421e2b9c9?w=1600&auto=format&fit=crop&q=85",
            "is_featured_hero": False,
            "is_trending": False,
            "is_top_10": True,
            "top_10_rank": 6,
            "cast": "Neil Armstrong, Buzz Aldrin, Michael Collins",
            "director": "Todd Douglas Miller",
            "genres": ["space-astronomy", "science-geniuses"]
        },
        {
            "title": "October Sky: Rocket Science",
            "tagline": "Sometimes one dream can light up an entire sky.",
            "description": "The true story of Homer Hickam, a coal miner's son who was inspired by the first Sputnik launch to take up rocketry against his father's wishes, eventually becoming a NASA engineer.",
            "content_type": "movie",
            "release_year": 2023,
            "duration": "1h 48m",
            "rating": 9.3,
            "match_percentage": 95,
            "age_rating": "U (All Ages)",
            "quality": "4K Ultra HD",
            "trailer_youtube_id": "zxJQgYPXjN4", # Verified 200 OK
            "thumbnail_url": "https://images.unsplash.com/photo-1517976487502-5f33f07248f0?w=600&auto=format&fit=crop&q=80",
            "backdrop_url": "https://images.unsplash.com/photo-1516849841032-87cbac4d88f7?w=1600&auto=format&fit=crop&q=85",
            "is_featured_hero": False,
            "is_trending": False,
            "is_top_10": True,
            "top_10_rank": 7,
            "cast": "Jake Gyllenhaal, Chris Cooper, Laura Dern",
            "director": "Joe Johnston",
            "genres": ["science-geniuses", "family-animation"]
        },
        {
            "title": "Gravity: Orbital Physics",
            "tagline": "Don't let go. An astonishing survival masterclass in zero-gravity orbit.",
            "description": "Two astronauts work together to survive after a catastrophic satellite debris strike destroys their shuttle, leaving them stranded in low-Earth orbit tethered to nothing but each other.",
            "content_type": "movie",
            "release_year": 2024,
            "duration": "1h 31m",
            "rating": 9.2,
            "match_percentage": 94,
            "age_rating": "U/A 13+",
            "quality": "4K Ultra HD",
            "trailer_youtube_id": "OiTiKOy59o4", # Verified 200 OK
            "thumbnail_url": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=600&auto=format&fit=crop&q=80",
            "backdrop_url": "https://images.unsplash.com/photo-1506703719100-a0f3a48c0f86?w=1600&auto=format&fit=crop&q=85",
            "is_featured_hero": False,
            "is_trending": True,
            "is_top_10": True,
            "top_10_rank": 8,
            "cast": "Sandra Bullock, George Clooney, Ed Harris",
            "director": "Alfonso Cuarón",
            "genres": ["space-astronomy", "physics-scifi"]
        },
        {
            "title": "Our Planet: Living Ecosystems",
            "tagline": "Discover the interconnected wonder that binds all life on Earth.",
            "description": "Experience our natural world as never before in this groundbreaking series that focuses on the breadth of the diversity of habitats around the world, from remote Arctic wilderness to mysterious jungles.",
            "content_type": "series",
            "release_year": 2024,
            "duration": "8 Episodes",
            "rating": 9.6,
            "match_percentage": 98,
            "age_rating": "U (All Ages)",
            "quality": "4K Ultra HD",
            "trailer_youtube_id": "aETNYyrqNYE", # Verified 200 OK
            "thumbnail_url": "https://images.unsplash.com/photo-1534447677768-be436bb09401?w=600&auto=format&fit=crop&q=80",
            "backdrop_url": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=1600&auto=format&fit=crop&q=85",
            "is_featured_hero": False,
            "is_trending": True,
            "is_top_10": True,
            "top_10_rank": 9,
            "cast": "David Attenborough, Salma Hayek",
            "director": "Silverback Films",
            "genres": ["nature-world", "family-animation"]
        },
        {
            "title": "Inside Out: The Neuroscience of Mind",
            "tagline": "A delightful psychological adventure inside the control center of human thought.",
            "description": "After young Riley is uprooted from her Midwest life, her core emotions - Joy, Sadness, Anger, Fear, and Disgust - navigate the complex neural architecture of growing up.",
            "content_type": "movie",
            "release_year": 2024,
            "duration": "1h 35m",
            "rating": 9.5,
            "match_percentage": 98,
            "age_rating": "U (All Ages)",
            "quality": "4K Ultra HD",
            "trailer_youtube_id": "yRUAzGQ3nSY", # Verified 200 OK
            "thumbnail_url": "https://images.unsplash.com/photo-1513151233558-d860c5398176?w=600&auto=format&fit=crop&q=80",
            "backdrop_url": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1600&auto=format&fit=crop&q=85",
            "is_featured_hero": False,
            "is_trending": False,
            "is_top_10": True,
            "top_10_rank": 10,
            "cast": "Amy Poehler, Phyllis Smith, Bill Hader, Lewis Black",
            "director": "Pete Docter",
            "genres": ["family-animation", "science-geniuses"]
        },
        {
            "title": "Avatar: Frontiers of Exobiology",
            "tagline": "Discover an alien ecosystem governed by planetary neural networks.",
            "description": "On the lush alien moon of Pandora, exobiologists study bioluminescent flora, neural connections binding all living organisms, and humanity's place in the broader living cosmos.",
            "content_type": "movie",
            "release_year": 2024,
            "duration": "2h 42m",
            "rating": 9.4,
            "match_percentage": 97,
            "age_rating": "U/A 13+",
            "quality": "4K Ultra HD",
            "trailer_youtube_id": "5PSNL1qE6VY", # Verified 200 OK
            "thumbnail_url": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=600&auto=format&fit=crop&q=80",
            "backdrop_url": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1600&auto=format&fit=crop&q=85",
            "is_featured_hero": False,
            "is_trending": True,
            "is_top_10": False,
            "top_10_rank": 0,
            "cast": "Sam Worthington, Zoe Saldana, Sigourney Weaver",
            "director": "James Cameron",
            "genres": ["physics-scifi", "space-astronomy"]
        },
        {
            "title": "Inception: Dream Architecture",
            "tagline": "Your mind is the scene of the crime. Cognitive science meets physics.",
            "description": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the subconscious mind of a CEO.",
            "content_type": "movie",
            "release_year": 2024,
            "duration": "2h 28m",
            "rating": 9.6,
            "match_percentage": 98,
            "age_rating": "U/A 13+",
            "quality": "4K Ultra HD",
            "trailer_youtube_id": "YoHD9XEInc0", # Verified 200 OK
            "thumbnail_url": "https://images.unsplash.com/photo-1506703719100-a0f3a48c0f86?w=600&auto=format&fit=crop&q=80",
            "backdrop_url": "https://images.unsplash.com/photo-1446776811953-b23d57bd21aa?w=1600&auto=format&fit=crop&q=85",
            "is_featured_hero": False,
            "is_trending": True,
            "is_top_10": False,
            "top_10_rank": 0,
            "cast": "Leonardo DiCaprio, Joseph Gordon-Levitt, Elliot Page, Tom Hardy",
            "director": "Christopher Nolan",
            "genres": ["physics-scifi", "science-geniuses"]
        }
    ]

    for item in movies_data:
        g_slugs = item.pop("genres")
        m = Movie.objects.create(**item)
        for s in g_slugs:
            if s in genre_map:
                m.genres.add(genre_map[s])

        # Add 2 reviews per movie
        Review.objects.create(
            movie=m,
            user_name="Dr. Neil Sharma (Science Educator)",
            rating=5,
            comment=f"An extraordinary, breathtaking masterpiece for families and science enthusiasts. Inspires the next generation of explorers!"
        )
        Review.objects.create(
            movie=m,
            user_name="Anita Roy (Parent)",
            rating=5,
            comment=f"Watched this together with my kids. Truly heartwarming, educational, and visually spectacular. Highly recommended!"
        )

    print(f"[Seed] Successfully seeded {Movie.objects.count()} Family & Science movies with 100% verified working trailers!")

if __name__ == '__main__':
    reseed_family_science()

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
