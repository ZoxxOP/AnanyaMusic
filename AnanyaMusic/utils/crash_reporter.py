# Copyright (c) 2025 Akash Daskhwanshi <ZoxxOP>
# Location: Mainpuri, Uttar Pradesh 
#
# All rights reserved.
#
# This code is the intellectual property of Akash Dakshwanshi.
# You are not allowed to copy, modify, redistribute, or use this
# code for commercial or personal projects without explicit permission.
#
# Allowed:
# - Forking for personal learning
# - Submitting improvements via pull requests
#
# Not Allowed:
# - Claiming this code as your own
# - Re-uploading without credit or permission
# - Selling or using commercially
#
# Contact for permissions:
# Email: akp954834@gmail.com


import asyncio
from traceback import format_exc
from pyrogram.errors import RPCError

from AnanyaMusic import app
from config import LOG_GROUP_ID

async def notify_logger_about_crash(error: Exception):
    error_text = (
        "🚨 <b><u>Bot Crash Alert</u></b>\n\n"
        f"<b>Error:</b> <code>{str(error)}</code>\n\n"
        f"<b>Traceback:</b>\n<pre>{format_exc()}</pre>"
    )
    try:
        await app.send_message(
            chat_id=LOG_GROUP_ID,
            text=error_text,
            disable_web_page_preview=True
        )
    except RPCError:
        pass

def logger_alert_on_crash(func):
    async def wrapper(client, *args, **kwargs):
        try:
            return await func(client, *args, **kwargs)
        except Exception as e:
            await notify_logger_about_crash(e)
            raise  # Optional: re-raise for higher-level logging if needed
    return wrapper

def setup_global_exception_handler():
    loop = asyncio.get_event_loop()

    def handle_exception(loop, context):
        error = context.get("exception")
        if error:
            asyncio.create_task(notify_logger_about_crash(error))

    loop.set_exception_handler(handle_exception)


# ©️ Copyright Reserved - @ZoxxOP  Akash Dakshwanshi

# ===========================================
# ©️ 2025 Akash Dakshwanshi (aka @ZoxxOP)
# 🔗 GitHub : https://github.com/ZoxxOP/AnanyaMusic
# 📢 Telegram Channel : https://t.me/AnanyaBots
# ===========================================


# ❤️ Love From AnanyaBots
