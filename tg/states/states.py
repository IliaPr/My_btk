from aiogram.fsm.state import StatesGroup, State


class UserState(StatesGroup):
    phone_info = State()
    user_name = State()
    inn = State()
    comp_name = State()
