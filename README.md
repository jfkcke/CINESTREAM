# CineStream

A movie and TV streaming discovery app powered by TMDB and Flask.

## Project Structure

```
cinestream/
├── app.py               # Flask backend (TMDB proxy)
├── requirements.txt     # Python dependencies
├── Procfile             # For Heroku / Railway deployment
├── .env.example         # Environment variable template
└── templates/
    ├── index.html       # Home page
    └── player.html      # Watch page
```

## Local Development

1. **Clone and install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set your TMDB API key**
   ```bash
   cp .env.example .env
   # Edit .env and add your key from https://www.themoviedb.org/settings/api
   ```

3. **Run the dev server**
   ```bash
   export TMDB_API_KEY=your_key_here   # or use python-dotenv
   python app.py
   ```
   Then open http://localhost:5000

## Deployment

### Railway / Render / Fly.io

1. Push to a GitHub repo
2. Connect the repo in your platform dashboard
3. Set the environment variable: `TMDB_API_KEY=your_key`
4. The `Procfile` handles the rest — gunicorn starts automatically

### Heroku

```bash
heroku create your-app-name
heroku config:set TMDB_API_KEY=your_key
git push heroku main
```

## Environment Variables

| Variable      | Required | Description                          |
|---------------|----------|--------------------------------------|
| `TMDB_API_KEY`| Yes      | Your TMDB v3 API key                 |
| `FLASK_DEBUG` | No       | Set to `1` for debug mode (dev only) |
| `CACHE_DIR`   | No       | Directory for response cache (default `/tmp`) |
| `PORT`        | No       | Port to bind on (set automatically by most platforms) |
