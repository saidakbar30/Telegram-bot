from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config import ADMIN_IDS, TEXT_TITLES
from database import get_stats, get_text, set_location, set_text
from keyboards import admin_menu_kb, back_kb, cancel_kb, edit_texts_kb
from states import AdminStates
from utils import broadcast

router = Router()
# Bu router faqat adminlar uchun
router.message.filter(F.from_user.id.in_(ADMIN_IDS))
router.callback_query.filter(F.from_user.id.in_(ADMIN_IDS))


@router.message(Command("admin"))
async def admin_panel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("🛠 Admin panel", reply_markup=admin_menu_kb())


@router.message(Command("cancel"))
async def cancel_cmd(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Bekor qilindi.", reply_markup=admin_menu_kb())


@router.callback_query(F.data.in_({"adm:menu", "adm:cancel"}))
async def to_menu(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text("🛠 Admin panel", reply_markup=admin_menu_kb())
    await call.answer()


# ----- Statistika -----
@router.callback_query(F.data == "adm:stats")
async def stats(call: CallbackQuery):
    s = get_stats()
    text = (
        "📊 Statistika\n\n"
        f"👥 Jami foydalanuvchilar: {s['total']}\n"
        f"✅ Faol: {s['active']}\n"
        f"🚫 Botni bloklagan: {s['blocked']}\n"
        f"🆕 Bugun qo'shilgan: {s['today']}"
    )
    await call.message.edit_text(text, reply_markup=back_kb())
    await call.answer()


# ----- Xabar yuborish -----
@router.callback_query(F.data == "adm:broadcast")
async def broadcast_start(call: CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.broadcast)
    await call.message.edit_text(
        "📢 Hammaga yuboriladigan xabarni yuboring (matn, rasm yoki video).",
        reply_markup=cancel_kb(),
    )
    await call.answer()


@router.message(AdminStates.broadcast)
async def broadcast_send(message: Message, state: FSMContext):
    await state.clear()
    wait = await message.answer("⏳ Yuborilmoqda...")
    sent, failed = await broadcast(message.bot, message.chat.id, message.message_id)
    await wait.edit_text(
        f"✅ Yuborildi: {sent}\n❌ Yuborilmadi: {failed}", reply_markup=back_kb()
    )


# ----- Matnlarni tahrirlash -----
@router.callback_query(F.data == "adm:texts")
async def texts_menu(call: CallbackQuery):
    await call.message.edit_text(
        "✏️ Qaysi matnni o'zgartirasiz?", reply_markup=edit_texts_kb()
    )
    await call.answer()


@router.callback_query(F.data.startswith("adm:edit:"))
async def edit_start(call: CallbackQuery, state: FSMContext):
    key = call.data.split(":", 2)[2]
    if key not in TEXT_TITLES:
        await call.answer("Noma'lum bo'lim", show_alert=True)
        return
    await state.set_state(AdminStates.edit_text)
    await state.update_data(key=key)
    await call.message.edit_text(
        f"{TEXT_TITLES[key]}\n\nHozirgi matn:\n\n{get_text(key)}\n\n"
        "👇 Yangi matnni yuboring.",
        reply_markup=cancel_kb(),
    )
    await call.answer()


@router.message(AdminStates.edit_text)
async def edit_save(message: Message, state: FSMContext):
    if not message.text:
        await message.answer("Iltimos, faqat matn yuboring.", reply_markup=cancel_kb())
        return
    data = await state.get_data()
    key = data.get("key")
    set_text(key, message.text)
    await state.clear()
    await message.answer(
        f"✅ «{TEXT_TITLES.get(key, key)}» yangilandi.", reply_markup=admin_menu_kb()
    )


# ----- Lokatsiya -----
@router.callback_query(F.data == "adm:location")
async def location_start(call: CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.set_location)
    await call.message.edit_text(
        "📍 Ustaxona turgan joydan Telegram'ning 📎 → Joylashuv (Location) "
        "orqali lokatsiya yuboring.",
        reply_markup=cancel_kb(),
    )
    await call.answer()


@router.message(AdminStates.set_location, F.location)
async def location_save(message: Message, state: FSMContext):
    set_location(message.location.latitude, message.location.longitude)
    await state.clear()
    await message.answer("✅ Lokatsiya yangilandi.", reply_markup=admin_menu_kb())


@router.message(AdminStates.set_location)
async def location_wrong(message: Message):
    await message.answer("Iltimos, aynan lokatsiya yuboring.", reply_markup=cancel_kb())
