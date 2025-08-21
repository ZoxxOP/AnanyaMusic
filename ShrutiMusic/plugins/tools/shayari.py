import random
import time
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from ShrutiMusic import app
from ShrutiMusic.utils.database import get_served_chats

# Dictionary to track user command usage for anti-spam
user_last_command_time = {}
user_command_count = {}
# Anti-spam settings
SPAM_THRESHOLD = 3  # Maximum commands allowed in time window
SPAM_WINDOW_SECONDS = 10  # Time window in seconds
COOLDOWN_TIME = 15  # Cooldown time in seconds

# Beautiful emojis and dividers for decoration
DECORATIVE_EMOJIS = ["✨", "💫", "🌟", "⭐", "🌠", "🌸", "🌺", "🌹", "💮", "🏵️", "🌻", "🥀", "💐"]
DIVIDERS = [
    "•✦───────────•✧•───────────✦•",
    "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━┓",
    "❃───•*¨*•.¸¸❁¸¸.•*¨*•───❃",
    "╭────────────────────╮",
    "ღ¸.•´.¸.•´¯`•.¸¸.•❤",
    "•° ★ °•",
    "═════════════",
    "─────※ ·❆· ※─────",
]

# Improved Shayari collection with better formatting
SHAYRI = [
    f"""╔══════════════════╗
☘️ **बहुत अच्छा लगता है तुझे सताना और फिर प्यार से तुझे मनाना।** ☘️

🥀 **Bahut aacha lagta hai tujhe satana Aur fir pyar se tujhe manana.** 🥀
╚══════════════════╝""",
    
    f"""╔══════════════════╗
☘️ **मेरी जिंदगी मेरी जान हो तुम मेरे सुकून का दुसरा नाम हो तुम।** ☘️

🥀 **Meri zindagi Meri jaan ho tum Mere sukoon ka Dusra naam ho tum.** 🥀
╚══════════════════╝""",
    
    f"""╔══════════════════╗
☘️ **तुम मेरी वो खुशी हो जिसके बिना, मेरी सारी खुशी अधूरी लगती है।** ☘️

🥀 **Tum Meri Wo Khushi Ho Jiske Bina, Meri Saari Khushi Adhuri Lagti Ha.** 🥀
╚══════════════════╝""",
    
    f"""╔══════════════════╗
☘️ **काश वो दिन जल्दी आए, जब तू मेरे साथ सात फेरो में बन्ध जाए।** ☘️

🥀 **Kash woh din jldi aaye Jb tu mere sath 7 feron me bndh jaye.** 🥀
╚══════════════════╝""",
    
    f"""╔══════════════════╗
☘️ **अपना हाथ मेरे दिल पर रख दो और अपना दिल मेरे नाम कर दो।** ☘️

🥀 **Apna hath mere dil pr rakh do aur apna dil mere naam kar do.** 🥀
╚══════════════════╝""",
    
    f"""╔══════════════════╗
☘️ **महादेव ना कोई गाड़ी ना कोई बंगला चाहिए सलामत रहे मेरा प्यार बस यही दुआ चाहिए।** ☘️

🥀 **Mahadev na koi gadi na koi bangla chahiye salamat rhe mera pyar bas yahi dua chahiye.** 🥀
╚══════════════════╝""",
    
    f"""╔══════════════════╗
☘️ **फिक्र तो होगी ना तुम्हारी इकलौती मोहब्बत हो तुम मेरी।** ☘️

🥀 **Fikr to hogi na tumhari ikloti mohabbat ho tum meri.** 🥀
╚══════════════════╝""",
    
    f"""╔══════════════════╗
☘️ **सुनो जानू आप सिर्फ किचन संभाल लेना आप को संभालने के लिए मैं हूं ना।** ☘️

🥀 **Suno jaanu aap sirf kitchen sambhal lena ap ko sambhlne ke liye me hun naa.** 🥀
╚══════════════════╝""",
    
    f"""╔══════════════════╗
☘️ **सौ बात की एक बात मुझे चाहिए बस तेरा साथ।** ☘️

🥀 **So bat ki ek bat mujhe chahiye bas tera sath.** 🥀
╚══════════════════╝""",
    
    f"""╔══════════════════╗
☘️ **बहुत मुश्किलों से पाया हैं तुम्हें, अब खोना नहीं चाहते, कि तुम्हारे थे तुम्हारे हैं अब किसी और के होना नहीं चाहते।** ☘️

🥀 **Bahut muskilon se paya hai tumhe Ab khona ni chahte ki tumhare they tumhare hai ab kisi or k hona nhi chahte.** 🥀
╚══════════════════╝""",
    
    f"""╔══════════════════╗
☘️ **बेबी बातें तो रोज करते है चलो आज रोमांस करते है।** ☘️

🥀 **Baby baten to roj karte hai chalo aaj romance karte hai..** 🥀
╚══════════════════╝""",
    
    f"""╔══════════════════╗
☘️ **सुबह शाम तुझे याद करते है हम और क्या बताएं की तुमसे कितना प्यार करते है हम।** ☘️

🥀 **Subha sham tujhe yad karte hai hum aur kya batayen ki tumse kitna pyar karte hai hum.** 🥀
╚══════════════════╝""",
    
    f"""╔══════════════════╗
☘️ **किसी से दिल लग जाने को मोहब्बत नहीं कहते जिसके बिना दिल न लगे उसे मोहब्बत कहते हैं।** ☘️

🥀 **Kisi se dil lag jane ko mohabbat nahi kehte jiske nina dil na lage use mohabbat kehte hai.** 🥀
╚══════════════════╝""",
    
    f"""╔══════════════════╗
☘️ **मेरे दिल के लॉक की चाबी हो तुम क्या बताएं जान मेरे जीने की एकलौती वजह हो तुम।** ☘️

🥀 **Mere dil ke lock ki chabi ho tum kya batayen jaan mere jeene ki eklauti wajah ho tum..** 🥀
╚══════════════════╝""",
    
    f"""╔══════════════════╗
☘️ **हम आपकी हर चीज़ से प्यार कर लेंगे, आपकी हर बात पर ऐतबार कर लेंगे, बस एक बार कह दो कि तुम सिर्फ मेरे हो, हम ज़िन्दगी भर आपका इंतज़ार कर लेंगे।** ☘️

🥀 **Hum apki har cheez se pyar kar lenge apki har baat par etvar kar lenge bas ek bar keh do ki tum sirf mere ho hum zindagi bhar apka intzaar kar lenge..** 🥀
╚══════════════════╝""",
]

