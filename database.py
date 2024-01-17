import logging
from sqlalchemy import create_engine, Column, BigInteger, MetaData, Table, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import POSTGRES_USER, POSTGRES_PASSWORD, DB_HOST, DB_PORT, POSTGRES_DB

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True)
    chat_id = Column(BigInteger)

class Database:
    def __init__(self):
        self.engine = create_engine(
            f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:{DB_PORT}/{POSTGRES_DB}"
        )
        self.metadata = MetaData()

        # Явное объявление столбцов
        self.users = Table('users', self.metadata,
                          Column('id', BigInteger, primary_key=True),
                          Column('chat_id', BigInteger),
                          extend_existing=True)

        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    async def add_chat_id(self, chat_id: int):
        try:
            with self.Session() as session:
                user = User(chat_id=chat_id)
                session.add(user)
                session.commit()
            logging.info(f"Successfully added chat_id {chat_id} to the database.")
        except Exception as e:
            logging.error(f"Error adding chat_id {chat_id} to the database: {e}")

    async def get_chat_ids(self):
        with self.Session() as session:
            query = select([self.users.c.chat_id])
            result = session.execute(query)
            return [row[0] for row in result]
