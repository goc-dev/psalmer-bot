import logging
from aiogram import Router, html
from aiogram.filters import Command
from aiogram.types import Message as TgMessage, CallbackQuery
from bots.utils.messages import Message as UtilMessage
from bots.utils.markdown import MarkdownV2 as MD_V2
from hymnal.catalog import HymnalLib
from .helpers import (
    get_main_menu_keyboard,
    send_markdown_message,
    find_and_send_psalm,
    get_hymnal_keyboard,
)

logger = logging.getLogger('psalmer-bot')

command_router = Router()

@command_router.message(Command(commands=['start']))
async def handle_command_start(message: TgMessage) -> None:
    """
    This handler receives messages with `/start` command
    """
    tg_user_name = message.from_user.full_name
    tg_user_name = MD_V2.escape_text(tg_user_name)
    s_greeting = UtilMessage.hello_user(tg_user_name)
    v_main_kbd = get_main_menu_keyboard()
    await send_markdown_message(message, s_greeting, v_main_kbd, escape_md=False)

@command_router.message(Command(commands=["psalm"]))
async def handle_command_psalm(message: TgMessage) -> None:
    """This handler is for the command `/psalm #id to print text/chords of Psalm#id"""
    args = message.text.split(maxsplit=1)
    v_hymn_id = int(args[1]) if len(args) > 1 and args[1].isdigit() else None
    await find_and_send_psalm(message, v_hymn_id)

@command_router.message(lambda msg: msg.text and msg.text.isdigit())
async def handler_int(message: TgMessage):
    v_hymn_id = int(message.text)
    await find_and_send_psalm(message, v_hymn_id)

@command_router.message(Command(commands=["list"]))
async def handle_command_list(message: TgMessage) -> None:
    v_msg = "Choose a hymnal:"
    v_kbd = get_hymnal_keyboard()
    await message.answer(v_msg, reply_markup=v_kbd)

@command_router.message(Command(commands=["help", "info"]))
async def handle_command_help(message: TgMessage) -> None:
    s_info = UtilMessage.help_info()
    print(f'DBG:help-msg:{s_info}')
    await send_markdown_message(message, s_info, escape_md=False)

@command_router.message(Command(commands=['settings', 'sett']))
async def handle_command_sett(message: TgMessage) -> None:
    s_sett = UtilMessage.setting_info()
    await send_markdown_message(message, s_sett, escape_md=False)

@command_router.message(Command(commands=['version']))
async def handle_command_version(message: TgMessage) -> None:
    s_version = UtilMessage.version_info()
    await send_markdown_message(message, s_version, escape_md=False)

@command_router.message()
async def handle_non_command(message: TgMessage) -> None:
    """
    Handler of all non-command messages, it forward the received message back to the sender
    """
    if not message.text or message.text.startswith("/"):
        return  # Ignore commands or empty messages
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer(f"ERROR: unknown command: {message.text}")