import asyncio
import random
from pyrogram import filters
from pyrogram.types import Message
from pyrogram import enums
from ShrutiMusic import app

# Global dictionary to track active chats for all tagging types
active_chats = {}

# Message templates for different times of day
GM_MESSAGES = [
    "🌞 Gᴏᴏᴅ Mᴏʀɴɪɴɢ 🌼\n\n{mention}",
    "☕ Rise and Shine!\n\n{mention}",
    "🌄 Sᴜʀᴀᴊ Nɪᴋʜʀᴀ, Tᴜᴍʜᴀʀᴀ Dɪɴ Sᴜʙʜ Hᴏ\n\n{mention}",
    "🌻 Nᴇᴇᴛʜ Kʜᴀᴛᴀᴍ, Aʙ Kᴀᴀᴍ Sʜᴜʀᴜ\n\n{mention}",
    "💫 Jᴀɢᴏ Mᴇʀᴇ Sʜᴇʀᴏ!\n\n{mention}",
    "🕊️ Sᴜᴋʜ Sᴀʙʜᴀ Gᴏᴏᴅ Mᴏʀɴɪɴɢ\n\n{mention}",
    "🌅 Nᴀʏɪ Sᴜʙᴀʜ, Nᴀʏᴇ Sᴀᴘɴᴇ\n\n{mention}",
    "🌸 Pʜᴜᴀʟᴏɴ Sᴇ Bʜᴀʀᴀ Yᴇʜ Sᴜʙᴀʜ\n\n{mention}",
    "⭐ Uᴛʜᴏ Mᴇʀᴇ Sɪᴛᴀʀᴏ, Dɪɴ Sᴜʜᴀᴠᴀɴᴀ Hᴏ\n\n{mention}",
    "🌺 Kʜᴜsʜɪʏᴏɴ Sᴇ Bʜᴀʀᴀ Hᴏ Yᴇʜ Dɪɴ\n\n{mention}",
    "🦋 Tɪᴛʟɪʏᴏɴ Kɪ Tᴀʀᴀʜ Uᴅᴏ Aᴀᴊ\n\n{mention}",
    "🌈 Rᴀɴɢ Bʜᴀʀᴀ Hᴏ Yᴇʜ Dɪɴ Tᴜᴍʜᴀʀᴀ\n\n{mention}",
    "🎵 Pᴀᴋsʜɪʏᴏɴ Kᴀ Gᴀᴀɴᴀ Sᴜɴᴋᴇ Uᴛʜᴏ\n\n{mention}",
    "🌤️ Dʜᴜᴀɴ Kᴀ Gɪʟᴀᴀs Aᴜʀ Tᴜᴍʜᴀʀɪ Hᴀɴsɪ\n\n{mention}",
    "🌟 Cʜᴀᴀɴᴅ Sɪᴛᴀʀᴇ Bᴏʟᴇ - Gᴏᴏᴅ Mᴏʀɴɪɴɢ\n\n{mention}",
    "💐 Hᴀʀ Kᴀᴀᴍ Mᴇɪɴ Kᴀᴀᴍʏᴀʙɪ Mɪʟᴇ\n\n{mention}"
]

