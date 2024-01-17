from pathlib import Path

from dotenv import load_dotenv
from envparse import env

load_dotenv(env('DOTENV_FILE', default=None))

BASE_DIR = Path(__file__).resolve().parent.parent

# bot_app
TELEGRAM_CONTACT_EMAIL = env('TELEGRAM_CONTACT_EMAIL')
TELEGRAM_CONTACT_USERNAME = env('TELEGRAM_CONTACT_USERNAME')
TELEGRAM_TOKEN = env('TELEGRAM_TOKEN')


POSTGRES_USER = env('POSTGRES_USER')
POSTGRES_PASSWORD = env('POSTGRES_PASSWORD')
DB_HOST = env('DB_HOST')
DB_PORT = env('DB_PORT')
POSTGRES_DB = env('POSTGRES_DB')
