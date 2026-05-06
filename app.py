import os
import time
import hashlib
import requests
from threading import Lock
from flask import Flask, render_template, request, jsonify, redirect

app = Flask(__name__)

# ── Config ────────────────────────────────────────────────────────────────────
TMDB_API_KEY  = os.getenv('TMDB_API_KEY')
TMDB_BASE_URL = 'https://api.themoviedb.org/3'
CACHE_TTL     = int(os.getenv('CACHE_TTL', 86400))   # seconds — default 24 h

if not TMDB_API_KEY:
    raise RuntimeError('TMDB_API_KEY environment variable is not set.')

# ── In-memory TTL cache ───────────────────────────────────────────────────────
# Much faster than requests_cache (SQLite): zero file I/O, no inter-worker
# lock contention. Each gunicorn worker keeps its own cache — cache misses
# just hit the TMDB API once per worker, which is completely fine.
#
# Structure: { cache_key: {'data': <dict>, 'ts': <float>} }
_cache: dict = {}
_cache_lock   = Lock()


def _cache_get(key: str):
    with _cache_lock:
        entry = _cache.get(key)
        if entry and (time.monotonic() - entry['ts']) < CACHE_TTL:
            return entry['data']
        return None


def _cache_set(key: str, data: dict):
    with _cache_lock:
        # Evict stale entries every ~500 writes so memory doesn't grow forever
        if len(_cache) % 500 == 0:
            now = time.monotonic()
            stale = [k for k, v in _cache.items() if now - v['ts'] >= CACHE_TTL]
            for k in stale:
                del _cache[k]
        _cache[key] = {'data': data, 'ts': time.monotonic()}


def _make_key(path: str, params: dict) -> str:
    """Stable cache key from path + sorted query params."""
    raw = path + '|' + '&'.join(f'{k}={v}' for k, v in sorted(params.items()) if k != 'api_key')
    return hashlib.md5(raw.encode()).hexdigest()


# ── Page routes ───────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/player')
@app.route('/player.html')
def player():
    return render_template('player.html')


# ── TMDB proxy — keeps the API key server-side ────────────────────────────────

@app.route('/api/tmdb')
def tmdb_proxy():
    path = request.args.get('path', '').strip()
    if not path:
        return jsonify({'error': 'Missing path parameter'}), 400

    if path.startswith('http'):
        return jsonify({'error': 'Invalid path'}), 400

    params = {k: v for k, v in request.args.items() if k != 'path'}
    cache_key = _make_key(path, params)

    # ── Cache hit: return immediately, no network call ────────────────────────
    cached = _cache_get(cache_key)
    if cached is not None:
        resp = jsonify(cached)
        resp.headers['X-Cache'] = 'HIT'
        resp.headers['Cache-Control'] = f'public, max-age={CACHE_TTL}'
        return resp

    # ── Cache miss: fetch from TMDB ───────────────────────────────────────────
    params['api_key'] = TMDB_API_KEY
    try:
        r = requests.get(
            f'{TMDB_BASE_URL}{path}',
            params=params,
            timeout=10,   # tighter timeout — fail fast, let the JS retry handle it
        )
        data = r.json()
    except requests.Timeout:
        return jsonify({'error': 'TMDB request timed out'}), 504
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    # Only cache successful responses
    if r.status_code == 200:
        _cache_set(cache_key, data)

    resp = jsonify(data)
    resp.headers['X-Cache'] = 'MISS'
    # Tell the browser to also cache this for 1 hour so repeated
    # visits / page navigations don't even hit the server
    resp.headers['Cache-Control'] = 'public, max-age=3600'
    return resp, r.status_code


# ── Cache stats endpoint (optional — useful for debugging) ───────────────────

@app.route('/api/cache-stats')
def cache_stats():
    with _cache_lock:
        total = len(_cache)
        now   = time.monotonic()
        fresh = sum(1 for v in _cache.values() if now - v['ts'] < CACHE_TTL)
    return jsonify({'total_entries': total, 'fresh_entries': fresh, 'ttl_seconds': CACHE_TTL})


# ── Legacy watch-route redirect ───────────────────────────────────────────────

@app.route('/watch/<media_type>/<tmdb_id>')
@app.route('/watch/<media_type>/<tmdb_id>/<int:season>/<int:episode>')
def watch(media_type, tmdb_id, season=1, episode=1):
    return redirect(f'/player?id={tmdb_id}&type={media_type}')


# ── Health check ──────────────────────────────────────────────────────────────

@app.route('/health')
def health():
    return jsonify({'status': 'ok'}), 200


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.getenv('FLASK_DEBUG', '0') == '1')
