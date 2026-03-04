import logging
from aiogram import Router
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardBuilder
from hymnal.catalog import HymnalLib
from hymnal.meta import HymnalMeta, RangeMeta
from .helpers import chunked

logger = logging.getLogger('psalmer-bot')

callback_router = Router()

@callback_router.callback_query(lambda c: c.data.startswith('hymnal:'))
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
                text=hr.label if hr.label else f"{hr.starting_prefix}...{hr.ending_prefix}",
                callback_data=f"hymnrange:{hymnal_id}:{hr.id}"
            )
            for hr in hymn_range_list
        ]

        v_bldr = InlineKeyboardBuilder()
        for group in chunked(range_buttons, 3):
            v_bldr.row(*group)

        v_kbd = v_bldr.as_markup()
        await callback_query.message.answer(v_msg, reply_markup=v_kbd)
        await callback_query.answer()

    except ValueError as e:
        print(f"Error: Bad Hymnal ID: {hymnal_id_str}")

@callback_router.callback_query(lambda c: c.data.startswith('hymnrange:'))
async def process_range_selection(callback_query: CallbackQuery):
    _, s_hymnal_id, s_range_id = callback_query.data.split(':')
    logger.debug(f'Data:{s_hymnal_id}:{s_range_id}')
    v_bldr = InlineKeyboardBuilder()

    try:
        hymnal_id = int(s_hymnal_id)
        range_id = int(s_range_id)

        hymnal_meta: HymnalMeta = HymnalLib.hymnal_meta(hymnal_id)
        range_meta: RangeMeta = HymnalLib.range_meta(hymnal_id, range_id)

        hymn_list = HymnalLib.hymnal_index(hymnal_id, range_id)

        v_range_label = range_meta.label if range_meta.label else f'{range_meta.starting_prefix}...{range_meta.ending_prefix}'

        v_msg = f"{hymnal_meta.title} ({v_range_label})"

        for hymn in hymn_list:
            v_bldr.row(InlineKeyboardButton(text=hymn.title, callback_data=f"hymn:{hymnal_id}:{hymn.id}"))

        v_kbd = v_bldr.as_markup()
        await callback_query.message.answer(v_msg, reply_markup=v_kbd)
        await callback_query.answer()
    except ValueError as e:
        print(f"Error: Bad Hymnal ID: {s_hymnal_id}")

@callback_router.callback_query(lambda c: c.data.startswith('hymn:'))
async def process_hymn_selection(callback_query: CallbackQuery):
    _, s_hymnal_id, s_hymn_id = callback_query.data.split(':')
    logger.debug(f'Data:{s_hymnal_id}:{s_hymn_id}')
    v_hymnal_id = int(s_hymnal_id)
    v_hymn_id = int(s_hymn_id)
    v_hymn_md = HymnalLib.hymn_text(v_hymnal_id, v_hymn_id)

    await callback_query.message.answer(v_hymn_md, parse_mode="MarkdownV2")
    await callback_query.answer()