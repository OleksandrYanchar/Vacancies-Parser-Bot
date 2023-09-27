import asyncio
import csv
import threading
from aiogram import Bot, Dispatcher, types, F
from src.configs.settings import TOKEN, IDS, csv_filename, bot, dp
from src.bot.tasks import thread


# clears csv file
async def clear_file():
    with open(csv_filename, mode="w", encoding="utf-8") as file:
        file.truncate(0)


# reads csv file
async def read_csv():
    try:
        with open(csv_filename, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            data = list(reader)
        return data
    except Exception as e:
        print(f"Помилка при обробці CSV файлу: {str(e)}")
        return []


# sends date fron csv file to admins
async def send_messages():
    data = await read_csv()
    if not data:
        return

    # values for sending message
    max_items_per_message = 10  # max amount of vacancies in one message
    current_items = 0
    message_text = ""

    for row in data:
        title = row.get("vacancy_title", "")
        link = row.get("vacancy_link", "")

        message_text += f"{title} - {link}\n"
        current_items += 1

        if current_items >= max_items_per_message:
            for chat_id in IDS:
                try:
                    await bot.send_message(chat_id, text=message_text)
                    print(f"Частина повідомлення відправлена в чат з ID: {chat_id}")
                    await asyncio.sleep(1)
                except Exception as e:
                    print(
                        f"Помилка відправлення повідомлення в чат з ID {chat_id}: {str(e)}"
                    )

            current_items = 0
            message_text = ""

    if message_text.strip():
        for chat_id in IDS:
            try:
                await bot.send_message(chat_id, text=message_text)
                print(f"rest of messages were sent to chat: {chat_id}")
                await asyncio.sleep(1)
            except Exception as e:
                print(f"EROR of sennding rest of messages to chat {chat_id}: {str(e)}")


# handles /start command to get users ID
@dp.message(F.text == "/start")
async def lol(message: types.Message):
    await message.answer(str(message.from_user.id))


# handles /scrap command to start scrapind websites and sends date to user
@dp.message(F.text == "/scrap")
async def scrap(message: types.Message):
    await bot_tasks()


# creates tasks and order for scraping
async def bot_tasks():
    await thread()
    await read_csv()
    await send_messages()
    await clear_file()


# main function to start poling bot
async def bot_main():
    await dp.start_polling(bot, skip_updates=True)


# function for celery task which executes at specifed time and than stops bot
async def bot_schedule():
    await bot_tasks()
    await dp.stop_polling(bot)
    await dp.start_polling(bot, skip_updates=True)
