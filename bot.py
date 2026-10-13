import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiohttp import web

from config import BOT_TOKEN
from database import init_db
from handlers import admin, user
from middlewares import SubscriptionMiddleware

logging.basicConfig(level=logging.INFO)


async def start_web_server():
    """Render Web Service port ochilishini talab qiladi."""

    async def health(request):
        return web.Response(text="Bot ishlayapti")

    app = web.Application()
    app.router.add_get("/", health)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", "10000"))
    await web.TCPSite(runner, "0.0.0.0", port).start()


async def main():
    init_db()
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties())
    dp = Dispatcher()

    dp.message.middleware(SubscriptionMiddleware())
    dp.callback_query.middleware(SubscriptionMiddleware())

    # Admin router birinchi bo'lishi shart
    dp.include_router(admin.router)
    dp.include_router(user.router)

    await start_web_server()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
