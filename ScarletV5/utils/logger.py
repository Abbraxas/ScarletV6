from pyrogram.enums import ParseMode, ButtonStyle
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from ScarletV5 import app
from ScarletV5.utils.database import is_on_off
from config import LOGGER_ID


async def play_logs(client, message, streamtype):
    try:
        invite = await client.export_chat_invite_link(message.chat.id)
    except:
        if message.chat.username:
            invite = f"https://t.me/{message.chat.username}"
        else:
            invite = None
    user_link = f"tg://user?id={message.from_user.id}"
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

    buttons = []
    
    buttons.append(
        [InlineKeyboardButton("𝐈ɴɪᴛɪᴀᴛᴏʀ", url=user_link, style=ButtonStyle.SUCCESS)]
    )
    
    if invite:
        buttons[0].append(
            InlineKeyboardButton("𝐖‌ʜєꝛє ?", url=invite, style=ButtonStyle.PRIMARY)
        )
    
    buttons = InlineKeyboardMarkup(buttons)

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

    try:
        invite = await client.export_chat_invite_link(message.chat.id)
    except:
        if message.chat.username:
            invite = f"https://t.me/{message.chat.username}"
        else:
            invite = None
    chat_username = message.chat.username
    if chat_username:
        chat_link = f"https://t.me/{chat_username}"
    else:
        chat_link = "Private Group"

    user_link = f"tg://user?id={message.from_user.id}"

    logger_text = f"""
<blockquote><b>@{bot_username} ᴘʟᴀʏ ʟᴏɢ</b></blockquote>
<blockquote expandable><b>ᴄʜᴧᴛ ιᴅ :</b> <code>{message.chat.id}</code>
<b>ᴄʜᴧᴛ ηᴧϻє :</b> {message.chat.title}
<b>ᴄʜᴧᴛ ᴜsєꝛηᴧϻє :</b> @{message.chat.username}
<b>ᴄʜᴀᴛ ʟɪɴᴋ :</b> {invite}</blockquote>
<blockquote><b>ᴜsєꝛ ιᴅ :</b> <code>{message.from_user.id}</code>
<b>ηᴧϻє :</b> {message.from_user.mention}
<b>ᴜsєꝛηᴧϻє :</b> @{message.from_user.username}</blockquote>
<blockquote><b>ǫᴜєꝛʏ :</b> {query}
<b>sᴛꝛєᴧϻᴛʏᴘє :</b> {streamtype}</blockquote>"""

    buttons = []
    
    buttons.append(
        [InlineKeyboardButton("𝐈ɴɪᴛɪᴀᴛᴏʀ", url=user_link, style=ButtonStyle.DANGER)]
    )
    
    if invite:
        buttons[0].append(
            InlineKeyboardButton("𝐖‌ʜєꝛє ?", url=invite, style=ButtonStyle.PRIMARY)
        )
    
    buttons = InlineKeyboardMarkup(buttons)

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
