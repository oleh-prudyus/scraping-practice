from . import db, notifications
from .config import logger
from .scraper import scrape_quotes


def run_scrape_job():
    run_id = db.start_run()
    logger.info("Starting scrape job")

    try:
        quotes = scrape_quotes()
        db.save_quotes(quotes)
        db.finish_run(run_id, "success", f"Collected {len(quotes)} quotes")
        logger.info(f"Scrape completed successfully: {len(quotes)} quotes")
        notifications.send_telegram(f"✅ Scrape completed: {len(quotes)} quotes")
    except Exception as e:
        db.finish_run(run_id, "failed", str(e))
        logger.error(f"Scrape failed: {e}")
        notifications.send_telegram(f"⚠️ Scrape failed: {e}")
        raise
