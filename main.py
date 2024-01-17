import logging
import random
import asyncio
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types
import schedule

from database import Database
from config import TELEGRAM_TOKEN

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)
db = Database()


async def send_message(chat_ids):
    try:
        with open("text.txt") as file:
            compliments = [line.strip() for line in file]
            random_compliment = random.choice(compliments)

        for chat_id in chat_ids:
            logging.info(f"Sending message to chat_id {chat_id}")
            await bot.send_message(chat_id, random_compliment)
            logging.info(f"Message sent successfully to chat_id {chat_id}")

        logging.info("Messages sent successfully.")
    except Exception as e:
        logging.error(f"Error in send_message: {e}")


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    chat_id = message.chat.id
    try:
        existing_chat_ids = await db.get_chat_ids()
        if chat_id not in existing_chat_ids:
            await db.add_chat_id(chat_id)
            logging.info(f"Added chat_id {chat_id} to the database.")
    except Exception as e:
        logging.error(f"Error in cmd_start: {e}")


async def scheduled_job():
    chat_ids = await db.get_chat_ids()
    await send_message(chat_ids)


def job():
    asyncio.run(scheduled_job())


schedule.every(1).hours.do(job)

if __name__ == '__main__':
    while True:
        schedule.run_pending()
        asyncio.sleep(1)
