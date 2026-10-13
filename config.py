import os

# ===== ASOSIY SOZLAMALAR =====
# Render'da: Environment bo'limida shu nomlar bilan kiritiladi.
BOT_TOKEN = os.getenv("BOT_TOKEN", "BU_YERGA_BOT_TOKEN")

# Admin Telegram ID'lari (bir nechta bo'lsa vergul bilan: 111,222)
ADMIN_IDS = [
    int(x) for x in os.getenv("ADMIN_IDS", "0").split(",") if x.strip().isdigit()
]

# Majburiy obuna kanali (bot shu kanalda ADMIN bo'lishi shart!)
CHANNEL_ID = os.getenv("CHANNEL_ID", "@karburatornew")
CHANNEL_URL = os.getenv("CHANNEL_URL", "https://t.me/karburatornew")

DB_PATH = os.getenv("DB_PATH", "bot.db")

# Ustaxona joylashuvi (botdagi /admin orqali ham o'zgartirish mumkin)
LATITUDE = float(os.getenv("LATITUDE", "40.4700"))
LONGITUDE = float(os.getenv("LONGITUDE", "71.7200"))

# ===== BOT MATNLARI =====
# Render bepul rejasida bot qayta ishga tushganda admin paneldan kiritilgan
# matnlar o'chib, shu yerdagilar qaytadi. Shuning uchun asl matnlarni shu yerga yozing.
DEFAULT_TEXTS = {
    "welcome": (
        "👋 Assalomu alaykum!\n\n"
        "Qumtepa Karburator botiga xush kelibsiz.\n"
        "Kerakli bo'limni tanlang 👇"
    ),
    "about": (
        "🔧 Qumtepa Karburator\n\n"
        "Karburator ta'mirlash va sozlash bo'yicha ustaxona.\n"
        "(Matnni /admin orqali yoki shu yerda o'zgartiring)"
    ),
    "address": (
        "📍 Manzil:\n"
        "Marg'ilon, Qumtepa bozori oldida."
    ),
    "prices": (
        "💰 Narxlar:\n\n"
        "(Narxlar ro'yxatini /admin orqali yoki shu yerda kiriting)"
    ),
    "hours": (
        "🕒 Ish vaqti:\n\n"
        "(Ish vaqtini /admin orqali yoki shu yerda kiriting)"
    ),
}

TEXT_TITLES = {
    "welcome": "👋 Salomlashuv matni",
    "about": "🔧 Karburator haqida",
    "address": "📍 Manzil matni",
    "prices": "💰 Narxlar",
    "hours": "🕒 Ish vaqti",
}