# Command
SHAYRI_COMMAND = ["gf", "bf", "shayri", "sari", "shari", "love", "shayari"]

# Random emoji selector function
def get_random_emoji_pair():
    emoji = random.choice(DECORATIVE_EMOJIS)
    return emoji, emoji

# Random divider selector function
def get_random_divider():
    return random.choice(DIVIDERS)

# Anti-spam function
def is_spam(user_id):
    current_time = time.time()
    
    # Initialize if user not in dictionary
    if user_id not in user_last_command_time:
        user_last_command_time[user_id] = current_time
        user_command_count[user_id] = 1
        return False
    
    # Check if user is in cooldown
    time_diff = current_time - user_last_command_time[user_id]
    
    # Reset if window has passed
    if time_diff > SPAM_WINDOW_SECONDS:
        user_last_command_time[user_id] = current_time
        user_command_count[user_id] = 1
        return False
    
    # Increment command count
    user_command_count[user_id] += 1
    
    # Check if spam threshold reached
    if user_command_count[user_id] > SPAM_THRESHOLD:
        user_last_command_time[user_id] = current_time  # Start cooldown
        return True
    
    return False

# Command handlers with enhanced visual output
@app.on_message(filters.command(SHAYRI_COMMAND) & filters.group)
async def shayari_group(client: Client, message: Message):
    user_id = message.from_user.id
    
    # Check for spam
    if is_spam(user_id):
        cooldown_msg = f"⚠️ **Spam detected!** Please wait {COOLDOWN_TIME} seconds before using this command again."
        await message.reply_text(cooldown_msg)
        return
    
    # Get stylish components
    divider = get_random_divider()
    start_emoji, end_emoji = get_random_emoji_pair()
    
    # Create stylish header
    header = f"{divider}\n{start_emoji} **𝓢𝓱𝓪𝔂𝓪𝓻𝓲 𝓕𝓸𝓻 𝓨𝓸𝓾** {end_emoji}\n{divider}"
    
    # Get random shayari
    selected_shayari = random.choice(SHAYRI)
    
    # Create footer
    footer = f"{divider}\n💌 **𝓢𝓱𝓪𝓻𝓮𝓭 𝓦𝓲𝓽𝓱 𝓛𝓸𝓿𝓮** 💌\n{divider}"
    
    # Combine all components
    complete_message = f"{header}\n\n{selected_shayari}\n\n{footer}"
    
    # Create stylish inline keyboard
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("❣️ 𝐒𝐮𝐩𝐩𝐨𝐫𝐭 ❣️", url="https://t.me/AnanyaBotSupport"),
                InlineKeyboardButton("💖 𝐂𝐡𝐚𝐧𝐧𝐞𝐥 💖", url="https://t.me/AnanyaBots")
            ],
            [
                InlineKeyboardButton("🎁 𝐌𝐨𝐫𝐞 𝐒𝐡𝐚𝐲𝐚𝐫𝐢 🎁", callback_data="more_shayari")
            ]
        ]
    )
    
    await message.reply_text(
        text=complete_message,
        reply_markup=keyboard,
        disable_web_page_preview=True
    )