GA_MESSAGES = [
    "🌞 Gᴏᴏᴅ Aғᴛᴇʀɴᴏᴏɴ ☀️\n\n{mention}",
    "🍵 Cʜᴀɪ Pɪ Lᴏ, Aғᴛᴇʀɴᴏᴏɴ Hᴏ Gᴀʏɪ\n\n{mention}",
    "🌤️ Hᴀʟᴋɪ Dᴏᴘʜᴀʀ, Aᴜʀ Tᴜᴍʜᴀʀᴀ Nᴀᴀᴍ 💌\n\n{mention}",
    "😴 Sᴏɴᴀ Mᴀᴛ, Kᴀᴀᴍ Kᴀʀᴏ 😜\n\n{mention}",
    "📢 Hᴇʏ Gᴏᴏᴅ Aғᴛᴇʀɴᴏᴏɴ!\n\n{mention}",
    "🌅 Dᴏᴘʜᴀʀ Kᴀ Sᴜʀᴀᴊ Tᴇᴢ Hᴀɪ\n\n{mention}",
    "🥗 Kʜᴀᴀɴᴀ Kʜᴀʏᴀ Kᴇ Nᴀʜɪ?\n\n{mention}",
    "☀️ Tᴇᴢ Dʜᴜᴀᴘ Mᴇɪɴ Tʜᴀɴᴅᴀ Pᴀᴀɴɪ Pɪʏᴏ\n\n{mention}",
    "🌻 Dᴏᴘʜᴀʀ Kᴀ Aʀᴀᴀᴍ Kᴀʀᴏ\n\n{mention}",
    "🍃 Pᴀᴘᴇᴅ Kᴇ Nᴇᴇᴄʜᴇ Bᴀɪᴛʜᴋᴇ Bᴀᴀᴛᴇɪɴ\n\n{mention}",
    "🌸 Lᴜɴᴄʜ Kᴀ Tɪᴍᴇ Hᴏ Gᴀʏᴀ\n\n{mention}",
    "🦋 Dᴏᴘʜᴀʀ Kɪ Mᴀsᴛɪ Kᴀʀᴏ\n\n{mention}",
    "🍉 Tᴀʀʙᴜᴊ Kʜᴀᴀᴋᴇ Tʜᴀɴᴅᴀ Hᴏ Jᴀᴏ\n\n{mention}",
    "🌺 Aᴀsᴍᴀɴ Bʜɪ Sᴀᴀғ Hᴀɪ Aᴀᴊ\n\n{mention}",
    "🎵 Gᴜɴɢᴜɴᴀᴛᴇ Hᴜᴇ Kᴀᴀᴍ Kᴀʀᴏ\n\n{mention}",
    "🌈 Rᴀɴɢ Bɪʀᴀɴɢᴀ Dᴏᴘʜᴀʀ\n\n{mention}"
]

GN_MESSAGES = [
    "🌙 Gᴏᴏᴅ Nɪɢʜᴛ\n\n{mention}",
    "💤 Sᴏɴᴇ Cʜᴀʟᴏ, Kʜᴀᴡᴀʙᴏɴ Mᴇɪɴ Mɪʟᴛᴇ Hᴀɪɴ 😴\n\n{mention}",
    "🌌 Aᴀsᴍᴀɴ Bʜɪ Sᴏ Gᴀʏᴀ, Aʙ Tᴜᴍʜɪ Bʜɪ Sᴏ Jᴀᴏ!\n\n{mention}",
    "✨ Rᴀᴀᴛ Kᴀ Sᴀᴋᴏᴏɴ Tᴜᴍʜᴇɪ Mɪʟᴇ\n\n{mention}",
    "🌃 Gᴏᴏᴅ Nɪɢʜᴛ & Sᴡᴇᴇᴛ Dʀᴇᴀᴍs\n\n{mention}",
    "🌟 Sɪᴛᴀʀᴏɴ Kᴇ Sᴀᴀᴛʜ Sᴏɴᴀ\n\n{mention}",
    "🕊️ Cᴀᴀɴᴅ Kɪ Rᴏsʜɴɪ Mᴇɪɴ Aᴀʀᴀᴀᴍ\n\n{mention}",
    "🎭 Sᴀᴘɴᴏɴ Kᴀ Rᴀᴀᴊᴀ Bᴀɴᴋᴇ Sᴏɴᴀ\n\n{mention}",
    "🌺 Rᴀᴀᴛ Kᴇ Pʜᴜᴀʟᴏɴ Sᴇ Mɪʟᴏ\n\n{mention}",
    "💫 Cʜᴀᴀɴᴅ Mᴀᴀᴍᴀ Kʜᴀᴀɴɪ Sᴜɴᴀᴛᴇ Hᴀɪɴ\n\n{mention}",
    "🎵 Lᴏʀɪ Kᴇ Sᴀᴀᴛʜ Sᴏɴᴀ\n\n{mention}",
    "🌸 Sᴀᴀʀᴇ Gᴀᴍ Bʜᴜᴀʟᴀᴋᴇ Sᴏɴᴀ\n\n{mention}",
    "🦋 Tɪᴛʟɪʏᴏɴ Kᴇ Sᴀᴀᴛʜ Sᴀᴘɴᴇ\n\n{mention}",
    "🌈 Rᴀɴɢ Bɪʀᴀɴɢᴇ Kʜᴀᴀʙ Dᴇᴋʜɴᴀ\n\n{mention}",
    "🕯️ Dɪʏᴇ Kɪ Rᴏsʜɴɪ Mᴇɪɴ Sᴏɴᴀ\n\n{mention}",
    "🌅 Kᴀʟ Pʜɪʀ Mɪʟᴇɴɢᴇ Sᴜʙᴀʜ\n\n{mention}"
]

