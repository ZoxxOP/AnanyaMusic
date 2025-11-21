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
from AnanyaMusic.utils.database import add_gban_user, remove_gban_user
from AnanyaMusic.utils.decorators.language import language
from AnanyaMusic.utils.extraction import extract_user
from config import BANNED_USERS


@app.on_message(filters.command(["block"]) & SUDOERS)
@language
async def useradd(client, message: Message, _):
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(_["general_1"])
    user = await extract_user(message)
    if user.id in BANNED_USERS:
        return await message.reply_text(_["block_1"].format(user.mention))
    await add_gban_user(user.id)
    BANNED_USERS.add(user.id)
    await message.reply_text(_["block_2"].format(user.mention))


@app.on_message(filters.command(["unblock"]) & SUDOERS)
@language
async def userdel(client, message: Message, _):
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(_["general_1"])
    user = await extract_user(message)
    if user.id not in BANNED_USERS:
        return await message.reply_text(_["block_3"].format(user.mention))
    await remove_gban_user(user.id)
    BANNED_USERS.remove(user.id)
    await message.reply_text(_["block_4"].format(user.mention))


@app.on_message(filters.command(["blocked", "blockedusers", "blusers"]) & SUDOERS)
@language
async def sudoers_list(client, message: Message, _):
    if not BANNED_USERS:
        return await message.reply_text(_["block_5"])
    mystic = await message.reply_text(_["block_6"])
    msg = _["block_7"]
    count = 0
    for users in BANNED_USERS:
        try:
            user = await app.get_users(users)
            user = user.first_name if not user.mention else user.mention
            count += 1
        except:
            continue
        msg += f"{count}➤ {user}\n"
    if count == 0:
        return await mystic.edit_text(_["block_5"])
    else:
        return await mystic.edit_text(msg)


# ©️ Copyright Reserved - @ZoxxOP  Akash Dakshwanshi

# ===========================================
# ©️ 2025 Akash Dakshwanshi (aka @ZoxxOP)
# 🔗 GitHub : https://github.com/ZoxxOP/AnanyaMusic
# 📢 Telegram Channel : https://t.me/AnanyaBots
# ===========================================


# ❤️ Love From AnanyaBots
