import asyncio
import logging
import sys
import os
from pathlib import Path

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, Router, html
from aiogram.filters import Command
from aiogram.types import \
    Message as TgMessage, CallbackQuery, \
    InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bots.utils.messages import Message as UtilMessage
from bots.utils.markdown import MarkdownV2 as MD_V2
from hymnal.finder import FileHymnFinder
from hymnal.catalog import HymnalLib

# Import routers from sub-files
from .commands import command_router
from .callbacks import callback_router

load_dotenv()

PSALMER_BOT_TOKEN = os.getenv("API_TOKEN")
HYMNAL_HOME_DIR   = Path( os.getenv("HYMNAL_HOME_DIR") ).resolve()
HYMNAL_MDV2_DIR   = Path( os.getenv("HYMNAL_MDV2_DIR") ).resolve()

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger('psalmer-bot')

# All handlers should be attached to the Router (or Dispatcher)
bot = Bot(token = PSALMER_BOT_TOKEN)
dp = Dispatcher()
router = Router()

@router.startup()
async def bot_startup():
    await HymnalLib.init_async( HYMNAL_HOME_DIR)
    FileHymnFinder.set_home_path( HYMNAL_HOME_DIR)
    print("PsalmerBot is started!")

# Include sub-routers
router.include_router(command_router)
router.include_router(callback_router)

dp.include_router(router)

async def main():
    logger.info("Bot is starting...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())