# Helper function to get all non-bot, non-deleted users from a chat
async def get_chat_users(chat_id):
    """Get all valid users from a chat (excluding bots and deleted accounts)"""
    users = []
    async for member in app.get_chat_members(chat_id):
        if member.user.is_bot or member.user.is_deleted:
            continue
        users.append(member.user)
    return users

# Generic tagging function
async def tag_users(chat_id, messages, tag_type):
    """Generic function to tag users with specified messages"""
    users = await get_chat_users(chat_id)
    
    for i in range(0, len(users), 5):
        # Check if tagging was stopped
        if chat_id not in active_chats:
            break
            
        batch = users[i:i+5]
        # Create proper mentions - this will show as clickable names
        mentions = " ".join([f"[{u.first_name}](tg://user?id={u.id})" for u in batch])
        msg = random.choice(messages).format(mention=mentions)
        
        # Use parse_mode=enums.ParseMode.MARKDOWN to properly format the mentions
        await app.send_message(chat_id, msg, disable_web_page_preview=True, parse_mode=enums.ParseMode.MARKDOWN)
        await asyncio.sleep(2)
    
    # Clean up and send completion message
    active_chats.pop(chat_id, None)
    await app.send_message(chat_id, f"✅ {tag_type} Tᴀɢɢɪɴɢ Dᴏɴᴇ!")

# =================== GOOD MORNING COMMANDS ===================

@app.on_message(filters.command("gmtag") & filters.group)
async def gmtag(_, message: Message):
    """Start Good Morning tagging"""
    chat_id = message.chat.id
    
    if chat_id in active_chats:
        return await message.reply("⚠️ Gᴏᴏᴅ Mᴏʀɴɪɴɢ Tᴀɢɢɪɴɢ Aʟʀᴇᴀᴅʏ Rᴜɴɴɪɴɢ.")
    
    active_chats[chat_id] = True
    await message.reply("☀️ Gᴏᴏᴅ Mᴏʀɴɪɴɢ Tᴀɢɢɪɴɢ Sᴛᴀʀᴛᴇᴅ...")
    
    await tag_users(chat_id, GM_MESSAGES, "Gᴏᴏᴅ Mᴏʀɴɪɴɢ")

@app.on_message(filters.command("gmstop") & filters.group)
async def gmstop(_, message: Message):
    """Stop Good Morning tagging"""
    chat_id = message.chat.id
    
    if chat_id in active_chats:
        del active_chats[chat_id]
        await message.reply("🛑 Gᴏᴏᴅ Mᴏʀɴɪɴɢ Tᴀɢɢɪɴɢ Sᴛᴏᴘᴘᴇᴅ.")
    else:
        await message.reply("❌ Nᴏᴛʜɪɴɢ Rᴜɴɴɪɴɢ.")

# =================== GOOD AFTERNOON COMMANDS ===================

