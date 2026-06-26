from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
)

from config import TOKEN
from database import init_db

from handlers.start import start
from handlers.admin import ql
from handlers.callback import callback


def main():
    if not TOKEN:
        print("Thiếu TELEGRAM_BOT_TOKEN trong file .env")
        return

    init_db()

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
    app.add_handler(CommandHandler("ql", ql))
    app.add_handler(CallbackQueryHandler(callback))

    print("BankMaintenanceBot V2 đang chạy...")
    app.run_polling(poll_interval=0.1)


if __name__ == "__main__":
    main()