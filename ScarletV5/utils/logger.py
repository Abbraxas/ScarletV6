from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from ScarletV5 import app
from ScarletV5.utils.database import is_on_off
from config import LOGGER_ID


async def play_logs(message, streamtype):
    if await is_on_off(2):
        logger_text = f"""<blockquote>
<b>{app.mention} ᴘʟᴧʏ ʟᴏɢ</b></blockquote>

<blockquote><b>ᴄʜᴧᴛ ιᴅ :</b> <code>{message.chat.id}</code>
<b>ᴄʜᴧᴛ ηᴧϻє :</b> {message.chat.title}
<b>ᴄʜᴧᴛ ᴜsєꝛηᴧϻє :</b> @{message.chat.username}</blockquote>

<blockquote><b>ᴜsєꝛ ιᴅ :</b> <code>{message.from_user.id}</code>
<b>ηᴧϻє :</b> {message.from_user.mention}
<b>ᴜsєꝛηᴧϻє :</b> @{message.from_user.username}</blockquote>

<blockquote><b>sᴛꝛєᴧϻᴛʏᴘє :</b> {streamtype}
<b>ǫᴜєꝛʏ :</b> {message.text.split(None, 1)[1]}</blockquote>"""
        if message.chat.id != LOGGER_ID:
            try:
                await app.send_message(
                    chat_id=LOGGER_ID,
                    text=logger_text,
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True,
                )
            except:
                pass
        return


async def clone_bot_logs(client, message, bot_mention, clone_logger_id, streamtype):

    if not clone_logger_id:
        print("[ERROR] clone_logger_id is missing!")
        return

    logger_text = f"""<blockquote>
<b>{bot_mention} ᴘʟᴧʏ ʟᴏɢ</b></blockquote>

<blockquote><b>ᴄʜᴧᴛ ιᴅ :</b> <code>{message.chat.id}</code>
<b>ᴄʜᴧᴛ ηᴧϻє :</b> {message.chat.title}
<b>ᴄʜᴧᴛ ᴜsєꝛηᴧϻє :</b> @{message.chat.username}</blockquote>

<blockquote><b>ᴜsєꝛ ιᴅ :</b> <code>{message.from_user.id}</code>
<b>ηᴧϻє :</b> {message.from_user.mention}
<b>ᴜsєꝛηᴧϻє :</b> @{message.from_user.username}</blockquote>

<blockquote><b>ǫᴜєꝛʏ :</b> {message.text.split(None, 1)[1]}
<b>sᴛꝛєᴧϻᴛʏᴘє :</b> {streamtype}</blockquote>"""

    if message.chat.id != clone_logger_id:
        try:
            await client.send_message(
                chat_id=int(clone_logger_id),
                text=logger_text,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
            )
        except Exception as e:
            print(f"[ERROR] Clone Bot Log Failed ({bot_mention}): {e}")

async def clone_main_logs(client, message, streamtype):

    query = (
        message.text.split(None, 1)[1]
        if len(message.text.split(None, 1)) > 1
        else "Unknown"
    )

    bot = await client.get_me()
    bot_username = bot.username or "UnknownBot"

    chat_username = message.chat.username
    if chat_username:
        chat_link = f"https://t.me/{chat_username}"
    else:
        chat_link = "Private Group"

    user_link = f"tg://user?id={message.from_user.id}"

    logger_text = f"""
<blockquote><b>@{bot_username} ᴘʟᴀʏ ʟᴏɢ</b></blockquote>

<blockquote><b>ᴄʜᴧᴛ ιᴅ :</b> <code>{message.chat.id}</code>
<b>ᴄʜᴧᴛ ηᴧϻє :</b> {message.chat.title}
<b>ᴄʜᴧᴛ ᴜsєꝛηᴧϻє :</b> @{message.chat.username}
<b>ᴄʜᴀᴛ ʟɪɴᴋ :</b> {chat_link}</blockquote>

<blockquote><b>ᴜsєꝛ ιᴅ :</b> <code>{message.from_user.id}</code>
<b>ηᴧϻє :</b> {message.from_user.mention}
<b>ᴜsєꝛηᴧϻє :</b> @{message.from_user.username}</blockquote>

<blockquote><b>ǫᴜєꝛʏ :</b> {message.text.split(None, 1)[1]}
<b>sᴛꝛєᴧϻᴛʏᴘє :</b> {streamtype}</blockquote>"""

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("👤 Played By", url=user_link),
                InlineKeyboardButton("💬 Open Group", url=chat_link if chat_username else user_link),
            ]
        ]
    )

    try:
        await app.send_message(
            chat_id=LOGGER_ID,
            text=logger_text,
            parse_mode=ParseMode.HTML,
            reply_markup=buttons,
            disable_web_page_preview=True,
        )
    except Exception as e:
        print(e)