@app.on_message(filters.command("gatag") & filters.group)
async def gatag(_, message: Message):
    """Start Good Afternoon tagging"""
    chat_id = message.chat.id
    
    if chat_id in active_chats:
        return await message.reply("⚠️ Aғᴛᴇʀɴᴏᴏɴ Tᴀɢɢɪɴɢ Aʟʀᴇᴀᴅʏ Oɴ.")
    
    active_chats[chat_id] = True
    await message.reply("☀️ Aғᴛᴇʀɴᴏᴏɴ Tᴀɢɢɪɴɢ Sᴛᴀʀᴛᴇᴅ...")
    
    await tag_users(chat_id, GA_MESSAGES, "Aғᴛᴇʀɴᴏᴏɴ")

@app.on_message(filters.command("gastop") & filters.group)
async def gastop(_, message: Message):
    """Stop Good Afternoon tagging"""
    chat_id = message.chat.id
    
    if chat_id in active_chats:
        del active_chats[chat_id]
        await message.reply("🛑 Aғᴛᴇʀɴᴏᴏɴ Tᴀɢɢɪɴɢ Sᴛᴏᴘᴘᴇᴅ.")
    else:
        await message.reply("❌ Nᴏᴛʜɪɴɢ Rᴜɴɴɪɴɢ.")

# =================== GOOD NIGHT COMMANDS ===================

@app.on_message(filters.command("gntag") & filters.group)
async def gntag(_, message: Message):
    """Start Good Night tagging"""
    chat_id = message.chat.id
    
    if chat_id in active_chats:
        return await message.reply("⚠️ Nɪɢʜᴛ Tᴀɢɢɪɴɢ Aʟʀᴇᴀᴅʏ Oɴ.")
    
    active_chats[chat_id] = True
    await message.reply("🌙 Nɪɢʜᴛ Tᴀɢɢɪɴɢ Sᴛᴀʀᴛᴇᴅ...")
    
    await tag_users(chat_id, GN_MESSAGES, "Gᴏᴏᴅ Nɪɢʜᴛ")

@app.on_message(filters.command("gnstop") & filters.group)
async def gnstop(_, message: Message):
    """Stop Good Night tagging"""
    chat_id = message.chat.id
    
    if chat_id in active_chats:
        del active_chats[chat_id]
        await message.reply("🛑 Nɪɢʜᴛ Tᴀɢɢɪɴɢ Sᴛᴏᴘᴘᴇᴅ.")
    else:
        await message.reply("❌ Nᴏᴛʜɪɴɢ Rᴜɴɴɪɴɢ.")

# =================== UTILITY COMMANDS ===================

@app.on_message(filters.command("stopall") & filters.group)
async def stopall(_, message: Message):
    """Stop all active tagging in current chat"""
    chat_id = message.chat.id
    
    if chat_id in active_chats:
        del active_chats[chat_id]
        await message.reply("🛑 Aʟʟ Tᴀɢɢɪɴɢ Sᴛᴏᴘᴘᴇᴅ.")
    else:
        await message.reply("❌ Nᴏ Aᴄᴛɪᴠᴇ Tᴀɢɢɪɴɢ Fᴏᴜɴᴅ.")

@app.on_message(filters.command("taghelp") & filters.group)
async def taghelp(_, message: Message):
    """Show help message for tagging commands"""
    help_text = """
🏷️ **Tagging Commands Help**

**Good Morning:**
• `/gmtag` - Start Good Morning tagging
• `/gmstop` - Stop Good Morning tagging

**Good Afternoon:**
• `/gatag` - Start Good Afternoon tagging  
• `/gastop` - Stop Good Afternoon tagging

**Good Night:**
• `/gntag` - Start Good Night tagging
• `/gnstop` - Stop Good Night tagging

**Utility:**
• `/stopall` - Stop all active tagging
• `/taghelp` - Show this help message

**Note:** Only one tagging session can run per chat at a time.
"""
    await message.reply(help_text)

