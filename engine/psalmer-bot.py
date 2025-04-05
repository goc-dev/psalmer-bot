import asyncio
import logging
import sys
from os import getenv
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, Router, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message 

load_dotenv()

PSALMER_BOT_TOKEN = getenv("PSALMER_BOT_TOKEN")
# Debug only:#print(f"Bot token: {PSALMER_BOT_TOKEN}")#exit()
# All handlers should be attached to the Router (or Dispatcher)
bot = Bot(token = PSALMER_BOT_TOKEN)
dp = Dispatcher()
router = Router()

# @dp.message(CommandStart())
@router.message(commands=["start"])
async def handle_command_start(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}! Are you looking for some psalm/chords?")


#@dp.message_handler(commands = ["psalm"])
@router.message(commands=["psalm"])
async def handle_command_psalm(message: Message) -> None:
    """This handler is for the command `/psalm #id to print text/chords of Psalm#id"""

    s_answer = """
**WARNING**: This is stub (yet)

```Some text, some text
Next text, Next text
```
"""
    message.reply(s_answer, parse_mode = "Markdown")


@dp.message()
async def echo_handler(message: Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        # Send a copy of the received message
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")


dp.include_router(router)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())