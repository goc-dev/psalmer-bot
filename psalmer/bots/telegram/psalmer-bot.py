import asyncio
import logging
import sys
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, Router, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message as TgMessage

from bots.utils.messages import Message as UtilMessage
from bots.utils.markdown import MarkdownV2 as MD_V2
from hymnal.finder import FileHymnFinder

load_dotenv()

PSALMER_BOT_TOKEN = os.getenv("PSALMER_BOT_TOKEN")
HYMNAL_HOME_DIR = os.getenv("HYMNAL_HOME_DIR")

# All handlers should be attached to the Router (or Dispatcher)
bot = Bot(token = PSALMER_BOT_TOKEN)
dp = Dispatcher()
router = Router()

async def send_markdown_message( message: TgMessage, text: str):
    #v_escaped_md = MD_V2.escape_text( text)
    v_escaped_md = text
    await message.answer( v_escaped_md, parse_mode = "MarkdownV2")


@router.message(Command(commands=['start']))
async def handle_command_start(message: TgMessage) -> None:
    """
    This handler receives messages with `/start` command
    """
    tg_user_name = message.from_user.full_name
    s_greeting = UtilMessage.hello_user( tg_user_name)
    await send_markdown_message( message, s_greeting)


async def find_and_send_psalm( message: TgMessage, i_hymn_id: int) -> None:
    FileHymnFinder.set_home_dir( HYMNAL_HOME_DIR)
    v_hf = FileHymnFinder('goc-2021')
    v_hymn_text_md = v_hf.text_by_id(i_hymn_id)

    await send_markdown_message( message, v_hymn_text_md)



@router.message(Command(commands=["psalm"]))
async def handle_command_psalm(message: TgMessage) -> None:
    """This handler is for the command `/psalm #id to print text/chords of Psalm#id"""

    args = message.text.split(maxsplit = 1)
    
    v_hymn_id = int(args[1]) if len(args) > 1 and args[1].isdigit() else None

    await find_and_send_psalm( message, v_hymn_id)


@router.message(lambda msg: msg.text and msg.text.isdigit())
async def handler_int(message: TgMessage):
    v_hymn_id = int(message.text)
    await find_and_send_psalm(message, v_hymn_id)


@router.message(Command(commands=["help", "info"]))
async def handle_command_help(message: TgMessage) -> None:
    s_info = UtilMessage.help_info()
    await send_markdown_message( message, s_info)


@router.message()
async def handle_non_command(message: TgMessage) -> None:
    """
    Handler of all non-command messages, it forward the received message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    if not message.text or message.text.startswith("/"):
        return  # Ignore commands or empty messages
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer(f"ERROR: unknown command: {message.text}")



dp.include_router(router)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())