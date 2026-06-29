import time
import random
import asyncio
import logging
from pyrogram import filters, Client
from pyrogram.enums import ChatType, ButtonStyle
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pyrogram.errors import MessageNotModified
from py_yt import VideosSearch

import config
from ScarletV5 import app
from ScarletV5.misc import _boot_
from ScarletV5.plugins.sudo.sudoers import sudoers_list
from ScarletV5.utils.formatters import get_readable_time

# ✅ CONFIG IMPORTS
from config import BANNED_USERS, OWNER_ID, STREAMI_PICS, CMBOT, EFFECT_ID

from ScarletV5.utils.decorators.language import LanguageStart
from strings import get_string
from ScarletV5.utils.database.clonedb import get_owner_id_from_db, get_cloned_support_chat, get_cloned_support_channel
from ScarletV5.cplugin.setinfo import get_logging_status, get_log_channel
from ScarletV5.utils.database import add_served_user_clone, add_served_chat_clone
from ScarletV5.utils.database import clonebotdb

# Initialize logging
LOG = logging.getLogger(__name__)

# =====================================================================
# DB Fetchers
# =====================================================================

def get_start_image(bot_id):
    d = clonebotdb.find_one({"bot_id": bot_id}) or {}
    return d.get("start_image")

def get_start_caption(bot_id):
    d = clonebotdb.find_one({"bot_id": bot_id}) or {}
    return d.get("start_caption")

def get_start_button(bot_id):
    d = clonebotdb.find_one({"bot_id": bot_id}) or {}
    return d.get("start_button")

def get_start_video(bot_id):
    d = clonebotdb.find_one({"bot_id": bot_id}) or {}
    return d.get("start_video")

# =====================================================================
# START PRIVATE (PM) - With Effects & Spoiler ✅
# =====================================================================

