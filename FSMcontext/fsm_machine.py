from aiogram.fsm.state import StatesGroup, State


class startSG(StatesGroup):
    start = State()
    terms = State()
    balance = State()
    wallet = State()
    tasks = State()
    rewards = State()