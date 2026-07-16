import time
import random
from datetime import datetime

import psutil
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from ScarletV5 import app
from config import PING_IMG_URL, STREAMI_PICS
from .utils import StartTime
from ScarletV5.utils import get_readable_time
from ScarletV5.utils.decorators.language import language
from pyrogram.enums import ButtonStyle

def random_style():
    return random.choice([
        ButtonStyle.SUCCESS,
        ButtonStyle.DANGER,
        ButtonStyle.PRIMARY
    ])
    
APP_LINK = f"https://t.me/newbot/ScarletCloneBot/"


@Client.on_message(filters.command("clone"))
@language
async def ping_clone(client: Client, message: Message, _):
    bot = await client.get_me()


    hmm = await message.reply_photo(
        photo=random.choice(STREAMI_PICS), caption=_["NO_CLONE_MSG"],
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("𝐂‌ꝛєᴧᴛє ᴧ 𝐌‌υsɪᴄ 𝐁‌σᴛ 𝐍‌σᴡ", url=APP_LINK, style=random_style())]
            ]
        )
    )