@Client.on_message(filters.command("start") & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
    a = await client.get_me()
    bot_id = a.id
    await add_served_user_clone(message.from_user.id, bot_id)

    # 1. LOADING ANIMATION
    loading = await message.reply_text(random.choice(CMBOT))
    
    animations = ["<b>ʟᴏᴀᴅɪɴɢ</b>", "<b>ʟᴏᴀᴅɪɴɢ.</b>", "<b>ʟᴏᴀᴅɪɴɢ..</b>", "<b>ʟᴏᴀᴅɪɴɢ...</b>"]
    for anim in animations:
        await asyncio.sleep(0.1)
        try:
            await loading.edit_text(anim)
        except:
            pass

    # DATA FETCHING
    C_BOT_OWNER_ID = get_owner_id_from_db(bot_id)
    C_SUPPORT_CHAT_USERNAME = await get_cloned_support_chat(bot_id)
    C_SUPPORT_CHANNEL_USERNAME = await get_cloned_support_channel(bot_id)
    
    C_SUPPORT_CHAT = f"https://t.me/{C_SUPPORT_CHAT_USERNAME}"
    C_SUPPORT_CHANNEL = f"https://t.me/{C_SUPPORT_CHANNEL_USERNAME}"
    
    # OWNER PROFILE LINK
    try:
        owner_info = await client.get_users(C_BOT_OWNER_ID)
        OWNER_URL = f"https://t.me/{owner_info.username}" if owner_info.username else f"tg://openmessage?user_id={C_BOT_OWNER_ID}"
    except:
        OWNER_URL = f"tg://openmessage?user_id={C_BOT_OWNER_ID}"

    try:
        await loading.delete()
    except:
        pass

    # 2. INLINE ARGUMENTS
    if len(message.text.split()) > 1:
        arg = message.text.split(None, 1)[1]
        if arg.startswith("help"):
            keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(_["S_B_9"], url=C_SUPPORT_CHAT, style=ButtonStyle.PRIMARY)]])
            return await message.reply_photo(random.choice(STREAMI_PICS), caption=_["help_1"].format(C_SUPPORT_CHAT), reply_markup=keyboard, has_spoiler=True)
        if arg.startswith("sud"):
            return await sudoers_list(client=client, message=message, _=_)
        if arg.startswith("inf"):
            m = await message.reply_text("🔎")
            q = arg.replace("info_", "", 1)
            try:
                results = await VideosSearch(f"https://www.youtube.com/watch?v={q}", limit=1).next()
                result = results["result"][0]
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                caption = _["start_6"].format(result["title"], result["duration"], result["viewCount"]["short"], result["publishedTime"], result["channel"]["link"], result["channel"]["name"], a.mention)
                key = InlineKeyboardMarkup([[InlineKeyboardButton(_["S_B_8"], url=result["link"], style=ButtonStyle.PRIMARY), InlineKeyboardButton(_["S_B_9"], url=C_SUPPORT_CHAT, style=ButtonStyle.PRIMARY)]])
                await m.delete()
                return await message.reply_photo(thumbnail, caption=caption, reply_markup=key, has_spoiler=True)
            except Exception as e:
                LOG.error(e)
                return await m.edit_text("❌ Error fetching info.")

    # 3. MAIN START UI
    out = [
        [InlineKeyboardButton(_["S_B_16"], url=f"https://t.me/{a.username}?startgroup=true", style=ButtonStyle.PRIMARY)],
        [InlineKeyboardButton(_["S_B_13"], url=C_SUPPORT_CHAT, style=ButtonStyle.PRIMARY), InlineKeyboardButton(_["S_B_14"], url=C_SUPPORT_CHANNEL, style=ButtonStyle.PRIMARY)],
        [InlineKeyboardButton(_["C_B_2"], url=OWNER_URL, style=ButtonStyle.SUCCESS)], 
        [InlineKeyboardButton(_["S_B_15"], callback_data="Axiom_Help", style=ButtonStyle.DANGER)]
    ]

    start_video = get_start_video(bot_id)
    start_img = get_start_image(bot_id)
    custom_caption = get_start_caption(bot_id)
    custom_button = get_start_button(bot_id)

    caption = custom_caption if custom_caption else _["c_start_2"].format(
        message.from_user.mention, a.mention, app.name, f"https://t.me/{app.username}",
        app.name, f"https://t.me/{app.username}", C_SUPPORT_CHANNEL_USERNAME, C_SUPPORT_CHAT_USERNAME
    )

    if custom_button and custom_button.get("text"):
        out.insert(0, [InlineKeyboardButton(custom_button["text"], url=custom_button["url"], style=ButtonStyle.PRIMARY)])

    effect = random.choice(EFFECT_ID)
    markup = InlineKeyboardMarkup(out)

    # SENDING WITH SPOILER
    if start_video:
        try:
            return await message.reply_video(start_video, caption=caption, reply_markup=markup, has_spoiler=True)
        except:
            pass
    
    photo = start_img if start_img else random.choice(STREAMI_PICS)
    await message.reply_photo(photo, caption=caption, reply_markup=markup, has_spoiler=True)

# =====================================================================
# GROUP START
# =====================================================================

