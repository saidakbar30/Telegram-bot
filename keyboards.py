from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from config import CHANNEL_URL, TEXT_TITLES

BTN_ABOUT = "🔧 Karburator haqida"
BTN_ADDRESS = "📍 Ustaxona manzili"
BTN_PRICES = "💰 Barcha narxlar"
BTN_HOURS = "🕒 Ish vaqti"


def main_menu_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_ABOUT)],
            [KeyboardButton(text=BTN_ADDRESS), KeyboardButton(text=BTN_PRICES)],
            [KeyboardButton(text=BTN_HOURS)],
        ],
        resize_keyboard=True,
    )


def subscribe_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📢 Kanalga obuna bo'lish", url=CHANNEL_URL)],
            [InlineKeyboardButton(text="✅ Tekshirish", callback_data="check_sub")],
        ]
    )


def admin_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📊 Statistika", callback_data="adm:stats")],
            [InlineKeyboardButton(text="📢 Xabar yuborish", callback_data="adm:broadcast")],
            [InlineKeyboardButton(text="✏️ Matnlarni tahrirlash", callback_data="adm:texts")],
            [InlineKeyboardButton(text="📍 Lokatsiyani o'zgartirish", callback_data="adm:location")],
        ]
    )


def edit_texts_kb() -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text=title, callback_data=f"adm:edit:{key}")]
        for key, title in TEXT_TITLES.items()
    ]
    rows.append([InlineKeyboardButton(text="⬅️ Orqaga", callback_data="adm:menu")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def cancel_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="adm:cancel")]
        ]
    )


def back_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="adm:menu")]
        ]
    )
