import os
import asyncio
from dotenv import load_dotenv

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

from banks import BANKS

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

LOGO_DIR = "logos"
PAGE_SIZE = 10
DELETE_MENU_AFTER = 20


def build_bank_menu(page=0):
    start = page * PAGE_SIZE
    end = start + PAGE_SIZE
    banks_page = BANKS[start:end]

    rows = []

    for i in range(0, len(banks_page), 2):
        row = []
        for bank_name, _ in banks_page[i:i + 2]:
            row.append(
                InlineKeyboardButton(
                    bank_name,
                    callback_data=f"bank:{page}:{bank_name}"
                )
            )
        rows.append(row)

    nav = []

    if page > 0:
        nav.append(
            InlineKeyboardButton(
                "⬅️ Trang trước",
                callback_data=f"page:{page - 1}"
            )
        )

    if end < len(BANKS):
        nav.append(
            InlineKeyboardButton(
                "Trang sau ➡️",
                callback_data=f"page:{page + 1}"
            )
        )

    if nav:
        rows.append(nav)

    return InlineKeyboardMarkup(rows)


def build_action_menu(bank_name, page):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🔴 Bảo trì",
                callback_data=f"act:maintenance:{page}:{bank_name}"
            ),
            InlineKeyboardButton(
                "🟢 Hoạt động lại",
                callback_data=f"act:online:{page}:{bank_name}"
            ),
        ],
        [
            InlineKeyboardButton(
                "⚠️ Lỗi chuyển khoản",
                callback_data=f"act:transfer_error:{page}:{bank_name}"
            ),
            InlineKeyboardButton(
                "📱 Lỗi QR",
                callback_data=f"act:qr_error:{page}:{bank_name}"
            ),
        ],
        [
            InlineKeyboardButton(
                "⬅️ Quay lại",
                callback_data=f"page:{page}"
            )
        ],
    ])


def get_logo_path(bank_name):
    bank_name = bank_name.strip().lower()
    base = os.path.dirname(os.path.abspath(__file__))

    for name, logo_file in BANKS:
        if name.strip().lower() == bank_name:
            path = os.path.join(base, LOGO_DIR, logo_file)
            if os.path.exists(path):
                return path

    return None


def message_text(bank_name, action):
    if action == "maintenance":
        return (
            f"<b>Ngân hàng {bank_name}</b> bảo trì.\n\n"
            "Trong quá trình bảo trì, vui lòng không tiến hành chuyển khoản "
            "để tránh trường hợp treo đơn.\n\n"
            "Xin cảm ơn!"
        )

    if action == "online":
        return (
            f"🏦 Ngân hàng <b>{bank_name}</b>\n\n"
            "✅ <b>HOÀN TẤT BẢO TRÌ</b>"
        )

    if action == "transfer_error":
        return (
            f"<b>Ngân hàng {bank_name}</b> đang gặp lỗi chuyển khoản.\n\n"
            "Vui lòng tạm thời không thực hiện giao dịch "
            "để tránh phát sinh treo đơn.\n\n"
            "Xin cảm ơn!"
        )

    if action == "qr_error":
        return (
            f"<b>Ngân hàng {bank_name}</b> đang gặp lỗi QR.\n\n"
            "Vui lòng kiểm tra kỹ thông tin trước khi giao dịch "
            "hoặc thử lại sau.\n\n"
            "Xin cảm ơn!"
        )

    return f"<b>Ngân hàng {bank_name}</b> có thông báo mới."


async def safe_delete_message(message, delay=0):
    try:
        if delay > 0:
            await asyncio.sleep(delay)
        await message.delete()
    except Exception:
        pass


async def is_group_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    try:
        member = await context.bot.get_chat_member(chat_id, user_id)
        return member.status in ["administrator", "creator"]
    except Exception:
        return False


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hệ thống thông báo ngân hàng.\n\n"
        "Lệnh quản lý dành cho admin: /ql"
    )


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_group_admin(update, context):
        return

    msg = await update.message.reply_text(
        "🏦 Chọn ngân hàng:",
        reply_markup=build_bank_menu(0)
    )

    context.application.create_task(
        safe_delete_message(msg, DELETE_MENU_AFTER)
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if not await is_group_admin(update, context):
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
                reply_markup=build_bank_menu(page)
            )
        except Exception:
            return

        return

    if data.startswith("bank:"):
        _, page, bank_name = data.split(":", 2)

        try:
            await query.message.edit_text(
                f"Bạn đã chọn: <b>{bank_name}</b>\n\n"
                "Chọn loại thông báo:",
                reply_markup=build_action_menu(bank_name, page),
                parse_mode="HTML"
            )
        except Exception:
            return

        context.application.create_task(
            safe_delete_message(query.message, DELETE_MENU_AFTER)
        )
        return

    if data.startswith("act:"):
        _, action, page, bank_name = data.split(":", 3)

        chat_id = query.message.chat_id
        text = message_text(bank_name, action)
        logo_path = get_logo_path(bank_name)

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

        if logo_path:
            with open(logo_path, "rb") as photo:
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


def main():
    if not TOKEN:
        print("Thiếu TELEGRAM_BOT_TOKEN trong file .env")
        return

    app = (
        ApplicationBuilder()
        .token(TOKEN)
        .connection_pool_size(20)
        .connect_timeout(10)
        .read_timeout(10)
        .write_timeout(10)
        .pool_timeout(10)
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ql", menu))
    app.add_handler(CallbackQueryHandler(button))

    print("Bot đang chạy...")
    app.run_polling(poll_interval=0.1)


if __name__ == "__main__":
    main()
