from aiogram.fsm.state import State, StatesGroup


class AdminStates(StatesGroup):
    broadcast = State()      # hammaga xabar yuborish
    edit_text = State()      # bot matnini tahrirlash
    set_location = State()   # ustaxona lokatsiyasini o'zgartirish
