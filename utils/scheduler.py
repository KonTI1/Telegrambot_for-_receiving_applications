from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sheets.table import clear_old_appointments
from loguru import logger

async def setup_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(clear_old_appointments, "interval", minutes=1)
    scheduler.start()
    logger.debug("Scheduler started")
