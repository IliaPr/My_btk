from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Update
from fastapi import APIRouter

from config import TELEGRAM_TOKEN, REDIS_HOST, REDIS_PORT, REDIS_DB
from tg.birthday_notify.handlers.manage import manage_router
from tg.task_collect.handlers.manage import task_router
from tg.middlewares import LoggingMiddleware

# FastAPI-роутер для приёма входящих от телеграм запросов
bot_router = APIRouter(prefix="/bot")
# Объект бота
bot = Bot(token=TELEGRAM_TOKEN)
# Хранилище данных бота
storage = RedisStorage.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}")
# Диспатчер, управляющий событиями бота
dp = Dispatcher(bot=bot, storage=storage)
# Подключение логгера к диспатчеру
dp.message.middleware(LoggingMiddleware())
dp.callback_query.middleware(LoggingMiddleware())
# Подключения роутов бота к диспатчеру
dp.include_router(manage_router)
dp.include_router(task_router)


@bot_router.post("/webhook")
async def bot_webhook(update: dict):
    """
    Обработчик вебхука от телеграма
    """
    update = Update.model_validate(update, context={"bot": bot})
    await dp.feed_update(bot, update)