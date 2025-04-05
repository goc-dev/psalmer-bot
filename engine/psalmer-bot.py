import asyncio
import logging
import sys
from os import getenv
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, Router, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message 

load_dotenv()

PSALMER_BOT_TOKEN = getenv("PSALMER_BOT_TOKEN")
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
    await message.answer(f"Hello, **{message.from_user.full_name}**! Are you looking for some psalm/chords?")


@router.message(Command(commands=["psalm"]))
async def handle_command_psalm(message: Message) -> None:
    """This handler is for the command `/psalm #id to print text/chords of Psalm#id"""

    s_answer = """
Есть победа
```Вступление:
E/H H7 E A E
```
```Куплет:
       A     G7     C#m
Есть по|беда |для ме|ня,
       E     F#7    Hsus H7
Есть по|беда |для те|бя  |
          E       Hm   A       D7
Есть в Кро|ви Свят|ого |Агнца, |
       E/H   H7     E7   A  E
Есть по|беда |для ме|ня. |  |
```
```Припев:
   E   A/H  E         
Мы |по-|--бе|дим, 
   C#/D# G#7  C#m   E7
мы |по---|--бе|дим, |
     A     F#    E/H    C#7 
Крови|ю Свя|того |Агнца |   
F#m  E/H H7  E     A  E
|мы  |по-|бе-|дим. |  |
```
"""
    await message.answer(s_answer, parse_mode = "Markdown")


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