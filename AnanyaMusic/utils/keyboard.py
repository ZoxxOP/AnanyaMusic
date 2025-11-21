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


from pykeyboard import InlineKeyboard
from pyrogram.types import InlineKeyboardButton as Ikb

from .functions import get_urls_from_text as is_url


def keyboard(buttons_list, row_width: int = 2):
    buttons = InlineKeyboard(row_width=row_width)
    data = [
        (
            Ikb(text=str(i[0]), callback_data=str(i[1]))
            if not is_url(i[1])
            else Ikb(text=str(i[0]), url=str(i[1]))
        )
        for i in buttons_list
    ]
    buttons.add(*data)
    return buttons


def ikb(data: dict, row_width: int = 2):
    return keyboard(data.items(), row_width=row_width)


# ©️ Copyright Reserved - @ZoxxOP  Akash Dakshwanshi

# ===========================================
# ©️ 2025 Akash Dakshwanshi (aka @ZoxxOP)
# 🔗 GitHub : https://github.com/ZoxxOP/AnanyaMusic
# 📢 Telegram Channel : https://t.me/AnanyaBots
# ===========================================


# ❤️ Love From AnanyaBots
