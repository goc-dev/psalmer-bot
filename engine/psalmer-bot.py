import asyncio
import logging
import sys
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, Router, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message 

load_dotenv()

PSALMER_BOT_TOKEN = os.getenv("PSALMER_BOT_TOKEN")
# Debug only:#print(f"Bot token: {PSALMER_BOT_TOKEN}")#exit()
# All handlers should be attached to the Router (or Dispatcher)
bot = Bot(token = PSALMER_BOT_TOKEN)
dp = Dispatcher()
router = Router()

@router.message(Command(commands=['start']))
async def handle_command_start(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    tg_user_name = message.from_user.full_name
    s_greating = f"""
Hello, *{tg_user_name}*
Are you looking for any psalm/chords?
"""
    await message.answer(s_greating, parse_mode = "MarkdownV2")


@router.message(Command(commands=["psalm"]))
async def handle_command_psalm(message: Message) -> None:
    """This handler is for the command `/psalm #id to print text/chords of Psalm#id"""

    v_book_dir = '../hymnal/goc-2021/'
    v_song_id  = 66
    v_song_idx = str(v_song_id)
    v_song_file = ''

    # Iterate through files in the directory and find matching prefix
    for filename in os.listdir(v_book_dir):
        if filename.startswith(v_song_idx):
            v_song_file = filename
            break

    if '' == v_song_file:
        v_song_text_md = 'File not found'
    else:
        with open( v_song_file, 'r') as song_file:
            v_song_text_md = song_file.read()

    await message.answer(v_song_text_md, parse_mode = "Markdown")


@router.message()
async def handle_non_command(message: Message) -> None:
    """
    Handler of all non-command messages, it forward the received message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    if not message.text or message.text.startswith("/"):
        return  # Ignore commands or empty messages
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")



dp.include_router(router)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())