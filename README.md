# 🎬 StreamFlix — Full-Stack Netflix Clone (Python & Django)

[![Python](https://img.shields.io/badge/Python-3.15%20%7C%203.12-3776AB?logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-6.1-092E20?logo=django&logoColor=white)](https://djangoproject.com)
[![Netflix Design](https://img.shields.io/badge/Design-Authentic%20Netflix-E50914?logo=netflix&logoColor=white)](#)
[![Deployment](https://img.shields.io/badge/Deploy-Render-46E3B7?logo=render&logoColor=white)](https://render.com)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

A high-performance, full-stack **Netflix Web Application Clone** built with **Python**, **Django 6**, **Vanilla CSS**, and **JavaScript**. Features an authentic cinematic dark UI, dynamic hero billboard, horizontal sliding carousels, **Top 10 Today** numbered cards, video trailer player modal, session-backed interactive **"My List" watchlist**, live search, community ratings/reviews, and complete Django Admin management.

---

## 🌟 Key Highlights & Features

### 1. 🎞️ Authentic Netflix UI & Experience
- **Cinematic Charcoal Palette**: Signature Netflix red (`#E50914`) and deep blacks (`#141414`), styled with custom vanilla CSS and Google Fonts (*Plus Jakarta Sans* & *Bebas Neue*).
- **Sticky Glassmorphic Navbar**: Smoothly transitions from a subtle top gradient to solid black upon scrolling down.
- **Top Billboard Hero**: Massive full-width backdrop with dual-axis vignette gradients, *"StreamFlix Original"* badge, match percentage, age maturity badge, synopsis, and action buttons.

### 2. 🍿 Curated Rows & Horizontal Carousels
- **Top 10 in India Today**: Giant outlined 3D numbers (1 through 10) flanking each movie poster, replicating Netflix's most iconic row.
- **Dynamic Category Rails**: *Trending Now*, *Sci-Fi & Cosmic Adventures*, *Anime Spotlight*, and *Action Thrillers*.
- **Smooth Rail Navigation**: Left and right chevron slider arrows (`‹` and `›`) that fade in on hover.

### 3. ⚡ Interactive Card Hover Mechanics
- Cards scale smoothly to `1.18x` with an elevated z-index on hover.
- Reveals quick action buttons:
  - ▶ **Play Trailer**
  - ➕ / ✓ **Toggle My List** (AJAX)
  - ⌵ **Expand Full Info Modal**
- Displays Match %, Age Rating (`U/A 16+`, `A 18+`), Duration, and Genre chips.

### 4. 🎥 Video Player Modal & Deep Details Modal
- **Trailer Video Player**: Full-screen modal overlay embedding responsive, high-definition official movie trailers.
- **Deep Detail Modal**: Large backdrop banner, full synopsis, director, full cast list, release year, and genres.

### 5. 💾 Session-Backed "My List" Watchlist (AJAX)
- Add or remove any movie or series to your personal watchlist with one click.
- Instant feedback with animated **Netflix Toast Notifications** on the bottom right.
- Dedicated **My List page (`/my-list/`)** displaying all bookmarked titles.

### 6. ⭐ Community Review & Rating System
- Interactive star rating picker (1 to 5 stars) and review submission form inside the detail modal.
- Reviews are saved in the SQLite database and updated instantly.

### 7. 🔍 Instant Search Engine
- Search across titles, actors (e.g. *Keanu Reeves*, *Pedro Pascal*), directors (e.g. *Christopher Nolan*), or genres (e.g. *Sci-Fi*, *Action*).

---

## 📂 Project Structure

```text
myproject/
├── myproject/             # Core Django configuration
│   ├── settings.py        # WhiteNoise, static files, and security settings
│   ├── urls.py            # Global URL dispatcher
│   └── wsgi.py            # WSGI application entrypoint for Gunicorn
├── myapp/                 # StreamFlix application
│   ├── models.py          # Genre, Movie, Watchlist, Review models
│   ├── views.py           # Views for Home, TV Shows, Movies, My List, Search & APIs
│   ├── urls.py            # App routes & REST API endpoints
│   ├── admin.py           # Django Admin panel registration
│   ├── templates/myapp/   # Semantic templates (base, home, browse, my_list, search)
│   └── static/myapp/css/  # Custom Netflix design system stylesheet (netflix.css)
├── build.sh               # Render cloud build script
├── render.yaml            # Render infrastructure specification
├── requirements.txt       # Production dependencies (Django, Gunicorn, WhiteNoise)
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
5. Click **Create Web Service**. Your live Netflix web app will be accessible worldwide!

---

## 👤 Author
- **Bhuvanashree K R**
- GitHub: [@bhuvanashreekr-del](https://github.com/bhuvanashreekr-del)
- Email: [bhuvanashreekr@gmail.com](mailto:bhuvanashreekr@gmail.com)