@Client.on_message(filters.command("start") & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    a = await client.get_me()
    uptime = get_readable_time(int(time.time() - _boot_))
    C_SUPPORT_CHAT_USER = await get_cloned_support_chat(a.id)
    C_SUPPORT_CHAT = f"https://t.me/{C_SUPPORT_CHAT_USER}"

    out = [[InlineKeyboardButton(_["S_B_1"], url=f"https://t.me/{a.username}?startgroup=true", style=ButtonStyle.PRIMARY),
            InlineKeyboardButton(_["S_B_2"], url=C_SUPPORT_CHAT, style=ButtonStyle.PRIMARY)]]
    
    caption = _["start_1"].format(a.mention, uptime)
    start_video = get_start_video(a.id)
    start_img = get_start_image(a.id)

    markup = InlineKeyboardMarkup(out)
    # Group mein bhi spoiler add kar diya gaya hai
    if start_video:
        try:
            return await message.reply_video(start_video, caption=caption, reply_markup=markup, has_spoiler=True)
        except:
            pass
    
    await message.reply_photo(start_img if start_img else random.choice(STREAMI_PICS), caption=caption, reply_markup=markup, has_spoiler=True)
    await add_served_chat_clone(message.chat.id, a.id)

# =====================================================================
# MANAGEMENT COMMANDS (UNTOUCHED)
# =====================================================================

@Client.on_message(filters.command("viewstartsettings") & ~BANNED_USERS)
async def view_start_settings(client, message):
    bot_id = (await client.get_me()).id
    img = "✅ Set" if get_start_image(bot_id) else "❌ Not Set"
    vid = "✅ Set" if get_start_video(bot_id) else "❌ Not Set"
    cap = get_start_caption(bot_id) or "❌ Not Set"
    btn = get_start_button(bot_id) or {"text": "❌ Not Set", "url": "N/A"}
    await message.reply_text(f"**📌 START SETTINGS**\n\n**Image:** `{img}`\n**Video:** `{vid}`\n**Caption:** `{cap[:50]}...` \n**Button:** `{btn['text']}`")

@Client.on_message(filters.command("resetstartsetting") & ~BANNED_USERS)
async def reset_start_settings(client, message):
    bot_id = (await client.get_me()).id
    owner = get_owner_id_from_db(bot_id)
    if message.from_user.id not in [OWNER_ID, owner]: return await message.reply_text("Owner Only!")
    clonebotdb.update_one({"bot_id": bot_id}, {"$unset": {"start_image": "", "start_video": "", "start_caption": "", "start_button": ""}})
    await message.reply_text("🔄 Settings Reset!")

@Client.on_message(filters.command("setstartimg") & ~BANNED_USERS)
async def set_start_image_cmd(client, message):
    bot_id = (await client.get_me()).id
    if message.reply_to_message and message.reply_to_message.photo:
        file_id = message.reply_to_message.photo.file_id
    elif len(message.command) > 1: file_id = message.command[1]
    else: return await message.reply_text("Reply to a photo.")
    clonebotdb.update_one({"bot_id": bot_id}, {"$set": {"start_image": file_id}}, upsert=True)
    await message.reply_text("✅ Image Set!")

@Client.on_message(filters.command("setstartcaption") & ~BANNED_USERS)
async def set_start_caption_cmd(client, message):
    bot_id = (await client.get_me()).id
    text = message.reply_to_message.text if message.reply_to_message else (message.text.split(None, 1)[1] if len(message.command) > 1 else None)
    if not text: return await message.reply_text("Give Text.")
    clonebotdb.update_one({"bot_id": bot_id}, {"$set": {"start_caption": text}}, upsert=True)
    await message.reply_text("✅ Caption Set!")

@Client.on_message(filters.command("setstartbutton") & ~BANNED_USERS)
async def set_start_button_cmd(client, message):
    bot_id = (await client.get_me()).id
    data = message.reply_to_message.text if message.reply_to_message else (message.text.split(None, 1)[1] if len(message.command) > 1 else None)
    if not data or "-" not in data: return await message.reply_text("Format: `Text - URL`")
    txt, url = data.split("-", 1)
    clonebotdb.update_one({"bot_id": bot_id}, {"$set": {"start_button": {"text": txt.strip(), "url": url.strip()}}}, upsert=True)
    await message.reply_text("✅ Button Set!")

@Client.on_message(filters.command("setstartvideo") & ~BANNED_USERS)
async def set_start_video_cmd(client, message):
    bot_id = (await client.get_me()).id
    if message.reply_to_message and message.reply_to_message.video:
        file_id = message.reply_to_message.video.file_id
    elif len(message.command) > 1: file_id = message.command[1]
    else: return await message.reply_text("Reply to video.")
    clonebotdb.update_one({"bot_id": bot_id}, {"$set": {"start_video": file_id}}, upsert=True)
    await message.reply_text("✅ Video Set!")

@Client.on_message(filters.command(["delstartimg", "delstartvideo", "delstartcaption", "delstartbutton"]) & ~BANNED_USERS)
async def delete_settings(client, message):
    bot_id = (await client.get_me()).id
    field = "start_" + message.command[0].replace("delstart", "")
    clonebotdb.update_one({"bot_id": bot_id}, {"$unset": {field: ""}})
    await message.reply_text(f"🗑 {field} Removed!")
