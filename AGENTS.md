# AGENTS.md

Spanish-language repo (docs, comments, UI). Single app in `unified-app/`: FastAPI serves **both** APIs and the static frontend on port 8000. No workspace config, no lockfiles, no tests/CI.

The unification of the two original demos (generator + dashboard) is **complete** — `spec.md`, `plan.md` and `task.md` record that refactor and are kept as its checklist/history; do not treat their "planned" state as pending. Root `README.md` documents the current setup.

## Commands

```bash
cd unified-app
python3 -m venv .venv && source .venv/bin/activate   # required: system Python is PEP 668-blocked (Homebrew)
pip install -r requirements.txt                      # fastapi, uvicorn
python database.py                                   # DESTRUCTIVE: wipes + reseeds database.db with today-relative dates
python -m uvicorn main:app --reload                  # http://localhost:8000
```

**Always run from `unified-app/`**: `database.db` and `static/` are cwd-relative — running elsewhere creates an empty DB and 404s on the frontend.

## Layout

- `unified-app/main.py` — both endpoints + `COURSES_DB` + `app.mount("/", StaticFiles(...))`.
- `unified-app/static/` — one `index.html` with two tab views (`#view-rutas`, `#view-progreso`), `app.js` (tab controller + both features), `style.css`.
- `unified-app/database.py` — SQLite schema + seed (only user `id = 1`).

## Gotchas

- **`StaticFiles` mount is the last line of `main.py`** — any new `/api/*` route added *after* it gets shadowed.
- **`python database.py` is destructive**: `DELETE`s all rows and reseeds with dates relative to `today`. Re-run it after manual DB edits; KPIs go stale if it hasn't run in a while (the 7-day window slides).
- **Chart.js + hidden tabs**: `#view-progreso` starts `hidden`; its data/chart load **lazily** on the first tab click (`progresoLoaded` flag in `app.js`). Rendering the chart while the canvas is hidden gives a 0-size chart — don't move `initDashboard()` back to `DOMContentLoaded`.
- **`GET /api/progreso/{user_id}`**: only user `1` exists in the seed; frontend hardcodes `/api/progreso/1` (same origin — no CORS, no absolute URLs; keep fetches relative).
- **`POST /api/rutas` returns 404** (not 422) when no courses match, and returns `[:3]` of the filtered list. Course id 6 is commented out, so Tecnología/Intermedio returns only **2** courses — expected, not a bug.
- Streak (`racha_dias`) uses local `date.today()`; the weekly-history SQL uses SQLite `date('now')` (UTC). Off-by-one around midnight/timezones is expected, not a regression.
- Backend swallows exceptions into a generic `500`; real failures only appear in the uvicorn/logs (`logger.error`).
- `database.db` and `.venv/` are gitignored; the DeprecationWarning from `database.py` (Python ≥3.12 date adapter) is harmless.

## Verification

No tests, lint, typecheck, or CI exist — don't invent one. Verify manually with the server running:

```bash
curl -X POST localhost:8000/api/rutas -H 'Content-Type: application/json' \
  -d '{"categoria":"Tecnología","nivel":"Básico"}'   # → 3 cursos; bad combo → 404
curl localhost:8000/api/progreso/1                    # → cursos_terminados, racha_dias, historial_semana
```

Plus a browser pass over both tabs (generate a route per category, switch tabs back and forth, reload). Trust code over docs if they diverge.
