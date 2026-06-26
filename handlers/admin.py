import asyncio

from telegram import Update
from telegram.ext import ContextTypes

from config import DELETE_MENU_AFTER
from services.auth import is_admin
from services.keyboard import bank_menu


async def delete_later(message):
    try:
        await asyncio.sleep(DELETE_MENU_AFTER)
        await message.delete()
    except Exception:
        pass


async def ql(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        return

    msg = await update.message.reply_text(
        "🏦 Chọn ngân hàng:",
        reply_markup=bank_menu(0)
    )

    context.application.create_task(
        delete_later(msg)
    )