import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

PAGE_SIZE = 10

DELETE_MENU_AFTER = 20

LOGO_FOLDER = "logos"

DATABASE = os.path.join("data", "bot.db")