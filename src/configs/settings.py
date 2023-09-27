from os import getenv
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from typing import List, Optional

load_dotenv()

# gets telegram bot TOKEN from .env file
TOKEN = getenv("TOKEN")

# gets telegram bot admins's IDS from .env file
env_admins_ID = getenv("IDs")
IDS: List[int] = [int(id) for id in (env_admins_ID or "").split(",") if id.strip()]

# Initializate bot and dp
bot = Bot(token=TOKEN)
dp = Dispatcher()

# urls for different sites to parse
jobs_url = "https://jobs.dou.ua/vacancies/?category=Python"
jooble_url = "https://ua.jooble.org/SearchResult?ukw=python"
csv_filename = "vacancies.csv"
urls = [
    "https://www.work.ua/jobs-python/",
    "https://www.work.ua/jobs-python+trainee/",
    "https://www.work.ua/jobs-python+junior/",
    "https://www.work.ua/jobs-python+developer/",
    "https://www.work.ua/jobs-django/",
]
# keywords for workua_scraper
key_words = [
    "python",
    "django",
]
# banwords for workua_scraper
ban_words = [
    "middle",
    "senior",
]
