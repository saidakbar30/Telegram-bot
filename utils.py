import asyncio
import logging

from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError, TelegramRetryAfter

from config import CHANNEL_ID
from database import get_active_user_ids, set_active

log = logging.getLogger(__name__)


async def is_subscribed(bot: Bot, user_id: int) -> bool:
    """Foydalanuvchi kanalga a'zomi yoki yo'qmi."""
    try:
        member = await bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ("member", "administrator", "creator")
    except Exception as e:
        log.warning("Obunani tekshirib bo'lmadi (bot kanalda admin emasmi?): %s", e)
        return False


async def broadcast(bot: Bot, from_chat_id: int, message_id: int) -> tuple[int, int]:
    """Barcha faol foydalanuvchilarga xabarni nusxalab yuboradi."""
    sent = failed = 0
    for uid in get_active_user_ids():
        try:
            await bot.copy_message(uid, from_chat_id, message_id)
            sent += 1
        except TelegramRetryAfter as e:
            await asyncio.sleep(e.retry_after)
            try:
                await bot.copy_message(uid, from_chat_id, message_id)
                sent += 1
            except Exception:
                failed += 1
        except TelegramForbiddenError:
            set_active(uid, False)
            failed += 1
        except Exception:
            failed += 1
        await asyncio.sleep(0.05)
    return sent, failed
