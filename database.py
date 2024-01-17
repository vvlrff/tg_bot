import logging
import asyncpg
from config import POSTGRES_USER, POSTGRES_PASSWORD, DB_HOST, DB_PORT, POSTGRES_DB

class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            database=POSTGRES_DB
        )

    async def close(self):
        if self.pool:
            await self.pool.close()

    async def add_chat_id(self, chat_id: int):
        try:
            async with self.pool.acquire() as connection:
                await connection.execute("INSERT INTO users (chat_id) VALUES ($1)", chat_id)
            logging.info(f"Successfully added chat_id {chat_id} to the database.")
        except Exception as e:
            logging.error(f"Error adding chat_id {chat_id} to the database: {e}")

    async def get_chat_ids(self):
        try:
            async with self.pool.acquire() as connection:
                result = await connection.fetch("SELECT chat_id FROM users")
            return [row['chat_id'] for row in result]
        except Exception as e:
            logging.error(f"Error retrieving chat_ids from the database: {e}")
            return []
