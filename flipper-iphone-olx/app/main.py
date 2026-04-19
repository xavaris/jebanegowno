from __future__ import annotations

import asyncio
import logging
import os
import random
import signal

from aiogram import Bot

from app.config import get_settings
from app.db import Database
from app.logging_setup import setup_logging
from app.services.flipper_service import FlipperService
from app.services.market_baseline_service import MarketBaselineService

logger = logging.getLogger(__name__)


async def continuous_scan(flipper: FlipperService, settings) -> None:
    first_iteration = True

    while True:
        try:
            if first_iteration and settings.STARTUP_SCAN:
                logger.info("Wykonuję startup scan...")
            await flipper.run_scan()
        except Exception:
            logger.exception("Błąd continuous_scan")
        first_iteration = False

        delay = max(15, settings.SCAN_INTERVAL_SECONDS) + random.uniform(0, 6)
        logger.info("Sleep po skanie: %.2fs", delay)
        await asyncio.sleep(delay)


async def continuous_baseline_refresh(baseline_service: MarketBaselineService, settings) -> None:
    while True:
        try:
            await baseline_service.refresh_all_baselines()
        except Exception:
            logger.exception("Błąd continuous_baseline_refresh")
        await asyncio.sleep(max(1, settings.BASELINE_REFRESH_INTERVAL_HOURS) * 3600)


async def main() -> None:
    settings = get_settings()
    db_dir = os.path.dirname(settings.DATABASE_PATH)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)

    setup_logging(settings.LOG_LEVEL)
    logger.info("Start workera...")
    logger.info("CHAT_ID=%s THREAD_ID=%s", settings.CHANNEL_ID, settings.MESSAGE_THREAD_ID)

    db = Database(settings.DATABASE_PATH)
    await db.init()

    bot = Bot(token=settings.TELEGRAM_TOKEN)
    flipper = FlipperService(bot=bot, db=db, settings=settings)
    baseline_service = MarketBaselineService(db=db, settings=settings)

    stop_event = asyncio.Event()

    def _handle_stop(*_) -> None:
        logger.warning("Otrzymano sygnał stop.")
        stop_event.set()

    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, _handle_stop)
        except NotImplementedError:
            signal.signal(sig, lambda *_: stop_event.set())

    tasks = [asyncio.create_task(continuous_scan(flipper, settings))]
    if settings.ENABLE_MARKET_BASELINE_REFRESH:
        tasks.append(asyncio.create_task(continuous_baseline_refresh(baseline_service, settings)))

    try:
        await stop_event.wait()
    finally:
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
