from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message

from config import ADMIN_IDS
from keyboards import subscribe_kb
from utils import is_subscribed

SUB_TEXT = (
    "⚠️ Botdan foydalanish uchun avval kanalimizga obuna bo'ling.\n\n"
    "Obuna bo'lgach, «✅ Tekshirish» tugmasini bosing."
)


class SubscriptionMiddleware(BaseMiddleware):
    """Kanalga obuna bo'lmagan foydalanuvchini botdan foydalantirmaydi."""

    async def __call__(self, handler, event, data):
        user = data.get("event_from_user")
        if user is None or user.id in ADMIN_IDS:
            return await handler(event, data)

        if isinstance(event, CallbackQuery) and event.data == "check_sub":
            return await handler(event, data)

        if await is_subscribed(data["bot"], user.id):
            return await handler(event, data)

        if isinstance(event, Message):
            await event.answer(SUB_TEXT, reply_markup=subscribe_kb())
        elif isinstance(event, CallbackQuery):
            await event.answer("Avval kanalga obuna bo'ling!", show_alert=True)
        return None
