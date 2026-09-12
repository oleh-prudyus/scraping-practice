from . import db, notifications
from .config import logger
from .scraper import scrape_quotes


def run_scrape_job():
    run_id = db.start_run()
    logger.info("Починаю скрапінг")

    try:
        quotes = scrape_quotes()
        db.save_quotes(quotes)
        db.finish_run(run_id, "success", f"Зібрано {len(quotes)} цитат")
        logger.info(f"Скрапінг завершено успішно: {len(quotes)} цитат")
        notifications.send_telegram(f"✅ Скрапінг завершено: {len(quotes)} цитат")
    except Exception as e:
        db.finish_run(run_id, "failed", str(e))
        logger.error(f"Скрапінг провалився: {e}")
        notifications.send_telegram(f"⚠️ Скрапінг провалився: {e}")
        raise
