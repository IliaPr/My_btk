import logging
import os
from dotenv import load_dotenv

# Загрузите переменные окружения из файла .env
logging.basicConfig(level=logging.DEBUG)
load_dotenv()

# Получите переменные окружения
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
