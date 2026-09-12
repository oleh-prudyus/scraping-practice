# Dashboard Backend

FastAPI service controlling a scheduled scraper.

## Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/status` | Scheduler state and last run info |
| POST | `/toggle` | Enable/disable scheduled runs (`{"enabled": true}`) |
| POST | `/run` | Trigger a scrape run in the background |
| GET | `/data?limit=200` | Return scraped records |
| GET | `/notifications` | Current Telegram config (token masked) |
| POST | `/notifications` | Save Telegram bot token + chat ID |

Interactive docs at `/docs` once running.

## Structure

- `app/config.py` — paths, logging setup
- `app/db.py` — SQLite: settings, quotes, run history
- `app/scraper.py` — Requests + BeautifulSoup scraper with retry/backoff
- `app/notifications.py` — Telegram `sendMessage` integration
- `app/job.py` — scrape → save → log → notify pipeline
- `app/scheduler.py` — APScheduler wrapper (enable/disable without touching the OS)
- `app/main.py` — FastAPI app and routes

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```
