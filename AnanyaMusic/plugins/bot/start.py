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


import time
import random

from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from py_yt import VideosSearch

import config
from AnanyaMusic import app
from AnanyaMusic.misc import _boot_
from AnanyaMusic.plugins.sudo.sudoers import sudoers_list
from AnanyaMusic.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_lang,
    is_banned_user,
    is_on_off,
)
from AnanyaMusic.utils import bot_sys_stats
from AnanyaMusic.utils.decorators.language import LanguageStart
from AnanyaMusic.utils.formatters import get_readable_time
from AnanyaMusic.utils.inline import help_pannel_page1, private_panel, start_panel
from config import BANNED_USERS
from strings import get_string


RANDOM_STICKERS = [
    "CAACAgUAAxkBAAEPbk1o0snAMAABD1dJ-MZEm_X_okD-nFYAAh8QAAK0zShUaoZsm96EvzQ2BA",
    "CAACAgUAAxkBAAEPbk9o0snDq5hEaP0m8bvUWpDo1vFgLQAC7RAAA8cpVMNMmZ22yquQNgQ",
    "CAACAgUAAxkBAAEPblNo0snHbOideaM_rgM8PXze_lO_FwACyREAAiMcKVSEbd50BZVsUzYE",
    "CAACAgUAAxkBAAEPblVo0snJAYHKLSJvR-ueI3r2hbbgxgACThYAAlHgKFQAARW8aAfbrqc2BA"
]

@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
    # Sticker bhejna disable
    # random_sticker = random.choice(RANDOM_STICKERS)
    # await message.reply_sticker(sticker=random_sticker)
    
    await add_served_user(message.from_user.id)

    # Reaction user ko turant bhejna
    emojis = ["👍", "❤️", "💯", "😁", "🤝", "🤔", "😢"]
    await app.send_reaction(message.chat.id, message.id, random.choice(emojis))

    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]

        if name[0:4] == "help":
            keyboard = help_pannel(_)
            return await message.reply_video(
                video=config.START_VIDEO_URL,
                caption=_["help_1"].format(config.SUPPORT_GROUP),
                protect_content=True,
                has_spoiler=True,
                reply_markup=keyboard,
            )

        if name[0:3] == "sud":
            await sudoers_list(client=client, message=message, _=_)
            if await is_on_off(2):
                return await app.send_message(
                    chat_id=config.LOG_GROUP_ID,
                    text=f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ <b>sᴜᴅᴏʟɪsᴛ</b>.\n\n"
                         f"<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n"
                         f"<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}",
                )
            return

        if name[0:3] == "inf":
            m = await message.reply_text("🔎")
            query = (str(name)).replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"
            results = VideosSearch(query, limit=1)
            for result in (await results.next())["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                channellink = result["channel"]["link"]
                channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]

            searched_text = _["start_6"].format(
                title, duration, views, published, channellink, channel, app.mention
            )

            key = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text=_["S_B_8"], url=link),
                        InlineKeyboardButton(text=_["S_B_9"], url=config.SUPPORT_GROUP),
                    ],
                ]
            )
            await m.delete()
            await app.send_photo(
                chat_id=message.chat.id,
                photo=thumbnail,
                has_spoiler=True,
                caption=searched_text,
                reply_markup=key,
            )

            if await is_on_off(2):
                return await app.send_message(
                    chat_id=config.LOG_GROUP_ID,
                    text=f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ <b>ᴛʀᴀᴄᴋ ɪɴғᴏʀᴍᴀᴛɪᴏɴ</b>.\n\n"
                         f"<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n"
                         f"<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}",
                )

    else:
        out = private_panel(_)
        UP, CPU, RAM, DISK = await bot_sys_stats()
        await message.reply_video(
            video=config.START_VIDEO_URL,
            caption=_["start_2"].format(message.from_user.mention, app.mention, UP, DISK, CPU, RAM),
            reply_markup=InlineKeyboardMarkup(out),
            has_spoiler=True,
        )

    if await is_on_off(2):
        await app.send_message(
            chat_id=config.LOG_GROUP_ID,
            text=f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ.\n\n"
                 f"<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n"
                 f"<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}",
        )


@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    # Sticker bhejna disable
    # random_sticker = random.choice(RANDOM_STICKERS)
    # await message.reply_sticker(sticker=random_sticker)
    
    out = start_panel(_)
    uptime = int(time.time() - _boot_)
    await message.reply_photo(
        photo=config.START_IMG_URL,
        caption=_["start_1"].format(app.mention, get_readable_time(uptime)),
        reply_markup=InlineKeyboardMarkup(out),
        has_spoiler=True,
    )
    return await add_served_chat(message.chat.id)


@app.on_message(filters.new_chat_members, group=-1)
async def welcome(client, message: Message):
    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)
            if await is_banned_user(member.id):
                try:
                    await message.chat.ban_member(member.id)
                except:
                    pass
            if member.id == app.id:
                if message.chat.type != ChatType.SUPERGROUP:
                    await message.reply_text(_["start_4"])
                    return await app.leave_chat(message.chat.id)
                if message.chat.id in await blacklisted_chats():
                    await message.reply_text(
                        _["start_5"].format(
                            app.mention,
                            f"https://t.me/{app.username}?start=sudolist",
                            config.SUPPORT_GROUP,
                        ),
                        disable_web_page_preview=True,
                    )
                    return await app.leave_chat(message.chat.id)

                # Sticker bhejna disable
                # random_sticker = random.choice(RANDOM_STICKERS)
                # await message.reply_sticker(sticker=random_sticker)

                out = start_panel(_)
                await message.reply_photo(
                    photo=config.START_IMG_URL,
                    caption=_["start_3"].format(
                        message.from_user.first_name,
                        app.mention,
                        message.chat.title,
                        app.mention,
                    ),
                    reply_markup=InlineKeyboardMarkup(out),
                    has_spoiler=True,
                )
                await add_served_chat(message.chat.id)
                await message.stop_propagation()
        except Exception as ex:
            print(ex)


# ©️ Copyright Reserved - @ZoxxOP  Akash Dakshwanshi

# ===========================================
# ©️ 2025 Akash Dakshwanshi (aka @ZoxxOP)
# 🔗 GitHub : https://github.com/ZoxxOP/AnanyaMusic
# 📢 Telegram Channel : https://t.me/AnanyaBots
# ===========================================


# ❤️ Love From AnanyaBots
