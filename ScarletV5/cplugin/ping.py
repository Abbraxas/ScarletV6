import time
from datetime import datetime
import psutil
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

# Ensure these imports are correct based on your folder structure
from config import SUPPORT_CHAT, PING_IMG_URL, OWNER_ID, BANNED_USERS
from ScarletV5 import app
from ScarletV5.misc import _boot_
from ScarletV5.utils import get_readable_time
from ScarletV5.utils.database.clonedb import (
    get_owner_id_from_db,
    get_cloned_support_chat,
    get_cloned_support_channel,
)
from ScarletV5.utils.database import clonebotdb

# =====================================================================
# DB HELPERS
# =====================================================================

def get_ping_image(bot_id: int):
    d = clonebotdb.find_one({"bot_id": bot_id}) or {}
    return d.get("ping_image")

def get_ping_video(bot_id: int):
    d = clonebotdb.find_one({"bot_id": bot_id}) or {}
    return d.get("ping_video")

# =====================================================================
# /ping COMMAND (Fixed Formatting)
# =====================================================================

@Client.on_message(filters.command("ping") & ~BANNED_USERS)
async def ping_clone(client: Client, message: Message):
    bot = await client.get_me()
    bot_id = bot.id

    # Support links fetch
    C_BOT_SUPPORT_CHAT = await get_cloned_support_chat(bot_id)
    C_SUPPORT_CHAT = f"https://t.me/{C_BOT_SUPPORT_CHAT}"

    # Fetch Media from DB
    ping_video = get_ping_video(bot_id)
    ping_img = get_ping_image(bot_id)
    
    start = datetime.now()
    caption_text = f"{bot.mention} is pinging..."

    # -----------------------------------------------------------
    # MEDIA PRIORITY: VIDEO > IMAGE > DEFAULT
    # -----------------------------------------------------------
    
    hmm = None
    
    # 1. Try sending Video
    if ping_video:
        try:
            hmm = await message.reply_video(video=ping_video, caption=caption_text)
        except Exception:
            pass # Fallback if video fails

    # 2. Try sending Custom Image
    if not hmm and ping_img:
        try:
            hmm = await message.reply_photo(photo=ping_img, caption=caption_text)
        except Exception:
            pass

    # 3. Default Config Image
    if not hmm:
        try:
            hmm = await message.reply_photo(photo=PING_IMG_URL, caption=caption_text)
        except Exception:
            # Last resort: Simple Text
            hmm = await message.reply_text(caption_text)

    # Stats Calculation
    upt = int(time.time() - _boot_)
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    resp = (datetime.now() - start).microseconds / 1000
    uptime = get_readable_time(upt)

    # FIXED: Clean formatting to avoid EntityBoundsInvalid
    stats_text = (
        f"➻ Pong: {resp}ms\n\n"
        f"{bot.mention} System Stats:\n\n"
        f"๏ Uptime: {uptime}\n"
        f"๏ Ram: {mem}%\n"
        f"๏ Cpu: {cpu}%\n"
        f"๏ Disk: {disk}%"
    )

    try:
        await hmm.edit_caption(
            stats_text,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Support", url=C_SUPPORT_CHAT)],
                ]
            ),
        )
    except Exception:
        # Fallback if caption edit fails (e.g., if hmm is a text message)
        await hmm.edit_text(
            stats_text,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Support", url=C_SUPPORT_CHAT)],
                ]
            ),
        )


# =====================================================================
# /setpingimg COMMAND (Fixed Error Messages)
# =====================================================================

@Client.on_message(filters.command("setpingimg") & ~BANNED_USERS)
async def set_ping_image(client: Client, message: Message):
    bot = await client.get_me()
    bot_id = bot.id
    
    owner_id = get_owner_id_from_db(bot_id)
    if message.from_user.id not in [OWNER_ID, owner_id]:
        return await message.reply_text("🚫 Only the Bot Owner can use this command.")

    if message.reply_to_message and message.reply_to_message.photo:
        file_id = message.reply_to_message.photo.file_id
        clonebotdb.update_one({"bot_id": bot_id}, {"$set": {"ping_image": file_id}}, upsert=True)
        return await message.reply_text("✅ Ping image saved!")

    if len(message.command) == 2:
        url = message.command[1].strip()
        clonebotdb.update_one({"bot_id": bot_id}, {"$set": {"ping_image": url}}, upsert=True)
        return await message.reply_text("✅ Ping image saved from URL!")

    # FIXED: Simplified message to avoid ENTITY_BOUNDS_INVALID
    return await message.reply_text("❗ Reply to a photo or use /setpingimg [URL]")


@Client.on_message(filters.command("delpingimg") & ~BANNED_USERS)
async def del_ping_image(client: Client, message: Message):
    bot = await client.get_me()
    bot_id = bot.id

    owner_id = get_owner_id_from_db(bot_id)
    if message.from_user.id not in [OWNER_ID, owner_id]:
        return await message.reply_text("🚫 Only the Bot Owner can use this command.")

    clonebotdb.update_one({"bot_id": bot_id}, {"$unset": {"ping_image": ""}})
    return await message.reply_text("🗑 Ping image removed!")


# =====================================================================
# /setpingvideo COMMAND (Fixed Error Messages)
# =====================================================================

@Client.on_message(filters.command("setpingvideo") & ~BANNED_USERS)
async def set_ping_video(client: Client, message: Message):
    bot = await client.get_me()
    bot_id = bot.id
    
    owner_id = get_owner_id_from_db(bot_id)
    if message.from_user.id not in [OWNER_ID, owner_id]:
        return await message.reply_text("🚫 Only the Bot Owner can use this command.")

    if message.reply_to_message and message.reply_to_message.video:
        file_id = message.reply_to_message.video.file_id
        clonebotdb.update_one({"bot_id": bot_id}, {"$set": {"ping_video": file_id}}, upsert=True)
        return await message.reply_text("✅ Ping video saved!")

    if message.reply_to_message and message.reply_to_message.animation:
        file_id = message.reply_to_message.animation.file_id
        clonebotdb.update_one({"bot_id": bot_id}, {"$set": {"ping_video": file_id}}, upsert=True)
        return await message.reply_text("✅ Ping GIF saved!")

    if len(message.command) == 2:
        url = message.command[1].strip()
        clonebotdb.update_one({"bot_id": bot_id}, {"$set": {"ping_video": url}}, upsert=True)
        return await message.reply_text("✅ Ping video saved from URL!")

    # FIXED: Simplified message to avoid ENTITY_BOUNDS_INVALID
    return await message.reply_text("❗ Reply to a video/GIF or use /setpingvideo [URL]")


@Client.on_message(filters.command("delpingvideo") & ~BANNED_USERS)
async def del_ping_video(client: Client, message: Message):
    bot = await client.get_me()
    bot_id = bot.id

    owner_id = get_owner_id_from_db(bot_id)
    if message.from_user.id not in [OWNER_ID, owner_id]:
        return await message.reply_text("🚫 Only the Bot Owner can use this command.")

    clonebotdb.update_one({"bot_id": bot_id}, {"$unset": {"ping_video": ""}})
    return await message.reply_text("🗑 Ping video removed!")