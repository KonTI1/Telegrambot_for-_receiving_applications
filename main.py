import asyncio
import sys

from loguru import logger
from os import environ

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from core.config import Settings
from core.router_manager import setup_router
from middlewares.logger import LoggerMiddleware
from utils.scheduler import setup_scheduler

async def main(): 
    logger.add(sys.stderr, format="{time} {level} {message}", filter ="template", level="INFO")
    
    environ["TZ"] = "Europe/Ekaterinburg"
    logger.debug("Starting bot...")
    config = Settings()
    router = setup_router()
    await setup_scheduler()
    
    bot = Bot(token=config.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    
    bot_info = await bot.get_me()
    
    dp = Dispatcher(config=config, bot_info=bot_info)
    dp.include_routers(router)
    
    dp.update.outer_middleware(LoggerMiddleware())
    
    try:
        logger.debug(f'Bot {bot_info.full_name} started (@{bot_info.username}. ID: {bot_info.id})')
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

def cli():
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")


if __name__ == '__main__':
    cli()
