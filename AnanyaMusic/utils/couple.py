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


coupledb = {}


async def _get_lovers(cid: int):
    chat_data = coupledb.get(cid, {})
    lovers = chat_data.get("couple", {})
    return lovers


async def get_image(cid: int):
    chat_data = coupledb.get(cid, {})
    image = chat_data.get("img", "")
    return image


async def get_couple(cid: int, date: str):
    lovers = await _get_lovers(cid)
    return lovers.get(date, False)


async def save_couple(cid: int, date: str, couple: dict, img: str):
    if cid not in coupledb:
        coupledb[cid] = {"couple": {}, "img": ""}
    coupledb[cid]["couple"][date] = couple
    coupledb[cid]["img"] = img


# ©️ Copyright Reserved - @ZoxxOP  Akash Dakshwanshi

# ===========================================
# ©️ 2025 Akash Dakshwanshi (aka @ZoxxOP)
# 🔗 GitHub : https://github.com/ZoxxOP/AnanyaMusic
# 📢 Telegram Channel : https://t.me/AnanyaBots
# ===========================================


# ❤️ Love From AnanyaBots
