from datetime import datetime

from pyrogram import filters
from pyrogram.types import Message
from config import *
from ScarletV5 import app
from ScarletV5.core.call import Axiom
from ScarletV5.utils import bot_sys_stats
from ScarletV5.utils.decorators.language import language
from ScarletV5.utils.inline import supp_markup
from config import BANNED_USERS
from config import PING_IMG_URL


@app.on_message(filters.command("ping", prefixes=["/", "!", "%", ",", "", ".", "@", "#"]) & ~BANNED_USERS)
@language
async def ping_com(client, message: Message, _):
    start = datetime.now()
    response = await message.reply_photo(
        photo=PING_IMG_URL,
        caption=_["ping_1"].format(app.mention),
    )
    pytgping = await Axiom.ping()
    UP, CPU, RAM, DISK = await bot_sys_stats()
    resp = (datetime.now() - start).microseconds / 1000
    await response.edit_text(
        _["ping_2"].format(resp, app.mention, UP, RAM, CPU, DISK, pytgping),
        reply_markup=supp_markup(_),
    )
