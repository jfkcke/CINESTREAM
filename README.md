# 🎬 CineStream

A sleek, ad-free movie and TV show streaming discovery platform powered by the TMDB API and a Flask backend.

---

## ✨ Features

- 🔍 **Search** movies and TV shows with live autocomplete suggestions
- 🎭 **Browse** by genre, trending, popular, and top-rated categories
- 📺 **TV Show support** with season and episode selectors
- 🎬 **Multiple streaming servers** — switch instantly if one is down
- 🛡️ **Built-in Ad Blocker** — blocks popups, overlays, redirects, and tracker requests
- 🖼️ **Rich detail modals** with cast, ratings, runtime, and genres
- 📱 **Fully responsive** — works on mobile, tablet, and desktop
- ⚡ **Server-side caching** — fast responses with 24-hour TTL cache

---

## 🗂️ Project Structure

```
cinestream/
├── app.py                  # Flask backend — TMDB proxy + caching
├── requirements.txt        # Python dependencies
├── Procfile                # For Heroku / Railway / Render deployment
├── README.md               # This file
└── templates/
    ├── index.html          # Home page — browse, search, hero banner
    └── player.html         # Watch page — embedded player + ad blocker
```

---

## ⚙️ Local Development

### 1. Clone and install dependencies

```bash
git clone https://github.com/yourname/cinestream.git
cd cinestream
pip install -r requirements.txt
```

### 2. Get a TMDB API key

1. Create a free account at [themoviedb.org](https://www.themoviedb.org)
2. Go to **Settings → API** and copy your v3 API key

### 3. Set environment variables

```bash
# Linux / macOS
export TMDB_API_KEY=your_api_key_here

# Windows (PowerShell)
$env:TMDB_API_KEY = "your_api_key_here"
```

### 4. Run the server

```bash
python app.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

---

## 🚀 Deployment

### Railway / Render / Fly.io

1. Push your project to a GitHub repository
2. Connect the repo in your platform dashboard
3. Add the environment variable: `TMDB_API_KEY=your_key`
4. Deploy — the `Procfile` starts gunicorn automatically

### Heroku

```bash
heroku create your-app-name
heroku config:set TMDB_API_KEY=your_key
git push heroku main
```

---

## 🛡️ Ad Blocker

The built-in ad blocker in `player.html` protects users across 8 layers:

| Layer | What it blocks |
|---|---|
| Popup blocker | `window.open` ad popups |
| Fetch interceptor | Network requests to 30+ ad domains |
| XHR interceptor | Legacy ad/tracker requests |
| Tab-under blocker | Redirect hijacks to ad pages |
| Page hijack blocker | Programmatic navigation not triggered by the user |
| Focus theft blocker | Scripts stealing window focus for ads |
| DOM observer | Injected overlay and interstitial ad elements |
| Click trap layer | Synthetic ad-click events over the player |

A live counter in the player bar shows how many ads have been blocked.

---

## 🌐 Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `TMDB_API_KEY` | ✅ Yes | — | Your TMDB v3 API key |
| `CACHE_TTL` | No | `86400` | Cache duration in seconds (default 24h) |
| `PORT` | No | `5000` | Port to bind on (auto-set by most platforms) |
| `FLASK_DEBUG` | No | `0` | Set to `1` to enable debug mode |

---

## 🔧 API Endpoints

| Endpoint | Description |
|---|---|
| `GET /` | Home page |
| `GET /player` | Watch page (requires `?id=&type=` params) |
| `GET /api/tmdb` | TMDB proxy — pass `path` and any TMDB query params |
| `GET /api/cache-stats` | View cache status (total and fresh entries) |
| `GET /health` | Health check — returns `{"status": "ok"}` |
| `GET /watch/<type>/<id>` | Legacy redirect to player page |

---

## 📦 Dependencies

**Backend**
- [Flask](https://flask.palletsprojects.com/) — web framework
- [Requests](https://requests.readthedocs.io/) — HTTP client for TMDB calls
- [Gunicorn](https://gunicorn.org/) — production WSGI server

**Frontend** *(no npm, no build step — pure HTML/CSS/JS)*
- [TMDB API](https://developer.themoviedb.org/) — movie and TV data
- [Google Fonts](https://fonts.google.com/) — Bebas Neue + DM Sans

---

## ⚖️ Disclaimer

> CineStream does not host or store any media files. All content is embedded from third-party streaming servers. This project is intended for educational purposes only.

---

## 📄 License

MIT License — free to use, modify, and distribute.
