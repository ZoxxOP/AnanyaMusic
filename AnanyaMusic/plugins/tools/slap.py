import logging
import html
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message
from pyrogram.errors import ChatWriteForbidden, ChatRestricted, RPCError
from AnanyaMusic import app

log = logging.getLogger(__name__)

API_URL = "https://api.waifu.pics"

# ✅ Prepare a requests session with automatic retries
session = requests.Session()
retries = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[502, 503, 504, 522, 524],
    allowed_methods=["GET"]
)
adapter = HTTPAdapter(max_retries=retries)
session.mount("http://", adapter)
session.mount("https://", adapter)

# ✅ SFW Action Categories (Safe For Work)
sfw_actions = {
    "waifu": "🌸", "neko": "🐱", "shinobu": "🍵", "megumin": "✨", "bully": "😈",
    "cuddle": "🤗", "cry": "😢", "hug": "🫂", "awoo": "🐺", "kiss": "😘",
    "lick": "👅", "pat": "🖐", "smug": "😏", "bonk": "🔨", "yeet": "📤",
    "blush": "😊", "smile": "😄", "wave": "👋", "highfive": "✋", "handhold": "🤝",
    "nom": "🍽", "bite": "😬", "glomp": "🫶", "slap": "😤", "kill": "💀",
    "kick": "🥾", "happy": "😁", "wink": "😉", "poke": "👉", "dance": "💃",
    "cringe": "😬"
}

# ✅ NSFW Action Categories (Not Safe For Work)
nsfw_actions = {
    "waifu": "🌸", "neko": "🐱", "trap": "👧", "blowjob": "😶‍🌫️"
}

def html_user_mention(user) -> str:
    """Return an HTML mention for the given user."""
    if not user:
        return "someone"
    name = html.escape(user.first_name or "User", quote=True)
    return f'<a href="tg://user?id={user.id}">{name}</a>'

def build_caption(sender, category: str, emoji: str, replied_user=None) -> str:
    """Build the action caption with mentions and emojis."""
    sender_mention = html_user_mention(sender)
    category_esc = html.escape(category, quote=True)
    emoji_esc = html.escape(emoji, quote=True)

    if replied_user:
        replied_mention = html_user_mention(replied_user)
        return f"{sender_mention} sent <b>{category_esc}</b> to {replied_mention} {emoji_esc}"
    return f"{sender_mention} is feeling <b>{category_esc}</b> {emoji_esc}"

async def safe_reply_animation(message: Message, animation_url: str, caption: str):
    """Safely reply with an animation and handle possible errors."""
    try:
        await message.reply_animation(
            animation=animation_url,
            caption=caption,
            parse_mode=ParseMode.HTML,  # ✅ Fixed from "html"
            disable_notification=False
        )
        return True
    except (ChatWriteForbidden, ChatRestricted):
        log.warning("[Waifu.pics] Chat write restricted: %s", message.chat.id if message.chat else "unknown")
    except RPCError as e:
        log.warning("[Waifu.pics] Telegram RPC error in chat %s: %s", message.chat.id if message.chat else "unknown", e)
    except Exception as e:
        log.exception("[Waifu.pics] Unexpected error sending animation: %s", e)
    return False

async def safe_reply_text(message: Message, text: str):
    """Safely reply with text and handle possible errors."""
    try:
        await message.reply_text(text, disable_web_page_preview=True)
        return True
    except (ChatWriteForbidden, ChatRestricted):
        log.warning("[Waifu.pics] Chat write restricted (text): %s", message.chat.id if message.chat else "unknown")
    except RPCError as e:
        log.warning("[Waifu.pics] Telegram RPC error (text) in chat %s: %s", message.chat.id if message.chat else "unknown", e)
    except Exception as e:
        log.exception("[Waifu.pics] Unexpected error sending text: %s", e)
    return False

async def send_action_image(client, message: Message, action_type: str, category: str, emoji: str):
    """Fetch an action image from the API and send it to the user."""
    if not (message and message.from_user):
        log.info("[Waifu.pics] Ignoring message without from_user in chat %s", message.chat.id if message.chat else "unknown")
        return

    try:
        r = session.get(f"{API_URL}/{action_type}/{category}", timeout=15)
        if r.status_code != 200:
            await safe_reply_text(message, "❌ Failed to fetch the image from the server.")
            return

        image_url = (r.json() or {}).get("url")
        if not image_url:
            await safe_reply_text(message, "❌ No image was returned by the API.")
            return

        replied_user = message.reply_to_message.from_user if (message.reply_to_message and message.reply_to_message.from_user) else None
        caption = build_caption(message.from_user, category, emoji, replied_user)

        sent = await safe_reply_animation(message, image_url, caption)
        if not sent:
            return

    except requests.exceptions.Timeout:
        log.warning("[Waifu.pics] Request timed out for %s/%s", action_type, category)
        await safe_reply_text(message, "⚠️ The image server took too long to respond. Please try again later.")
    except Exception as e:
        log.exception("[Waifu.pics] Fatal error: %s", e)
        await safe_reply_text(message, "❌ An unexpected error occurred while processing your request.")

# ✅ Register SFW handlers
for _category, _emoji in sfw_actions.items():
    @app.on_message(filters.command(_category))
    async def _sfw_handler(client, message: Message, category=_category, emoji=_emoji):
        await send_action_image(client, message, "sfw", category, emoji)

# ✅ Register NSFW handlers
for _category, _emoji in nsfw_actions.items():
    @app.on_message(filters.command(_category))
    async def _nsfw_handler(client, message: Message, category=_category, emoji=_emoji):
        await send_action_image(client, message, "nsfw", category, emoji)
