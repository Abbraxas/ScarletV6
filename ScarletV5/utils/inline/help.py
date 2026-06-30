from typing import Union
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from ScarletV5 import app
from pyrogram.enums import ButtonStyle



def help_pannel(_, START: Union[bool, int] = None):
    first = [
        [InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close", style=ButtonStyle.DANGER)]
    ]

    second = [
        [InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data="Axiom_Back", style=ButtonStyle.PRIMARY)]
    ]

    mark = second if START else first

    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text=_["H_B_1"], callback_data="help_callback hb1", style=ButtonStyle.SUCCESS),
                InlineKeyboardButton(text=_["H_B_2"], callback_data="help_callback hb2", style=ButtonStyle.SUCCESS),
                InlineKeyboardButton(text=_["H_B_3"], callback_data="help_callback hb3", style=ButtonStyle.SUCCESS),
            ],
            [
                InlineKeyboardButton(text=_["H_B_4"], callback_data="help_callback hb4", style=ButtonStyle.SUCCESS),
                InlineKeyboardButton(text=_["H_B_5"], callback_data="help_callback hb5", style=ButtonStyle.SUCCESS),
                InlineKeyboardButton(text=_["H_B_6"], callback_data="help_callback hb6", style=ButtonStyle.SUCCESS),
            ],
            [
                InlineKeyboardButton(text=_["H_B_7"], callback_data="help_callback hb7", style=ButtonStyle.SUCCESS),
                InlineKeyboardButton(text=_["H_B_8"], callback_data="help_callback hb8", style=ButtonStyle.SUCCESS),
                InlineKeyboardButton(text=_["H_B_9"], callback_data="help_callback hb9", style=ButtonStyle.SUCCESS),
            ],
            [
                InlineKeyboardButton(text=_["H_B_10"], callback_data="help_callback hb10", style=ButtonStyle.SUCCESS),
                InlineKeyboardButton(text=_["H_B_11"], callback_data="help_callback hb11", style=ButtonStyle.SUCCESS),
                InlineKeyboardButton(text=_["H_B_12"], callback_data="help_callback hb12", style=ButtonStyle.SUCCESS),
            ],
            [
                InlineKeyboardButton(text=_["H_B_13"], callback_data="help_callback hb13", style=ButtonStyle.SUCCESS),
                InlineKeyboardButton(text=_["H_B_14"], callback_data="help_callback hb14", style=ButtonStyle.SUCCESS),
                InlineKeyboardButton(text=_["H_B_15"], callback_data="help_callback hb15", style=ButtonStyle.SUCCESS),
            ],
            *mark,
        ]
    )
    return upl


def help_back_markup(_):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["BACK_BUTTON"],
                    callback_data="Axiom_Help", 
                    style=ButtonStyle.DANGER,
                )
            ]
        ]
    )


def private_help_panel(_):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["S_B_4"],
                    url=f"https://t.me/{app.username}?start=help", 
                    style=ButtonStyle.PRIMARY,
                )
            ]
        ]
    )


def first_page(_):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text=_["H_B_1"], callback_data="help_callback hb1", style=ButtonStyle.SUCCESS),
                InlineKeyboardButton(text=_["H_B_2"], callback_data="help_callback hb2", style=ButtonStyle.SUCCESS),
                InlineKeyboardButton(text=_["H_B_3"], callback_data="help_callback hb3", style=ButtonStyle.SUCCESS),
            ],
            [
                InlineKeyboardButton(text=_["H_B_11"], callback_data="help_callback hb11", style=ButtonStyle.SUCCESS),
                InlineKeyboardButton(text=_["H_B_8"], callback_data="help_callback hb8", style=ButtonStyle.SUCCESS),
                InlineKeyboardButton(text=_["H_B_6"], callback_data="help_callback hb6", style=ButtonStyle.SUCCESS),
            ],
            [
                InlineKeyboardButton(text=_["H_B_13"], callback_data="help_callback hb13", style=ButtonStyle.SUCCESS),
                InlineKeyboardButton(text=_["H_B_12"], callback_data="help_callback hb12", style=ButtonStyle.SUCCESS),
                InlineKeyboardButton(text=_["H_B_9"], callback_data="help_callback cloghelp", style=ButtonStyle.SUCCESS),
            ],
            [
                InlineKeyboardButton(text=_["H_B_10"], callback_data="help_callback hb10", style=ButtonStyle.SUCCESS),
                InlineKeyboardButton(text=_["H_B_14"], callback_data="help_callback hb14", style=ButtonStyle.SUCCESS),
                InlineKeyboardButton(text=_["H_B_15"], callback_data="help_callback hb15", style=ButtonStyle.SUCCESS),
            ],
            [
                InlineKeyboardButton(text="𝐏‌єꝛsσηᴧʟɪᴢє 𝐅‌σꝛɢє", callback_data="help_callback clone_start", style=ButtonStyle.PRIMARY),
                InlineKeyboardButton(text="𝐂‌ʟσηє 𝐖‌σꝛᴋsᴘᴧᴄє", callback_data="help_callback chelp", style=ButtonStyle.PRIMARY),
            ],
            [
                InlineKeyboardButton(text="⏭ 𝐍ᴇxᴛ", callback_data="help_next",),
            ],
            [
                InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close", style=ButtonStyle.DANGER),
            ],
        ]
    )


def second_page(_):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text=_["H_B_7"], callback_data="help_callback hb7", style=ButtonStyle.SUCCESS),
                InlineKeyboardButton(text=_["H_B_19"], callback_data="help_callback hb19", style=ButtonStyle.SUCCESS),
                InlineKeyboardButton(text=_["H_B_14"], callback_data="help_callback hb14", style=ButtonStyle.SUCCESS),
            ],
            [
                InlineKeyboardButton(text=_["H_B_15"], callback_data="help_callback hb15", style=ButtonStyle.SUCCESS),
                InlineKeyboardButton(text=_["H_B_16"], callback_data="help_callback hb16", style=ButtonStyle.SUCCESS),
                InlineKeyboardButton(text=_["H_B_17"], callback_data="help_callback hb17", style=ButtonStyle.SUCCESS),
            ],
            [
                InlineKeyboardButton(text=_["H_B_18"], callback_data="help_callback hb18", style=ButtonStyle.SUCCESS),
                InlineKeyboardButton(text=_["H_B_13"], callback_data="help_callback hb13", style=ButtonStyle.SUCCESS),
            ],
            [
                InlineKeyboardButton(text=_["H_B_20"], callback_data="help_callback hb20", style=ButtonStyle.SUCCESS),
                InlineKeyboardButton(text=_["H_B_22"], callback_data="help_callback hb22", style=ButtonStyle.SUCCESS),
            ],
            [
                InlineKeyboardButton(text=_["H_B_21"], callback_data="help_callback hb21", style=ButtonStyle.SUCCESS),
            ],
            [
                InlineKeyboardButton(text="⏮ 𝐁ᴀᴄᴋ", callback_data="help_back",),
            ],
            [
                InlineKeyboardButton(
                    text=_["BACK_BUTTON"],
                    callback_data="Axiom_Help", 
                    style=ButtonStyle.DANGER,
                )
            ],
        ]
    )
