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


from pyrogram import filters
from pyrogram.types import Message

from AnanyaMusic import app
from AnanyaMusic.misc import SUDOERS
from AnanyaMusic.utils.database import (
    get_lang,
    is_maintenance,
    maintenance_off,
    maintenance_on,
)
from strings import get_string


@app.on_message(filters.command(["maintenance"]) & SUDOERS)
async def maintenance(client, message: Message):
    try:
        language = await get_lang(message.chat.id)
        _ = get_string(language)
    except:
        _ = get_string("en")
    usage = _["maint_1"]
    if len(message.command) != 2:
        return await message.reply_text(usage)
    state = message.text.split(None, 1)[1].strip().lower()
    if state == "enable":
        if await is_maintenance() is False:
            await message.reply_text(_["maint_4"])
        else:
            await maintenance_on()
            await message.reply_text(_["maint_2"].format(app.mention))
    elif state == "disable":
        if await is_maintenance() is False:
            await maintenance_off()
            await message.reply_text(_["maint_3"].format(app.mention))
        else:
            await message.reply_text(_["maint_5"])
    else:
        await message.reply_text(usage)


# ©️ Copyright Reserved - @ZoxxOP  Akash Dakshwanshi

# ===========================================
# ©️ 2025 Akash Dakshwanshi (aka @ZoxxOP)
# 🔗 GitHub : https://github.com/ZoxxOP/AnanyaMusic
# 📢 Telegram Channel : https://t.me/AnanyaBots
# ===========================================


# ❤️ Love From AnanyaBots
