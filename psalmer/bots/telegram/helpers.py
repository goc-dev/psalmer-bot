import logging
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardBuilder
from bots.utils.markdown import MarkdownV2 as MD_V2
from hymnal.catalog import HymnalLib

logger = logging.getLogger('psalmer-bot')

def get_main_menu_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="/list"), KeyboardButton(text="/help")],
            [KeyboardButton(text="/sett"), KeyboardButton(text="/version")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )

async def send_markdown_message(message, text, reply_markup=None, escape_md=True):
    v_text = MD_V2.escape_text(text) if escape_md else text
    await message.answer(v_text, parse_mode="MarkdownV2", reply_markup=reply_markup)

async def find_and_send_psalm(message, hymn_id, hymnal_id=1):
    """Send psalm text for given hymn_id (default hymnal_id=1)"""
    v_hymn_text_md = HymnalLib.hymn_text(hymnal_id, hymn_id)
    await send_markdown_message(message, v_hymn_text_md)

def get_hymnal_keyboard():
    hymnals = HymnalLib.hymnal_list()
    bldr = InlineKeyboardBuilder()
    for hymnal_meta in hymnals:
        bldr.row(InlineKeyboardButton(text=hymnal_meta.title, callback_data=f"hymnal:{hymnal_meta.id}"))
    return bldr.as_markup()

def chunked(seq, n):
    """Yield successive n-sized chunks from seq."""
    for i in range(0, len(seq), n):
        yield seq[i:i + n]