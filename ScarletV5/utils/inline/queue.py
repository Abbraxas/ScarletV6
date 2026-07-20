import random
from typing import Union
from ScarletV5 import app
from ScarletV5.utils.formatters import time_to_seconds
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import ButtonStyle

def random_style():
    return random.choice([
        ButtonStyle.SUCCESS,
        ButtonStyle.DANGER,
        ButtonStyle.PRIMARY
    ])

def queue_markup(
    _,
    DURATION,
    CPLAY,
    videoid,
    played: Union[bool, int] = None,
    dur: Union[bool, int] = None,
):
    not_dur = [
        [
            InlineKeyboardButton(
                text=_["QU_B_1"],
                callback_data=f"GetQueued {CPLAY}|{videoid}", style=random_style(),
            ),
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data="close",
                style=ButtonStyle.DANGER,
            ),
        ]
    ]
    dur = [
        [
            InlineKeyboardButton(
                text=_["QU_B_2"].format(played, dur),
                callback_data="GetTimer",
                style=random_style(),
            )
        ],
        [
            InlineKeyboardButton(
                text=_["QU_B_1"],
                callback_data=f"GetQueued {CPLAY}|{videoid}", style=random_style(),
            ),
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data="close",
                style=ButtonStyle.DANGER,
            ),
        ],
    ]
    upl = InlineKeyboardMarkup(not_dur if DURATION == "Unknown" else dur)
    return upl


def queue_back_markup(_, CPLAY):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["BACK_BUTTON"],
                    callback_data=f"queue_back_timer {CPLAY}", style=random_style(),
                ),
                InlineKeyboardButton(
                    text=_["CLOSE_BUTTON"],
                    callback_data="close",
                    style=ButtonStyle.DANGER,
                ),
            ]
        ]
    )
    return upl


def aq_markup(_, chat_id):
    buttons = [
        [
            
            InlineKeyboardButton(text="ᴘᴧυsє", callback_data=f"ADMIN Pause|{chat_id}", style=random_style()),
            InlineKeyboardButton(text="sᴋɪᴘ", callback_data=f"ADMIN Skip|{chat_id}", style=random_style()),
            InlineKeyboardButton(text="єηᴅ", callback_data=f"ADMIN Stop|{chat_id}", style=random_style()),
            InlineKeyboardButton(text="ꝛєsυϻє", callback_data=f"ADMIN Resume|{chat_id}", style=random_style()),
        ],
        [
            InlineKeyboardButton(text="ᴧᴅᴅ ϻєєʜ", url=f"https://t.me/{app.username}?startgroup=true", style=random_style()),
            InlineKeyboardButton(text="ꝛєᴘʟᴧʏ", callback_data=f"ADMIN Replay|{chat_id}", style=random_style()),
            InlineKeyboardButton(text="ᴄʟσsє", callback_data="close", style=ButtonStyle.DANGER),
        ]
    ]
    return buttons


def queuemarkup(_, vidid, chat_id):

    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_5"],
                url=f"https://t.me/{app.username}?startgroup=true",
                style=random_style()
            ),
        ],
        [
            InlineKeyboardButton(
                text="ᴘᴀᴜsᴇ",
                callback_data=f"ADMIN Pause|{chat_id}", style=random_style(),
            ),
            InlineKeyboardButton(text="sᴛᴏᴘ", callback_data=f"ADMIN Stop|{chat_id}", style=random_style()),
            InlineKeyboardButton(text="sᴋɪᴘ", callback_data=f"ADMIN Skip|{chat_id}", style=random_style()),
        ],
        [
            InlineKeyboardButton(
                text="ʀᴇsᴜᴍᴇ", callback_data=f"ADMIN Resume|{chat_id}", style=random_style()
            ),
            InlineKeyboardButton(
                text="ʀᴇᴘʟᴀʏ", callback_data=f"ADMIN Replay|{chat_id}", style=random_style()
            ),
        ],
        [
            InlineKeyboardButton(
                text="๏ ᴍᴏʀᴇ ๏",
                url="https://t.me/ScarletSupportChat",
                style=random_style(),
            ),
        ],
    ]

    return buttons
