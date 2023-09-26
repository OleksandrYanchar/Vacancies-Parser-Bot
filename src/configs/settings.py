from os import getenv
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from typing import List, Optional

load_dotenv()

TOKEN = getenv("TOKEN")


bot = Bot(token= TOKEN )
dp = Dispatcher()


jobs_url = "https://jobs.dou.ua/vacancies/?category=Python"
jooble_url = 'https://ua.jooble.org/SearchResult?ukw=python%20junior%2Ftranee'
csv_filename = "vacancies.csv"
vacansies_txt = "vacancies.txt"
urls = [
    "https://www.work.ua/jobs-python/",
    "https://www.work.ua/jobs-python+trainee/",
    "https://www.work.ua/jobs-python+junior/",
    "https://www.work.ua/jobs-python+developer/",
    "https://www.work.ua/jobs-django/",
]

key_words = [
    "python",
    "django",
]

ban_words = [
    "middle",
    "senior",
]

env_admins_ID = getenv("IDs")
IDS: List[int] = [int(id) for id in (env_admins_ID or "").split(",") if id.strip()]