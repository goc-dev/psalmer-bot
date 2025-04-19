import asyncio
import logging
import sys
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, Router, html
from aiogram.filters import CommandStart, Command
from aiogram.types import Message as TgMessage, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bots.utils.messages import Message as UtilMessage
from hymnal.finder import FileHymnFinder
from hymnal.catalog import HymnalLib

load_dotenv()

PSALMER_BOT_TOKEN = os.getenv("PSALMER_BOT_TOKEN")
HYMNAL_HOME_DIR = os.getenv("HYMNAL_HOME_DIR")

# All handlers should be attached to the Router (or Dispatcher)
bot = Bot(token = PSALMER_BOT_TOKEN)
dp = Dispatcher()
router = Router()

@router.startup()
async def bot_startup():
    await HymnalLib.init()
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


#------------- LIST ----------
def get_hymnal_keyboard():
    hymnals = HymnalLib.hymnal_list()
    bldr = InlineKeyboardBuilder()
    for hymnal in hymnals:
        bldr.row( InlineKeyboardButton( text=hymnal['title'], callback_data=f"hymnal:{hymnal['id']}"))
    return bldr.as_markup()


@router.message(Command(commands=["list"]))
async def handle_command_list(message: TgMessage) -> None:
    v_msg = "Choose a hymnal:"
    v_kbd = get_hymnal_keyboard()
    await message.answer( v_msg, reply_markup=v_kbd)

#--- "hymnal:ID"
@dp.callback_query(lambda c: c.data.startswith('hymnal:'))
async def process_hymnal_selection(callback_query: CallbackQuery):
    s_id = callback_query.data.split(':')[1]
    print(f"DBG: [s_id:{s_id}]")
    v_bldr = InlineKeyboardBuilder()

    try:
        hymnal_id = int( s_id)    
        hymn_list = HymnalLib.hymnal_content( hymnal_id)

        v_msg = f"Hymnal: {s_id}"
        for hymn in hymn_list:
            v_bldr.row( InlineKeyboardButton( text=hymn['title'], callback_data=f"hymn:{hymn['id']}"))
            #v_msg += f"\n\- {hymn['title']}" 

        v_kbd = v_bldr.as_markup()
        await callback_query.message.answer(v_msg, reply_markup=v_kbd)
        await callback_query.answer()
    except ValueError as e:
        print(f"Error: Bad Hymnal ID: {s_id}")

#--- "hymn:ID"
@dp.callback_query(lambda c: c.data.startswith('hymn:'))
async def process_hymn_selection(callback_query: CallbackQuery):
    s_id = callback_query.data.split(':')[1]
    v_msg = f"Hymn Content: {s_id}"
    await callback_query.message.answer(v_msg)
    await callback_query.answer()

#------- HELP,INFO -----
@router.message(Command(commands=["help", "info"]))
async def handle_command_help(message: TgMessage) -> None:
    s_info = UtilMessage.help_info()
    await send_markdown_message( message, s_info)


@router.message(Command(commands=['settings','sett']))
async def handle_command_sett(message: TgMessage) -> None:
    s_sett = "Settings: _nothing set yet_"
    await send_markdown_message( message, s_sett)

@router.message(Command(commands=['version']))
async def handle_command_version(message: TgMessage) -> None:
    s_version = "*Version*: `0.1.2025-0419-1940`"
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
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())