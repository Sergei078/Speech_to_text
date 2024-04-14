from aiogram.fsm.state import StatesGroup, State


class FSMFillForm(StatesGroup):
    voice_message = State()  # Ожидание голосового от пользователя
