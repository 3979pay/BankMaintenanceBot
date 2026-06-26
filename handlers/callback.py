from telegram import Update
from telegram.ext import ContextTypes

from database import set_status
from services.auth import is_admin
from services.keyboard import bank_menu, action_menu
from services.message import build_message
from services.logo import get_logo


async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    await query.answer()

    if not await is_admin(update, context):
        await query.answer(
            "Bạn không có quyền sử dụng chức năng này.",
            show_alert=True
        )
        return

    data = query.data

    if data.startswith("page:"):
        page = int(data.split(":")[1])

        try:
            await query.message.edit_text(
                "🏦 Chọn ngân hàng:",
                reply_markup=bank_menu(page)
            )
        except Exception:
            pass

        return

    if data.startswith("bank:"):
        _, page, bank = data.split(":", 2)

        try:
            await query.message.edit_text(
                f"Bạn đã chọn: <b>{bank}</b>\n\n"
                "Chọn loại thông báo:",
                reply_markup=action_menu(bank, page),
                parse_mode="HTML"
            )
        except Exception:
            pass

        return

    if data.startswith("act:"):
        _, action, page, bank = data.split(":", 3)

        chat_id = query.message.chat_id
        admin_id = update.effective_user.id

        text = build_message(bank, action)
        logo = get_logo(bank)

        set_status(bank, action, admin_id)

        try:
            await query.message.delete()
        except Exception:
            pass

        if action == "online":
            await context.bot.send_message(
                chat_id=chat_id,
                text=text,
                parse_mode="HTML"
            )
            return

        if logo:
            with open(logo, "rb") as photo:
                await context.bot.send_photo(
                    chat_id=chat_id,
                    photo=photo,
                    caption=text,
                    parse_mode="HTML"
                )
        else:
            await context.bot.send_message(
                chat_id=chat_id,
                text=text,
                parse_mode="HTML"
            )