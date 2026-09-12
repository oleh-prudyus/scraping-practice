from apscheduler.schedulers.background import BackgroundScheduler

from . import db
from .config import logger
from .job import run_scrape_job

JOB_ID = "scrape_job"

scheduler = BackgroundScheduler()


def start_scheduler():
    scheduler.start()
    if db.get_setting("scheduler_enabled") == "true":
        _add_job()


def _add_job():
    if not scheduler.get_job(JOB_ID):
        scheduler.add_job(run_scrape_job, "interval", minutes=30, id=JOB_ID)
        logger.info("Scheduled scraping enabled (every 30 min)")


def _remove_job():
    if scheduler.get_job(JOB_ID):
        scheduler.remove_job(JOB_ID)
        logger.info("Scheduled scraping disabled")


def set_enabled(enabled):
    db.set_setting("scheduler_enabled", "true" if enabled else "false")
    if enabled:
        _add_job()
    else:
        _remove_job()


def is_enabled():
    return scheduler.get_job(JOB_ID) is not None
