from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message

from database import add_user, get_location, get_text
from keyboards import (
    BTN_ABOUT,
    BTN_ADDRESS,
    BTN_HOURS,
    BTN_PRICES,
    main_menu_kb,
)
from utils import is_subscribed

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    u = message.from_user
    add_user(u.id, u.full_name, u.username)
    await message.answer(get_text("welcome"), reply_markup=main_menu_kb())


@router.callback_query(F.data == "check_sub")
async def check_sub(call: CallbackQuery):
    if await is_subscribed(call.bot, call.from_user.id):
        u = call.from_user
        add_user(u.id, u.full_name, u.username)
        try:
            await call.message.delete()
        except Exception:
            pass
        await call.message.answer(get_text("welcome"), reply_markup=main_menu_kb())
        await call.answer()
    else:
        await call.answer("❌ Siz hali obuna bo'lmagansiz!", show_alert=True)


@router.message(F.text == BTN_ABOUT)
async def about(message: Message):
    await message.answer(get_text("about"))


@router.message(F.text == BTN_ADDRESS)
async def address(message: Message):
    lat, lon = get_location()
    await message.answer_location(latitude=lat, longitude=lon)
    await message.answer(get_text("address"))


@router.message(F.text == BTN_PRICES)
async def prices(message: Message):
    await message.answer(get_text("prices"))


@router.message(F.text == BTN_HOURS)
async def hours(message: Message):
    await message.answer(get_text("hours"))


@router.message()
async def fallback(message: Message):
    await message.answer(
        "Iltimos, menyudagi tugmalardan birini tanlang 👇",
        reply_markup=main_menu_kb(),
    )
