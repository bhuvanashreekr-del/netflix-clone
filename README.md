# 🍿 StreamFlix — Personal Web Application & AI Diagnostics Platform
> **Final Assessment in Software Development**  
> **Student:** Bhuvanashree  
> **Repository:** [https://github.com/bhuvanashreekr-del/netflix-clone](https://github.com/bhuvanashreekr-del/netflix-clone)  
> **Live Website (HTTPS):** [https://prophet-position-tomorrow-counts.trycloudflare.com](https://prophet-position-tomorrow-counts.trycloudflare.com)  

---

## 📑 Project Overview & Assessment Task Title
**Task Title:** *StreamFlix: A Resilient Cloud-Deployed Web Platform with Dual-Database Architecture (SQL & MongoDB), Intelligent AI Support Concierge, and System Diagnostics.*

StreamFlix is an authentic, production-grade streaming application featuring modern web architecture, an integrated AI concierge (**FlixAI**), automated error diagnosis, real-time request logging, and resilient fallback systems across relational SQL and document-based NoSQL datastores.

---

## 🎯 Compliance Checklist (Assessment Requirements)

| Requirement | Implementation Details | Status |
| :--- | :--- | :---: |
| **Responsive Website (3+ Pages)** | Includes Home (`/`), FAQs (`/faqs/`), Error Codes (`/error-codes/`), Support Desk (`/support/`), Health (`/health/`), Movies (`/movies/`), TV Series (`/tv-shows/`), and Watchlist (`/my-list/`). Mobile optimized with responsive CSS flexbox/grid. | ✅ **Met** |
| **Chat Widget on Every Page** | Floating FlixAI assistant drawer injected globally via `base.html` accessible from any route across desktop & mobile. | ✅ **Met** |
| **10+ FAQs in SQL Database** | 12 comprehensive FAQs stored in SQLite/SQL (`FAQ` model) and interactively rendered on the `/faqs/` page with search and category filters. | ✅ **Met** |
| **8+ Error Codes (including site-specific)** | 8 codes documented and queryable (`ErrorCode` model): `400`, `401`, `403`, `404`, `429`, `500`, `503`, and proprietary `FLIX-402` (Concurrency Limit Exceeded). Accessible at `/error-codes/`. | ✅ **Met** |
| **Custom 404 & 500 Pages** | Custom cinematic `404.html` and `500.html` error templates with direct **"Ask the Assistant"** one-click diagnostic escalation. | ✅ **Met** |
| **AI Assistant (FAQs, Errors, Tickets)** | **FlixAI** natural language engine in `myapp/ai_engine.py` searches SQL FAQs, provides in-depth explanations for HTTP/site error codes, and automatically generates SQL support tickets when inquiries are unresolved. | ✅ **Met** |
| **Dual Database (SQL & MongoDB)** | • **SQL (SQLite/PostgreSQL):** Stores relational data (`Movie`, `Genre`, `Review`, `FAQ`, `ErrorCode`, `SupportTicket`, `RequestLog`).<br>• **MongoDB:** Stores semi-structured chat conversation logs and user feedback via `myapp/mongo_db.py`. | ✅ **Met** |
| **Security & Environment Variables** | No secrets stored in GitHub. Configured using environment variables (`SECRET_KEY`, `MONGODB_URI`, `GEMINI_API_KEY`, `DEBUG`) with `.env.example` template provided. | ✅ **Met** |
| **Request Logging & Health Check** | Custom middleware `RequestLoggingMiddleware` records path, method, status, latency, and IP. Live system diagnostics available at `/health/` (and `/health/?format=json`). | ✅ **Met** |
| **Third-Party API (Timeout & Fallback)** | Consumes external daily developer quote API (`myapp/third_party.py`) with strict `timeout=2.0s` and zero-latency curated fallback mechanism. | ✅ **Met** |
| **Proposed Improvement** | Detailed in this README under [Proposed Improvement & Future Roadmap](#-proposed-improvement--future-roadmap). | ✅ **Met** |

---

## 🏛️ System Architecture

```text
[ Web Client (Desktop / Mobile) ]
             │
             ▼
   [ Django Web Server / Gunicorn / WhiteNoise ]
             │
             ├── [ RequestLoggingMiddleware ] ──► [ SQL Database (RequestLog) ]
             │
             ├── [ Core Routing & Views ]
             │     ├── Home / Movies / TV Shows / Watchlist
             │     ├── FAQs Page ──────────────► [ SQL Database (FAQ Table) ]
             │     ├── Error Reference ────────► [ SQL Database (ErrorCode Table) ]
             │     ├── Support Portal ─────────► [ SQL Database (SupportTicket) ]
             │     └── Health Check ───────────► Real-time Latency & DB Ping
             │
             ├── [ FlixAI Concierge Engine (myapp/ai_engine.py) ]
             │     ├── 1. Natural Language Intent Matcher
             │     ├── 2. Error Code Diagnostic Lookup
             │     ├── 3. SQL FAQ Knowledge Search
             │     ├── 4. Automated Support Ticket Creator (Escalation)
             │     └── 5. Conversation & Feedback Logger ──► [ MongoDB (NoSQL) ]
             │
             └── [ Third-Party API Client (myapp/third_party.py) ]
                   ├── Primary: Live ZenQuotes / DummyJSON (Timeout: 2.0s)
                   └── Resilient Fallback: Local Cached Quotes Engine
```

---

## 🛠️ Technology Stack
- **Backend:** Python 3.12+, Django 6.x, Gunicorn WSGI, WhiteNoise static engine.
- **Frontend:** Semantic HTML5, Vanilla CSS3 (Dark Theme `#141414`, `#E50914` accents), JavaScript ES6+.
- **Databases:**
  - **Relational SQL:** SQLite / PostgreSQL (Django ORM).
  - **NoSQL Document Store:** MongoDB (via `pymongo` with resilient fallback).
- **Hosting & Cloud:** Render Web Service (`render.yaml` Blueprint).

---

## 🚀 Local Installation & Running Guide

### 1. Clone the Repository
```bash
git clone https://github.com/bhuvanashreekr-del/netflix-clone.git
cd netflix-clone
```

### 2. Set Up Virtual Environment & Dependencies
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Environment Configuration
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
*(Optionally provide `MONGODB_URI` and `GEMINI_API_KEY` in `.env`)*

### 4. Database Setup & Seeding
```bash
python manage.py migrate
python seed_db.py
```

### 5. Launch Development Server
```bash
python manage.py runserver
```
Visit **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)** in your browser.

---

## 💡 Proposed Improvement & Future Roadmap
*(Required Assessment Submission Section)*

### **Proposed Improvement: Real-Time Voice-Interactive Support Assistant via WebRTC & Automated Ticket Notification Webhooks**

#### Context & Motivation:
While the current text-based **FlixAI** assistant delivers rapid diagnosis of FAQs and error codes, streaming platform users encountering playback disruptions on living room smart TVs, tablets, or mobile devices experience high friction when typing detailed problem descriptions using on-screen keyboards.

#### Proposed Implementation:
1. **Low-Latency Voice AI Pipeline (WebRTC + Whisper):**
   - Integrate an in-browser voice capture interface using the Web Audio API and WebRTC.
   - Stream audio directly to a serverless transcription endpoint running OpenAI Whisper or Google Speech-to-Text for instant voice-to-text conversion.
   - Implement streaming text-to-speech (TTS) to verbally explain error codes (e.g. speaking: *"You are encountering Error FLIX-402 because your active stream limit was reached on another device"*).
2. **Automated Notification Webhooks for Support Tickets:**
   - When FlixAI escalates an issue and writes a `SupportTicket` to the SQL database, trigger an asynchronous background task (via Celery or Django Signals) dispatching an instant webhook to Slack/Discord or email (SendGrid).
   - This ensures engineering on-call responders receive critical ticket alerts (`URGENT` priority) in under 5 seconds.

#### Business & Technical Impact:
- **Reduces Time-to-Resolution (TTR)** by up to 60% for non-technical users.
- **Enhanced Accessibility (a11y)** for visually impaired users who cannot navigate complex error text.

---

## 👤 Author & Credentials
- **Student Developer:** Bhuvanashree  
- **GitHub:** [@bhuvanashreekr-del](https://github.com/bhuvanashreekr-del)  
- **Default Admin Portal:** `http://127.0.0.1:8000/admin/` (`admin` / `admin123`)
