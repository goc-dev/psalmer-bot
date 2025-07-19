import asyncio
import logging
import sys
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, Router, html
from aiogram.filters import Command
from aiogram.types import Message as TgMessage, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bots.utils.messages import Message as UtilMessage
from hymnal.finder import FileHymnFinder
from hymnal.catalog import HymnalLib

load_dotenv()

PSALMER_BOT_TOKEN = os.getenv("PSALMER_BOT_TOKEN")
HYMNAL_HOME_DIR   = os.getenv("HYMNAL_HOME_DIR")

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger('psalmer-bot')

# All handlers should be attached to the Router (or Dispatcher)
bot = Bot(token = PSALMER_BOT_TOKEN)
dp = Dispatcher()
router = Router()

@router.startup()
async def bot_startup():
    await HymnalLib.init( HYMNAL_HOME_DIR)
    FileHymnFinder.set_home_path( HYMNAL_HOME_DIR)
    print("PsalmerBot is started!")

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

#------- PSALM (FIND) -------
async def find_and_send_psalm( message: TgMessage, i_hymnal_id: int, i_hymn_id: int) -> None:
    v_hymn_text_md = HymnalLib.hymn_text(i_hymnal_id, i_hymn_id)
    await send_markdown_message( message, v_hymn_text_md)


@router.message(Command(commands=["psalm"]))
async def handle_command_psalm(message: TgMessage) -> None:
    """This handler is for the command `/psalm #id to print text/chords of Psalm#id"""

    args = message.text.split(maxsplit = 1)
    
    v_hymn_id = int(args[1]) \
        if len(args) > 1 and args[1].isdigit() \
        else None

    await find_and_send_psalm( message, v_hymn_id)


@router.message(lambda msg: msg.text and msg.text.isdigit())
async def handler_int(message: TgMessage):
    v_hymn_id = int(message.text)
    await find_and_send_psalm(message, v_hymn_id)


#------------- LIST ----------
def get_hymnal_keyboard():
    hymnals = HymnalLib.hymnal_list()
    bldr = InlineKeyboardBuilder()
    for hymnal in hymnals:
        bldr.row( InlineKeyboardButton( text=hymnal.title, callback_data=f"hymnal:{hymnal.id}"))
    return bldr.as_markup()


@router.message(Command(commands=["list"]))
async def handle_command_list(message: TgMessage) -> None:
    v_msg = "Choose a hymnal:"
    v_kbd = get_hymnal_keyboard()
    await message.answer( v_msg, reply_markup=v_kbd)

#--- "hymnal:ID"
#--- Data format: "hymnal:ID"
@dp.callback_query(lambda c: c.data.startswith('hymnal:'))
async def process_hymnal_selection(callback_query: CallbackQuery):
    s_id = callback_query.data.split(':')[1]
    print(f"DBG: [s_id:{s_id}]")
    v_bldr = InlineKeyboardBuilder()

    try:
        hymnal_id = int( s_id)
        hymnal_list = HymnalLib.hymnal_list( hymnal_id)
        hymnal = hymnal_list[0]
        hymn_list = HymnalLib.hymnal_index( hymnal_id)

        v_msg = f"{hymnal.title}"
        for hymn in hymn_list:
            title = f'{hymn.title}' # ...' ({hymn.id}: {hymn.fmt})'
            v_bldr.row( InlineKeyboardButton( text=title, callback_data=f"hymn:{hymnal_id}:{hymn.id}"))

        v_kbd = v_bldr.as_markup()
        await callback_query.message.answer(v_msg, reply_markup=v_kbd)
        await callback_query.answer()
    except ValueError as e:
        print(f"Error: Bad Hymnal ID: {s_id}")

#--- "hymn:ID"
#--- format: "hymn:HYMNAL_ID:HYMN_ID"
@dp.callback_query(lambda c: c.data.startswith('hymn:'))
async def process_hymn_selection(callback_query: CallbackQuery):
    _, s_hymnal_id, s_hymn_id = callback_query.data.split(':')
    logger.debug( f'Data:{s_hymnal_id}:{s_hymn_id}')
    v_hymnal_id = int(s_hymnal_id)
    v_hymn_id   = int(s_hymn_id)
    v_hymn_md = HymnalLib.hymn_text( v_hymnal_id, v_hymn_id)

    await callback_query.message.answer(v_hymn_md, parse_mode="MarkdownV2")
    await callback_query.answer()

#------- HELP,INFO -----
@router.message(Command(commands=["help", "info"]))
async def handle_command_help(message: TgMessage) -> None:
    s_info = UtilMessage.help_info()
    print(f'DBG:help-msg:{s_info}')
    await send_markdown_message( message, s_info)


@router.message(Command(commands=['settings','sett']))
async def handle_command_sett(message: TgMessage) -> None:
    s_sett = "Settings: _nothing set yet_"
    await send_markdown_message( message, s_sett)

@router.message(Command(commands=['version']))
async def handle_command_version(message: TgMessage) -> None:
    s_version = "*Version*: `0.1.2025-0522-0900`"
    await send_markdown_message( message, s_version)


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
    logger.info("Bot is starting...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())