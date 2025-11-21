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


import pyrogram
from pyrogram import Client
from pyrogram.enums import ChatMemberStatus, ParseMode
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import config
from ..logging import LOGGER


class Aviax(Client):
    def __init__(self):
        LOGGER(__name__).info("🚀 Starting Music Bot...")
        super().__init__(
            name="AnanyaMusic",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            parse_mode=ParseMode.HTML,
            max_concurrent_transmissions=7,
        )

    async def start(self):
        await super().start()
        get_me = await self.get_me()
        self.username = get_me.username
        self.id = get_me.id
        self.name = f"{self.me.first_name} {(self.me.last_name or '')}".strip()
        self.mention = self.me.mention

        button = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="✨ ᴀᴅᴅ ᴍᴇ ɪɴ ɢʀᴏᴜᴘ ✨",
                        url=f"https://t.me/{self.username}?startgroup=true",
                    )
                ]
            ]
        )

        caption = (
            f"<b>━━━━━━━━━━━━━━━━━━━━━━━</b>\n"
            f"<b>🥀 ʙᴏᴛ sᴛᴀʀᴛᴇᴅ</b> 🎉\n"
            f"<b>━━━━━━━━━━━━━━━━━━━━━━━</b>\n\n"
            f"<b>🤖 ɴᴀᴍᴇ :</b> {self.name}\n"
            f"<b>🆔 ɪᴅ :</b> <code>{self.id}</code>\n"
            f"<b>📎 ᴜsᴇʀɴᴀᴍᴇ :</b> @{self.username}\n\n"
            f"<b>💖 ᴛʜᴀɴᴋs ғᴏʀ ᴜsɪɴɢ ᴍᴇ!</b>\n"
            f"<b>━━━━━━━━━━━━━━━━━━━━━━━</b>"
        )

        if config.LOG_GROUP_ID:
            try:
                await self.send_photo(
                    config.LOG_GROUP_ID,
                    photo=config.START_IMG_URL,
                    caption=caption,
                    reply_markup=button,
                )
            except pyrogram.errors.ChatWriteForbidden as e:
                LOGGER(__name__).error(f"Bot cannot write to log group: {e}")
                try:
                    await self.send_message(
                        config.LOG_GROUP_ID,
                        caption,
                        reply_markup=button,
                    )
                except Exception as e:
                    LOGGER(__name__).error(f"Failed to send message in log group: {e}")
            except Exception as e:
                LOGGER(__name__).error(f"Unexpected error while sending to log group: {e}")
        else:
            LOGGER(__name__).warning("LOG_GROUP_ID not set — skipping log group notifications.")

        # Check admin in log group
        if config.LOG_GROUP_ID:
            try:
                chat_member_info = await self.get_chat_member(config.LOG_GROUP_ID, self.id)
                if chat_member_info.status != ChatMemberStatus.ADMINISTRATOR:
                    LOGGER(__name__).error("Please promote bot as admin in log group.")
            except Exception as e:
                LOGGER(__name__).error(f"Error checking bot status: {e}")

        LOGGER(__name__).info(f"✅ Music Bot Started as {self.name}")

    async def stop(self):
        await super().stop()


# ©️ Copyright Reserved - @ZoxxOP  Akash Dakshwanshi

# ===========================================
# ©️ 2025 Akash Dakshwanshi (aka @ZoxxOP)
# 🔗 GitHub : https://github.com/ZoxxOP/AnanyaMusic
# 📢 Telegram Channel : https://t.me/AnanyaBots
# ===========================================


# ❤️ Love From AnanyaBots
