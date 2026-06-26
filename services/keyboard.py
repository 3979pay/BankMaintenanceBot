from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from banks import BANKS
from config import PAGE_SIZE


def bank_menu(page=0):
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


def action_menu(bank, page):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🔴 Bảo trì",
                callback_data=f"act:maintenance:{page}:{bank}"
            ),
            InlineKeyboardButton(
                "🟢 Hoạt động lại",
                callback_data=f"act:online:{page}:{bank}"
            ),
        ],
        [
            InlineKeyboardButton(
                "⚠️ Lỗi chuyển khoản",
                callback_data=f"act:transfer:{page}:{bank}"
            ),
            InlineKeyboardButton(
                "📱 Lỗi QR",
                callback_data=f"act:qr:{page}:{bank}"
            ),
        ],
        [
            InlineKeyboardButton(
                "⬅️ Quay lại",
                callback_data=f"page:{page}"
            )
        ],
    ])