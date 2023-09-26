import asyncio
import csv
import threading
from aiogram import Bot, Dispatcher, types, F
from src.configs.settings import TOKEN, IDS, csv_filename
from src.bot.tasks import thread

bot = Bot(token= TOKEN )
dp = Dispatcher()

async def clear_file():
    with open(csv_filename, mode='w', encoding='utf-8') as file:
        file.truncate(0)

async def read_csv():
    try:
        with open(csv_filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            data = list(reader)
        return data
    except Exception as e:
        print(f"Помилка при обробці CSV файлу: {str(e)}")
        return []

# Функція для відправки повідомлень
async def send_messages():
    data = await read_csv()  # Очікуємо завершення функції read_csv()
    if not data:
        return

    # Ініціалізуємо змінні для обмеження кількості тайтлів і посилань в одному повідомленні
    max_items_per_message = 10
    current_items = 0
    message_text = ""

    for row in data:
        title = row.get('vacancy_title', '')
        link = row.get('vacancy_link', '')

        # Додаємо тайтл і посилання до поточного повідомлення
        message_text += f"{title} - {link}\n"
        current_items += 1

        # Якщо досягнуто обмеження, надсилаємо повідомлення та очищуємо змінну
        if current_items >= max_items_per_message:
            for chat_id in IDS:
                try:
                    await bot.send_message(chat_id, text=message_text)
                    print(f"Частина повідомлення відправлена в чат з ID: {chat_id}")
                    await asyncio.sleep(1)
                except Exception as e:
                    print(f"Помилка відправлення повідомлення в чат з ID {chat_id}: {str(e)}")

            # Очищуємо змінну для нових тайтлів і посилань
            current_items = 0
            message_text = ""

    if message_text.strip():
        for chat_id in IDS:
            try:
                await bot.send_message(chat_id, text=message_text)
                print(f"Залишок повідомлення відправлений в чат з ID: {chat_id}")
                await asyncio.sleep(1)
            except Exception as e:
                print(f"Помилка відправлення залишку повідомлення в чат з ID {chat_id}: {str(e)}")

@dp.message(F.text =='/start')
async def lol(message: types.Message):
    await message.answer('aga')
    await thread()
    await read_csv()  
    await send_messages()
    await clear_file()


async def main():
    await dp.start_polling(bot)

