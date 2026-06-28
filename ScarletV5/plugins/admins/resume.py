from pyrogram import filters
from pyrogram.types import Message

from ScarletV5 import app
from ScarletV5.core.call import Axiom
from ScarletV5.utils.database import is_music_playing, music_on
from ScarletV5.utils.decorators import AdminRightsCheck
from ScarletV5.utils.inline import close_markup
from config import BANNED_USERS


@app.on_message(filters.command(["resume", "cresume"]) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def resume_com(cli, message: Message, _, chat_id):
    if await is_music_playing(chat_id):
        return await message.reply_text(_["admin_3"])
    await music_on(chat_id)
    await Axiom.resume_stream(chat_id)
    await message.reply_text(
        _["admin_4"].format(message.from_user.mention), reply_markup=close_markup(_)
    )
