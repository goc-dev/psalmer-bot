import asyncio
import logging
import sys
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, Router, html
from aiogram.filters import Command
from aiogram.types import Message as TgMessage, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
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


def get_main_menu_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="/list"), KeyboardButton(text="/help")],
            [KeyboardButton(text="/sett"), KeyboardButton(text="/version")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )

@router.startup()
async def bot_startup():
    await HymnalLib.init_async( HYMNAL_HOME_DIR)
    FileHymnFinder.set_home_path( HYMNAL_HOME_DIR)
    print("PsalmerBot is started!")

async def send_markdown_message( message: TgMessage, text: str, reply_markup:ReplyKeyboardMarkup|None = None):
    #v_escaped_md = MD_V2.escape_text( text)
    v_escaped_md = text
    await message.answer( v_escaped_md, parse_mode = "MarkdownV2", reply_markup=reply_markup)


@router.message(Command(commands=['start']))
async def handle_command_start(message: TgMessage) -> None:
    """
    This handler receives messages with `/start` command
    """
    tg_user_name = message.from_user.full_name
    s_greeting   = UtilMessage.hello_user( tg_user_name)
    v_main_kbd   = get_main_menu_keyboard()
    await send_markdown_message( message, s_greeting, v_main_kbd)
    #await message.answer( s_greeting, reply_markup=v_main_kbd, parse_node="MarkdownV2")

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
    for hymnal_meta in hymnals:
        bldr.row( InlineKeyboardButton( text=hymnal_meta.title, callback_data=f"hymnal:{hymnal_meta.id}"))
    return bldr.as_markup()


@router.message(Command(commands=["list"]))
async def handle_command_list(message: TgMessage) -> None:
    v_msg = "Choose a hymnal:"
    v_kbd = get_hymnal_keyboard()
    await message.answer( v_msg, reply_markup=v_kbd)


#--- Data format: "hymnal:ID"
# TODO: path: hymnal-list -> letters-index -> hymn-list -> hymn-text
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

@dp.callback_query(lambda c: c.data.startswith('hymnal:'))
async def process_hymnal_selection(callback_query: CallbackQuery):
    hymnal_id_str = callback_query.data.split(':')[1]
    print(f"DBG: [hymnal_id:{hymnal_id_str}]")

    try:
        hymnal_id = int(hymnal_id_str)
        hymnal_meta: HymnalMeta = HymnalLib.hymnal_meta(hymnal_id)
        hymn_range_list = HymnalLib.range_list(hymnal_id)
        v_msg = f"{hymnal_meta.title}"

        # ✨ Create all buttons first
        range_buttons = [
            InlineKeyboardButton(
                text=f"{hr.starting_prefix}...{hr.ending_prefix}",
                callback_data=f"hymnrange:{hymnal_id}:{hr.id}"
            )
            for hr in hymn_range_list
        ]

        # 🔁 Chunk into groups of 3 per row
        def chunked(seq, n):
            for i in range(0, len(seq), n):
                yield seq[i:i + n]

        v_bldr = InlineKeyboardBuilder()
        for group in chunked(range_buttons, 3):
            v_bldr.row(*group)

        v_kbd = v_bldr.as_markup()
        await callback_query.message.answer(v_msg, reply_markup=v_kbd)
        await callback_query.answer()

    except ValueError as e:
        print(f"Error: Bad Hymnal ID: {hymnal_id_str}")



#--- Data format: "hymnrange:HYMNAL_ID:RANGE_ID"
@dp.callback_query(lambda c: c.data.startswith('hymnrange:'))
async def process_range_selection(callback_query: CallbackQuery):
    _, s_hymnal_id, s_range_id = callback_query.data.split(':')
    logger.debug(f'Data:{s_hymnal_id}:{s_range_id}')
    v_bldr = InlineKeyboardBuilder()

    try:
        hymnal_id = int( s_hymnal_id)
        range_id = int( s_range_id)
        
        hymnal_meta:HymnalMeta = HymnalLib.hymnal_meta(hymnal_id)
        range_meta:RangeMeta = HymnalLib.range_meta(hymnal_id, range_id)

        hymn_list = HymnalLib.hymnal_index( hymnal_id, range_id)

        v_msg = f"{hymnal_meta.title} ({range_meta.starting_prefix}...{range_meta.ending_prefix})"
        for hymn in hymn_list:
            v_bldr.row( InlineKeyboardButton( text=hymn.title, callback_data=f"hymn:{hymnal_id}:{hymn.id}"))

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
    s_version = "*Version*: `1.0.2025-0808-1012`"
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