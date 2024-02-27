from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from aiogram.fsm.state import StatesGroup, State
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os

from db.models import User

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


Base.metadata.create_all(bind=engine)

API_TOKEN = "YOUR_BOT_TOKEN"
bot = Bot(token=API_TOKEN)
dp = Dispatcher()


class RegistrationStep(StatesGroup):
    step1 = State()
    step2 = State()


@dp.message(Command('start'))
async def start_command(message: types.Message):
    await message.answer("Привет! Давайте начнем регистрацию. Введите ваш ник:")
    await RegistrationStep.step1.set()


@dp.message(state=RegistrationStep.step1)
async def process_step1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['username'] = message.text

    await message.answer(
        "Теперь введите номер телефона, имя, ИНН и название организации через запятую:")

    await RegistrationStep.step2.set()


@dp.message(state=RegistrationStep.step2)
async def process_step2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        user_data = {"user_id": message.from_user.id, "username": data['username']}
        phone_number, name, inn, organization_name = map(str.strip, message.text.split(','))
        user_data.update(
            {"phone_number": phone_number, "name": name, "inn": inn, "organization_name": organization_name})

        # Save user data to the database
        db = SessionLocal()
        user = User(**user_data)
        db.add(user)
        db.commit()
        db.refresh(user)

    await message.answer(
        "Регистрация завершена! Теперь вы можете использовать команду /tracking для отслеживания статуса заказа.")



