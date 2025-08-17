from pyrogram.types import InlineKeyboardButton
import config
from ShrutiMusic import app

def start_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_1"], url=f"https://t.me/{app.username}?startgroup=true"
            ),
            InlineKeyboardButton(text=_["S_B_2"], url=config.SUPPORT_GROUP),
        ],
        [
            InlineKeyboardButton(text=_["E_X_1"], callback_data="show_video_panel"),
            InlineKeyboardButton(text=_["S_B_11"], callback_data="about_page")  # About button
        ],
    ]
    return buttons

def private_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_3"],
                url=f"https://t.me/{app.username}?startgroup=true",
            )
        ],
        [
            InlineKeyboardButton(
                text=_["S_B_11"],
                callback_data="about_page"
            ),
            InlineKeyboardButton(
                text=_["S_B_12"],
                callback_data="owner_page"
            )
        ],
        [
            InlineKeyboardButton(
                text=_["E_X_1"],
                callback_data="show_video_panel"
            ),
            InlineKeyboardButton(text=_["S_B_5"], user_id=config.OWNER_ID),
        ],
        [
            InlineKeyboardButton(text=_["S_B_4"], callback_data="help_page_1")
        ],
    ]
    return buttons

def about_panel(_):
    buttons = [
        [
            InlineKeyboardButton(text=_["S_B_6"], url=config.SUPPORT_CHANNEL),
            InlineKeyboardButton(text=_["S_B_2"], url=config.SUPPORT_GROUP),
        ],
        [
            InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data="settingsback_helper")
        ]
    ]
    return buttons

def owner_panel(_):
    buttons = [
        [
            InlineKeyboardButton(text=_["S_H_1"], url=config.INSTAGRAM),
            InlineKeyboardButton(text=_["S_H_2"], url=config.YOUTUBE),
        ],
        [
            InlineKeyboardButton(text=_["S_H_3"], url=config.GITHUB),
            InlineKeyboardButton(text=_["S_H_4"], url=config.DONATE),
        ],
        [
            InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data="settingsback_helper")
        ]
    ]
    return buttons

