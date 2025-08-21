import asyncio
import random

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.raw.functions.messages import DeleteHistory

from ShrutiMusic import userbot as us, app
from ShrutiMusic.core.userbot import assistants

@app.on_message(filters.command("sg"))
async def sg(client: Client, message: Message):
    
    if not message.reply_to_message and len(message.text.strip().split()) < 2:
        return await message.reply("❗ Please reply to a user or provide a username/ID.\nExample: `/sg @username`")

    if message.reply_to_message:
        args = message.reply_to_message.from_user.id
    else:
        args = message.text.strip().split()[1]

    lol = await message.reply("<code>Processing...</code>")

    try:
        user = await client.get_users(str(args))
    except Exception:
        return await lol.edit("<code>⚠️ Invalid username or user ID provided.</code>")

    bot_list = ["sangmata_bot", "sangmata_beta_bot"]
    sg_bot = random.choice(bot_list)

    if 1 in assistants:
        ubot = us.one
    else:
        return await lol.edit("❌ Userbot is not available or not running.")

    try:
        msg = await ubot.send_message(sg_bot, str(user.id))
        await msg.delete()
    except Exception as e:
        return await lol.edit(f"<code>Error: {str(e)}</code>")

    await asyncio.sleep(1)

    async for stalk in ubot.search_messages(msg.chat.id):
        if not stalk or not stalk.text:
            continue
        await message.reply(stalk.text)
        break

    try:
        user_info = await ubot.resolve_peer(sg_bot)
        await ubot.send(DeleteHistory(peer=user_info, max_id=0, revoke=True))
    except Exception:
        pass

    await lol.delete()
