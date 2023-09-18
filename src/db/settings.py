import logging
import os

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine
from sqlalchemy.ext.asyncio import create_async_engine

load_dotenv(".env")


log_level: str = os.getenv("SQLALCHEMY_LOG_LEVEL")
logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(getattr(logging, log_level))


class EngineDB:
    url_obj: URL = URL.create(
        "postgresql+asyncpg",
        username=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("POSTGRES_DB"),
    )
    __instance = None

    def __new__(cls) -> "EngineDB":
        if cls.__instance is None:
            cls.__instance: "EngineDB" = create_async_engine(url=cls.url_obj)
        return cls.__instance
