from aiogram.fsm.state import State, StatesGroup

class Base(StatesGroup):
    name = State()
    location = State()