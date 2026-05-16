# CineStream 🎬

A fast, clean movie and TV streaming discovery app built with Flask and the TMDB API. Browse trending titles, search across movies and shows, and watch instantly — all from a single-page experience with no sign-up required.

**Live site:** https://cinestream-1-ucdr.onrender.com

---

## Features

- **Hero banner** — auto-rotating showcase of trending movies with backdrop art, ratings, and quick-play
- **Browsable rows** — Trending, Popular, Top Rated, and TV Shows carousels with smooth horizontal scroll
- **Live search with autocomplete** — results appear as you type with poster thumbnails, year, and rating; keyboard navigable
- **Detail modal** — click any title to see full metadata (overview, genres, cast, runtime, release date) without leaving the page
- **Integrated player** — watch movies and TV episodes directly in-app via an embedded player with episode/season switching for TV shows
- **More Like This** — similar title suggestions shown below the player
- **Cast display** — actor photos, character names, and roles shown per title
- **TMDB proxy with caching** — API key kept server-side; responses cached in-memory for 24 hours so repeat requests never hit the network
- **Mobile responsive** — works on phones, tablets, and desktops

---

## Project Structure

```
cinestream/
├── app.py                  # Flask backend — TMDB proxy + caching + routes
├── requirements.txt        # Python dependencies
├── Procfile                # Gunicorn start command for deployment
└── templates/
    ├── index.html          # Home page — hero, carousels, search, detail modal
    └── player.html         # Watch page — embedded player, cast, More Like This
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python · Flask · Gunicorn |
| Frontend | Vanilla JS · HTML · CSS |
| Data | TMDB API v3 |
| Fonts | Bebas Neue · DM Sans (Google Fonts) |
| Hosting | Render / Railway / Heroku compatible |
| Caching | In-memory TTL cache (per worker, 24h default) |

---

## Local Development

**1. Clone the repo and install dependencies**
```bash
git clone https://github.com/jfkcke/cinestream.git
cd cinestream
pip install -r requirements.txt
```

**2. Get a TMDB API key**

Sign up free at https://www.themoviedb.org/settings/api and copy your v3 API key.

**3. Set the environment variable**
```bash
# macOS / Linux
export TMDB_API_KEY=your_key_here

# Windows (Command Prompt)
set TMDB_API_KEY=your_key_here

# Windows (PowerShell)
$env:TMDB_API_KEY="your_key_here"
```

**4. Run the dev server**
```bash
python app.py
```

Open http://localhost:5000 in your browser.

---

## Deployment

CineStream works out of the box on any platform that supports Python and reads a `Procfile`.

### Render (recommended — free tier available)

1. Push the repo to GitHub
2. Go to https://render.com → New Web Service → connect your repo
3. Set environment variable: `TMDB_API_KEY` = your key
4. Build command: `pip install -r requirements.txt`
5. Start command is handled by the `Procfile` automatically

### Railway

1. Push to GitHub
2. New Project → Deploy from GitHub repo
3. Add environment variable `TMDB_API_KEY` in the Variables tab
4. Deploy — Railway detects the `Procfile` automatically

### Heroku

```bash
heroku create your-app-name
heroku config:set TMDB_API_KEY=your_key_here
git push heroku main
```

---

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `TMDB_API_KEY` | Yes | — | Your TMDB v3 API key |
| `CACHE_TTL` | No | `86400` | Cache lifetime in seconds (default 24h) |
| `PORT` | No | `5000` | Port to bind on (set automatically by hosting platforms) |
| `FLASK_DEBUG` | No | `0` | Set to `1` for debug mode — dev only, never in production |

---

## How the TMDB Proxy Works

All TMDB requests go through `/api/tmdb?path=...` on the Flask backend. This keeps your API key out of the browser and adds two layers of caching:

- **Server cache** — in-memory TTL dict (default 24h). Cache hits return instantly with zero network calls. Stale entries are evicted automatically every 500 writes.
- **Browser cache** — responses include `Cache-Control: public, max-age=3600` so the browser caches them for 1 hour. Navigating back to a page you already visited makes zero requests to the server.

Each gunicorn worker maintains its own cache — on a cold miss per worker the TMDB API is called once, then cached. This is intentional; a shared SQLite cache would introduce file I/O and lock contention across workers.

---

## API Endpoints

| Endpoint | Description |
|---|---|
| `GET /` | Home page |
| `GET /player` | Watch page (requires `?id=<tmdb_id>&type=movie\|tv`) |
| `GET /api/tmdb?path=<path>&...` | TMDB proxy — pass any TMDB v3 path and params |
| `GET /api/cache-stats` | Debug endpoint — shows cache entry count and freshness |
| `GET /watch/<type>/<id>` | Legacy redirect → `/player` |
| `GET /health` | Health check — returns `{"status": "ok"}` |

---

## Legal

This site does not store any media files on its servers. All content metadata is sourced from [TMDB](https://www.themoviedb.org). Streaming is provided via third-party embedded players.

> This product uses the TMDB API but is not endorsed or certified by TMDB.

---

## License

MIT — do whatever you want, just don't remove the TMDB attribution.
