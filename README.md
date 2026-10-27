# 🎬 StreamFlix — AI-Powered Full-Stack Netflix Web Application

[![Python](https://img.shields.io/badge/Python-3.15%20%7C%203.12-3776AB?logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-6.1-092E20?logo=django&logoColor=white)](https://djangoproject.com)
[![AI Engine](https://img.shields.io/badge/AI-FlixAI%20Copilot-9333EA?logo=openai&logoColor=white)](#)
[![Netflix Design](https://img.shields.io/badge/Design-Authentic%20Netflix-E50914?logo=netflix&logoColor=white)](#)
[![Deployment](https://img.shields.io/badge/Deploy-Render-46E3B7?logo=render&logoColor=white)](https://render.com)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

A high-performance, full-stack **Netflix Web Application Clone & AI Cinema Concierge** built with **Python**, **Django 6**, **Vanilla CSS**, **JavaScript**, and **FlixAI Intelligent Recommendation Engine**. Features an authentic cinematic dark UI, dynamic hero billboard, horizontal sliding carousels, **Top 10 Today** numbered cards, video trailer player modal, session-backed interactive **"My List" watchlist**, live search, community ratings/reviews, and an **interactive AI movie concierge (FlixAI)**.

---


[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/bhuvanashreekr-del/netflix-clone)


## 🌟 Architecture Breakdown: Frontend, Backend & AI

### 1. 🎨 Frontend Architecture
- **Authentic Netflix Design System**: Custom vanilla CSS with iconic Netflix Crimson (`#E50914`) and deep charcoal (`#141414`), typography with Google Fonts (*Plus Jakarta Sans* and *Bebas Neue*).
- **Sticky Glassmorphic Navbar**: Dynamically transitions from a subtle top gradient to solid black upon scrolling down.
- **Top Billboard Hero**: Massive full-width backdrop with dual-axis vignette gradients, *"StreamFlix Original"* badge, match percentage, age maturity badge, synopsis, and action buttons (`▶ Play`, `ℹ More Info`, `+ My List`).
- **Top 10 in India Today**: Giant outlined 3D numbers (1 through 10) flanking each movie poster, replicating Netflix's most iconic row.
- **Dynamic Category Rails**: *Trending Now*, *Sci-Fi & Cosmic Adventures*, *Anime Spotlight*, and *Action Thrillers* with left & right scroll arrows (`‹` and `›`).
- **Interactive Card Hover Expansion**: Cards scale smoothly to `1.18x` with an elevated z-index, revealing quick action buttons (Play, My List toggle, Info chevron), Match %, Age Rating (`U/A 16+`, `A 18+`), Duration, and Genre chips.
- **HD Video Trailer Player Modal**: Full-screen modal overlay embedding official trailers.

### 2. ⚙️ Backend Architecture
- **Django 6 MVT Architecture**: Clean separation of Models, Views, and Templates with custom context processors and session management.
- **Database Models (SQLite / PostgreSQL)**:
  - `Genre`: Normalized genre taxonomy (Action, Sci-Fi, Anime, Thriller, Drama, etc.).
  - `Movie`: Titles, taglines, synopsis, content_type ('movie' vs 'series'), year, duration, rating, match %, age rating, quality ('4K Ultra HD'), backdrop and poster URLs, YouTube trailer ID, cast, and director.
  - `Watchlist`: Session-backed bookmarking allowing users to add/remove titles to their personal "My List" with zero login friction.
  - `Review`: Star ratings (1 to 5) and viewer comments with timestamps, saved to the database.
- **REST APIs**:
  - `POST /api/watchlist/toggle/<movie_id>/`: Instant AJAX toggle for bookmarks.
  - `GET /api/movie/<movie_id>/`: Deep metadata and reviews endpoint.
  - `POST /api/movie/<movie_id>/review/`: Review submission endpoint.
  - `POST /api/ai/chat/`: AI cinema concierge natural language processing endpoint.
- **Django Admin Portal**: Full CRUD management of movies, genres, watchlists, and community reviews.
- **Production WhiteNoise & Gunicorn**: Compressed static assets and WSGI application server ready for Render cloud hosting.

### 3. 🧠 AI Engine Architecture (FlixAI)
- **Multi-Tier Hybrid AI Engine (`myapp/ai_engine.py`)**:
  - **Tier 1: Cloud LLM (Gemini API Integration)**: If `GEMINI_API_KEY` is present in environment variables, FlixAI calls Google Gemini with catalog context for advanced generative recommendations.
  - **Tier 2: Built-in Neuro-Symbolic Cinematic NLP Engine**: Runs natively in Python without requiring external API keys. Parses queries for moods, themes, actors, directors, plot tropes, and content types, scoring the database catalog with relevance algorithms.
- **Floating FlixAI Copilot**: A bottom-right glowing assistant button opening a full conversational drawer with quick-prompt chips (e.g. *"Mind-bending Sci-Fi like Inception"*, *"High octane tactical combat"*).
- **Interactive Chat Recommendations**: FlixAI responds conversationally and embeds clickable movie cards directly into the chat stream with instant "Play" and "Info" actions.
- **FlixAI Mood Matcher (`/ai-assistant/`)**: Dedicated discovery page mapping emotional states (*Mind-Bending 🤯*, *High Adrenaline ⚡*, *Dark Mystery 🕵️*, *Mythic Anime 🏮*, *Deep Character ♟️*) to tailored movie collections with custom AI reasoning.
- **FlixAI Title Insights**: Deep detail modal incorporates synthesized *"Why You'll Love This"* summaries and dynamic hashtag vibe tags.

---

## 📂 Project Structure

```text
myproject/
├── myproject/             # Core Django configuration
│   ├── settings.py        # WhiteNoise, static files, and security settings
│   ├── urls.py            # Global URL dispatcher
│   └── wsgi.py            # WSGI application entrypoint for Gunicorn
├── myapp/                 # StreamFlix application
│   ├── ai_engine.py       # FlixAI NLP & Gemini recommendation engine
│   ├── models.py          # Genre, Movie, Watchlist, Review models
│   ├── views.py           # Views for Home, TV Shows, Movies, My List, AI Assistant & APIs
│   ├── urls.py            # App routes & REST API endpoints
│   ├── admin.py           # Django Admin panel registration
│   ├── templates/myapp/   # Semantic templates (base, home, browse, my_list, search, ai_assistant)
│   └── static/myapp/css/  # Custom Netflix design system stylesheet (netflix.css)
├── build.sh               # Render cloud build script
├── render.yaml            # Render infrastructure specification
├── requirements.txt       # Production dependencies (Django, Gunicorn, WhiteNoise, Requests)
├── manage.py
└── README.md
```

---

## 🛠️ Local Development Setup

### 1. Clone the repository
```bash
git clone https://github.com/bhuvanashreekr-del/netflix-clone.git
cd netflix-clone
```

### 2. Set up a virtual environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply database migrations
```bash
python manage.py migrate
```

### 5. Start the local server
```bash
python manage.py runserver
```

Open **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)** in your browser!

---

## ☁️ Deploying to Render (Free Hosting)

1. Sign in to **[Render.com](https://render.com)** with your GitHub account (`bhuvanashreekr-del`).
2. Click **New +** > **Web Service**.
3. Select your repository: **`netflix-clone`**.
4. Configure the settings:
   - **Name**: `streamflix-app`
   - **Language**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn myproject.wsgi:application`
   - *(Optional)* **Environment Variables**: Add `GEMINI_API_KEY` if you wish to use Google Gemini for FlixAI.
5. Click **Create Web Service**.

---

## 👤 Author
- **Bhuvanashree K R**
- GitHub: [@bhuvanashreekr-del](https://github.com/bhuvanashreekr-del)
- Email: [bhuvanashreekr@gmail.com](mailto:bhuvanashreekr@gmail.com)
