import logging
import random
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram import executor
import schedule

from database import Database
from config import TELEGRAM_TOKEN

logging.basicConfig(level=logging.INFO)
logging.getLogger("aiogram").setLevel(logging.DEBUG)

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)
db = Database()


async def send_message(chat_ids):
    try:
        logging.info(f"Attempting to send message to chat_ids: {chat_ids}")

        if not chat_ids:
            logging.info(
                "No chat_ids found in the database. Skipping message sending.")
            return

        with open("text.txt", encoding="utf-8") as file:
            compliments = [line.strip() for line in file]
            random_compliment = random.choice(compliments)

        for chat_id in chat_ids:
            logging.info(f"Sending message to chat_id {chat_id}")
            await bot.send_message(chat_id, random_compliment.encode("utf-8").decode("utf-8"))
            logging.info(f"Message sent successfully to chat_id {chat_id}")

        logging.info("Messages sent successfully.")
    except Exception as e:
        logging.error(f"Error in send_message: {e}")


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    chat_id = message.chat.id
    logging.info(f"тык")
    try:
        logging.info(f"Received /start command from chat_id {chat_id}")

        existing_chat_ids = await db.get_chat_ids()
        logging.info(f"Existing chat_ids in the database: {existing_chat_ids}")

        if chat_id not in existing_chat_ids:
            await db.add_chat_id(chat_id)
            logging.info(f"Added chat_id {chat_id} to the database.")

        # Отправляем дополнительное сообщение
        await send_message([chat_id])
        logging.info(f"Additional message sent to chat_id {chat_id}")
    except Exception as e:
        logging.error(f"Error in cmd_start: {e}")
        raise  # Добавим эту строку для более подробной информации об ошибке


async def scheduled_job():
    chat_ids = await db.get_chat_ids()
    await send_message(chat_ids)


def job():
    asyncio.create_task(scheduled_job())


async def on_startup(dp):
    # Запускаем расписание
    schedule.every(1).hours.do(job)

    # Устанавливаем вебхук, чтобы использовать Long Polling
    await bot.delete_webhook()

    # Подключаемся к базе данных
    await db.connect()

    # Добавим логирование для проверки наличия пользователей в базе данных
    existing_chat_ids = await db.get_chat_ids()
    logging.info(f"Existing chat_ids in the database: {existing_chat_ids}")

    # Запускаем цикл выполнения задач в фоновом режиме
    asyncio.create_task(background_task())


async def background_task():
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)


async def on_shutdown(dp):
    # Закрываем подключение к базе данных
    await db.close()


def main():
    # Запускаем бота с использованием Long Polling
    executor.start_polling(dp, on_startup=on_startup,
                           on_shutdown=on_shutdown, skip_updates=True)


if __name__ == "__main__":
    main()