@app.on_message(filters.command(SHAYRI_COMMAND) & filters.private)
async def shayari_private(client: Client, message: Message):
    user_id = message.from_user.id
    
    # Check for spam
    if is_spam(user_id):
        cooldown_msg = f"⚠️ **Spam detected!** Please wait {COOLDOWN_TIME} seconds before using this command again."
        await message.reply_text(cooldown_msg)
        return
    
    # Get stylish components
    divider = get_random_divider()
    start_emoji, end_emoji = get_random_emoji_pair()
    
    # Create stylish header
    header = f"{divider}\n{start_emoji} **Shayri For You** {end_emoji}\n{divider}"
    
    # Get random shayari
    selected_shayari = random.choice(SHAYRI)
    
    # Create footer
    footer = f"{divider}\n💌 **Shared with Love** 💌\n{divider}"
    
    # Combine all components
    complete_message = f"{header}\n\n{selected_shayari}\n\n{footer}"
    
    # Create stylish inline keyboard
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("❣️ 𝐒𝐮𝐩𝐩𝐨𝐫𝐭 ❣️", url="https://t.me/AnanyaBotSupport"),
                InlineKeyboardButton("💖 𝐂𝐡𝐚𝐧𝐧𝐞𝐥 💖", url="https://t.me/AnanyaBots")
            ],
            [
                InlineKeyboardButton("🎁 𝐌𝐨𝐫𝐞 𝐒𝐡𝐚𝐲𝐚𝐫𝐢 🎁", callback_data="more_shayari")
            ]
        ]
    )
    
    await message.reply_text(
        text=complete_message,
        reply_markup=keyboard,
        disable_web_page_preview=True
    )

# Callback handler for "More Shayari" button
@app.on_callback_query(filters.regex("more_shayari"))
async def more_shayari_callback(client, callback_query):
    user_id = callback_query.from_user.id
    
    # Check for spam
    if is_spam(user_id):
        await callback_query.answer("Please wait a moment before requesting more shayari.", show_alert=True)
        return
    
    # Get stylish components
    divider = get_random_divider()
    start_emoji, end_emoji = get_random_emoji_pair()
    
    # Create stylish header
    header = f"{divider}\n{start_emoji} **New Shayri For You** {end_emoji}\n{divider}"
    
    # Get random shayari (different from previous)
    selected_shayari = random.choice(SHAYRI)
    
    # Create footer
    footer = f"{divider}\n💌 **Shared with Love** 💌\n{divider}"
    
    # Combine all components
    complete_message = f"{header}\n\n{selected_shayari}\n\n{footer}"

    # Create stylish inline keyboard
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("❣️ 𝐒𝐮𝐩𝐩𝐨𝐫𝐭 ❣️", url="https://t.me/AnanyaBotSupport"),
                InlineKeyboardButton("💖 𝐂𝐡𝐚𝐧𝐧𝐞𝐥 💖", url="https://t.me/AnanyaBots")
            ],
            [
                InlineKeyboardButton("🎁 𝐌𝐨𝐫𝐞 𝐒𝐡𝐚𝐲𝐚𝐫𝐢 🎁", callback_data="more_shayari")
            ]
        ]
    )
    
    try:
        await callback_query.edit_message_text(
            text=complete_message,
            reply_markup=keyboard,
            disable_web_page_preview=True
        )
        await callback_query.answer("Enjoy your new shayari! ❤️")
    except Exception as e:
        await callback_query.answer("Something went wrong. Please try again.")

# Module info
__MODULE__ = "Sʜᴀʏᴀʀɪ"
__HELP__ = """
/ɢғ, /ʙғ, /sʜᴀʏʀɪ, /sʜᴀʏᴀʀɪ, /sᴀʀɪ, /sʜᴀʀɪ, /ʟᴏᴠᴇ: 

✨ **Gᴇᴛ ᴀ ʙᴇᴀᴜᴛɪғᴜʟʟʏ ғᴏʀᴍᴀᴛᴛᴇᴅ ʀᴀɴᴅᴏᴍ Sʜᴀʏᴀʀɪ** ✨

📋 **Fᴇᴀᴛᴜʀᴇs:**
• Sᴛʏʟɪsʜ ғᴏʀᴍᴀᴛᴛɪɴɢ ᴡɪᴛʜ ᴅᴇᴄᴏʀᴀᴛɪᴠᴇ ᴇʟᴇᴍᴇɴᴛs
• "Mᴏʀᴇ Sʜᴀʏᴀʀɪ" ʙᴜᴛᴛᴏɴ ᴛᴏ ɢᴇᴛ ᴀ ɴᴇᴡ sʜᴀʏᴀʀɪ ɪɴsᴛᴀɴᴛʟʏ
• Wᴏʀᴋs ɪɴ ʙᴏᴛʜ ᴘʀɪᴠᴀᴛᴇ ᴀɴᴅ ɢʀᴏᴜᴘ ᴄʜᴀᴛs
• Aɴᴛɪ-sᴘᴀᴍ ᴘʀᴏᴛᴇᴄᴛɪᴏɴ ᴛᴏ ᴘʀᴇᴠᴇɴᴛ ᴀʙᴜsᴇ

💫 **Usᴀɢᴇ:** Sɪᴍᴘʟʏ sᴇɴᴅ ᴀɴʏ ᴏғ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅs ʟɪsᴛᴇᴅ ᴀʙᴏᴠᴇ ᴀɴᴅ ᴇɴᴊᴏʏ ᴀ ʙᴇᴀᴜᴛɪғᴜʟ sʜᴀʏᴀʀɪ!
"""
