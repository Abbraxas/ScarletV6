import re
import logging
import asyncio
import importlib
from sys import argv
from pyrogram import idle
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors.exceptions.bad_request_400 import (
    AccessTokenExpired,
    AccessTokenInvalid,
)
from ScarletV5.utils.database import get_assistant
from config import API_ID, API_HASH
from ScarletV5 import app
from config import OWNER_ID
from ScarletV5.misc import SUDOERS
from ScarletV5.utils.database import get_assistant, clonebotdb
from ScarletV5.utils.database.clonedb import has_user_cloned_any_bot
from config import LOGGER_ID, CLONE_LOGGER
import requests
from ScarletV5.utils.decorators.language import language
import pyrogram.errors

from ScarletV5.utils.database.clonedb import get_owner_id_from_db
from config import SUPPORT_CHAT, OWNER_ID

from datetime import datetime
CLONES = set()

C_BOT_DESC = "𝐖‌єʟᴄσϻє ᴛσ ʏσυꝛ ᴘєꝛsσηᴧʟɪᴢєᴅ ϻυsɪᴄ 𝚺ᴄσsʏsᴛєϻ. \n\n𝐅‌ꝛσϻ sᴛꝛєᴧϻɪηɢ ᴧηᴅ ʙꝛσᴧᴅᴄᴧsᴛɪηɢ ᴛσ ᴘєꝛsσηᴧʟɪᴢєᴅ ϻєᴅɪᴧ, єᴠєꝛʏ ғєᴧᴛυꝛє ɪs ʙυɪʟᴛ ᴛσ ʙє ʏσυꝛs.\n\n𝐍‌єєᴅ ʏσυꝛ σᴡη? 𝐂‌ʟσηє ɪᴛ ɪη ᴧ ғєᴡ sєᴄσηᴅs ➜ @ScarletCloneBot\n\n• 𝐔‌ᴘᴅᴧᴛєs ➜ @AxiomBots\n• 𝐂‌ꝛєᴧᴛσꝛ ➜ @CreativeAxiom"

C_BOT_COMMANDS = [
                {"command": "/start", "description": "| 𝐈‌ηɪᴛɪᴧᴛєs 𝐓‌ʜє 𝐌‌υsɪᴄ 𝐁‌σᴛ."},
                {"command": "/help", "description": "| 𝐀‌ᴄᴄєss 𝐓‌ʜє 𝐇‌єʟᴘ 𝐇‌υʙ 𝐖‌ɪᴛʜ 𝐂‌σϻᴘʟєᴛє 𝐂‌σϻϻᴧηᴅ 𝐄‌xᴘʟᴧηᴧᴛɪσηs."},
                {"command": "/clone", "description": "| 𝐅‌σꝛɢєs 𝐀‌ 𝐏‌єꝛsσηᴧʟɪᴢєᴅ 𝐂‌ʟσηє 𝐎‌ғ 𝐓‌ʜє 𝐌‌υsɪᴄ 𝐁‌σᴛ."},
                {"command": "/play", "description": "| 𝐋‌ᴧυηᴄʜєs 𝐓‌ʜє 𝐑‌єǫυєsᴛєᴅ 𝐓‌ꝛᴧᴄᴋ 𝐈‌η 𝐕‌σɪᴄє 𝐂‌ʜᴧᴛ."},
                {"command": "/vplay", "description": "| 𝐋‌ᴧυηᴄʜєs 𝐓‌ʜє 𝐑‌єǫυєsᴛєᴅ 𝐕‌ɪᴅєσ 𝐈‌η 𝐕‌σɪᴄє 𝐂‌ʜᴧᴛ."},
                {"command": "/cplay", "description": "| 𝐈‌ηɪᴛɪᴧᴛєs 𝐀‌υᴅɪσ 𝐏‌ʟᴧʏʙᴧᴄᴋ 𝐎‌η 𝐘‌συꝛ 𝐂‌ʟσηє 𝐁‌σᴛ."},
                {"command": "/cvplay", "description": "| 𝐈‌ηɪᴛɪᴧᴛєs 𝐕‌ɪᴅєσ 𝐏‌ʟᴧʏʙᴧᴄᴋ 𝐎‌η 𝐘‌συꝛ 𝐂‌ʟσηє 𝐁‌σᴛ."},
                {"command": "/cplayforce", "description": "| 𝐅‌σꝛᴄєs 𝐀‌υᴅɪσ 𝐏‌ʟᴧʏʙᴧᴄᴋ 𝐁‌ʏ 𝐁‌ʏᴘᴧssɪηɢ 𝐓‌ʜє 𝐐‌υєυє."},
                {"command": "/cvplayforce", "description": "| 𝐅‌σꝛᴄєs 𝐕‌ɪᴅєσ 𝐏‌ʟᴧʏʙᴧᴄᴋ 𝐁‌ʏ 𝐁‌ʏᴘᴧssɪηɢ 𝐓‌ʜє 𝐐‌υєυє."},
                {"command": "/pause", "description": "| 𝐇‌ᴧʟᴛs 𝐓‌ʜє 𝐂‌υꝛꝛєηᴛʟʏ 𝐒‌ᴛꝛєᴧϻɪηɢ 𝐓‌ꝛᴧᴄᴋ."},
                {"command": "/resume", "description": "| 𝐑‌єᴧᴄᴛɪᴠᴧᴛєs 𝐓‌ʜє 𝐏‌ᴧυsєᴅ 𝐒‌ᴛꝛєᴧϻ."},
                {"command": "/skip", "description": "| 𝐎‌ϻɪᴛs 𝐓‌ʜє 𝐂‌υꝛꝛєηᴛ 𝐓‌ꝛᴧᴄᴋ 𝐀‌ηᴅ 𝐀‌ᴅᴠᴧηᴄєs 𝐓‌σ 𝐓‌ʜє 𝐍‌єxᴛ 𝐎‌ηє."},
                {"command": "/end", "description": "| 𝐓‌єꝛϻɪηᴧᴛєs 𝐓‌ʜє 𝐒‌ᴛꝛєᴧϻ 𝐀‌ηᴅ 𝐏‌υꝛɢєs 𝐓‌ʜє 𝐐‌υєυє."},
                {"command": "/ping", "description": "| 𝐃‌ɪsᴘʟᴧʏs 𝐁‌σᴛ 𝐋‌ᴧᴛєηᴄʏ 𝐀‌ηᴅ 𝐒‌ʏsᴛєϻ 𝐌‌єᴛꝛɪᴄs."},
                {"command": "/id", "description": "| 𝐑‌єᴠєᴧʟs 𝐓‌ʜє 𝐂‌υꝛꝛєηᴛ 𝐂‌ʜᴧᴛ 𝐎‌ꝛ 𝐔‌sєꝛ 𝐈‌ᴅєηᴛɪғɪєꝛ."},
            ]


@app.on_message(filters.command("clone"))
@language
async def clone_txt(client, message, _):
    userbot = await get_assistant(message.chat.id)

    userid = message.from_user.id
    has_already_cbot = await has_user_cloned_any_bot(userid)

    if has_already_cbot:
        if message.from_user.id != OWNER_ID:
            return await message.reply_text(_["C_B_H_0"])
    else:
        pass
    

    if len(message.command) > 1:
        bot_token = message.text.split("/clone", 1)[1].strip()
        mi = await message.reply_text(_["C_B_H_2"])
        try:
            ai = Client(
                bot_token,
                API_ID,
                API_HASH,
                bot_token=bot_token,
                plugins=dict(root="ScarletV5.cplugin"), 
            )
            await ai.start()
            bot = await ai.get_me()
            bot_users = await ai.get_users(bot.username)
            bot_id = bot_users.id
            c_b_owner_fname = message.from_user.first_name
            c_bot_owner = message.from_user.id

        except (AccessTokenExpired, AccessTokenInvalid):
            await mi.edit_text(_["C_B_H_3"])
            return
        except Exception as e:
            if "database is locked" in str(e).lower():
                await message.reply_text(_["C_B_H_4"])
            else:
                await mi.edit_text(f"An error occurred: {str(e)}")
            return

        await mi.edit_text(_["C_B_H_5"])
        try:

            await app.send_message(
                CLONE_LOGGER, f"**#New_Cloned_Bot**\n\n**ʙᴏᴛ:- {bot.mention}**\n**ᴜsᴇʀɴᴀᴍᴇ:** @{bot.username}\n**ʙᴏᴛ ɪᴅ :** `{bot_id}`\n\n**ᴏᴡɴᴇʀ : ** [{c_b_owner_fname}](tg://user?id={c_bot_owner})"
            )
            await userbot.send_message(bot.username, "/start")

            details = {
                "bot_id": bot.id,
                "is_bot": True,
                "user_id": message.from_user.id,
                "name": bot.first_name,
                "token": bot_token,
                "username": bot.username,
                "channel": "AxiomBots",
                "support": "Axlomm",
                "premium" : False,
                "Date" : False,
            }
            clonebotdb.insert_one(details)
            CLONES.add(bot.id)

            def set_bot_commands():
                url = f"https://api.telegram.org/bot{bot_token}/setMyCommands"
                
                params = {"commands": C_BOT_COMMANDS}
                response = requests.post(url, json=params)
                print(response.json())

            set_bot_commands()

            def set_bot_desc():
                url = f"https://api.telegram.org/bot{bot_token}/setMyDescription"
                params = {"description": C_BOT_DESC}
                response = requests.post(url, data=params)
                if response.status_code == 200:
                    logging.info(f"Successfully updated Description for bot: {bot_token}")
                else:
                    logging.error(f"Failed to update Description: {response.text}")

            set_bot_desc()

            await mi.edit_text(_["C_B_H_6"].format(bot.username))
        except BaseException as e:
            logging.exception("Error while cloning bot.")
            await mi.edit_text(
                f"⚠️ <b>ᴇʀʀᴏʀ:</b>\n\n<code>{e}</code>\n\n**ᴋɪɴᴅʟʏ ғᴏᴡᴀʀᴅ ᴛʜɪs ᴍᴇssᴀɢᴇ ᴛᴏ @CreativeAxiom ᴛᴏ ɢᴇᴛ ᴀssɪsᴛᴀɴᴄᴇ**"
            )
    else:
        await message.reply_text(_["C_B_H_1"])


@app.on_message(
    filters.command(
        [
            "delbot",
            "rmbot",
            "delcloned",
            "delclone",
            "deleteclone",
            "removeclone",
            "cancelclone",
        ]
    )
)
@language
async def delete_cloned_bot(client, message, _):
    try:
        if len(message.command) < 2:
            await message.reply_text(_["C_B_H_8"])
            return

        query_value = " ".join(message.command[1:])
        if query_value.startswith("@"):
            query_value = query_value[1:]
        await message.reply_text(_["C_B_H_9"])

        cloned_bot = clonebotdb.find_one({"$or": [{"token": query_value}, {"username": query_value}]})
        
        if cloned_bot:

            bot_info = f"**ʙᴏᴛ ɪᴅ**: `{cloned_bot['bot_id']}`\n" \
           f"**ʙᴏᴛ ɴᴀᴍᴇ**: {cloned_bot['name']}\n" \
           f"**ᴜsᴇʀɴᴀᴍᴇ**: @{cloned_bot['username']}\n" \
           f"**ᴛᴏᴋᴇɴ**: `{cloned_bot['token']}`\n" \
           f"**ᴏᴡɴᴇʀ**: `{cloned_bot['user_id']}`\n"

            C_OWNER = get_owner_id_from_db(cloned_bot['bot_id'])
            OWNERS = [OWNER_ID, C_OWNER]

            if message.from_user.id not in OWNERS:
                return await message.reply_text(_["NOT_C_OWNER"].format(SUPPORT_CHAT))

            clonebotdb.delete_one({"_id": cloned_bot["_id"]})
            CLONES.remove(cloned_bot["bot_id"])

            await message.reply_text(_["C_B_H_10"])
            await app.send_message(
                CLONE_LOGGER, bot_info
            )
        else:
            await message.reply_text(_["C_B_H_11"])
    except Exception as e:
        await message.reply_text(_["C_B_H_12"])
        await app.send_message(
                CLONE_LOGGER, bot_info
            )
        logging.exception(e)


async def restart_bots():
    global CLONES
    try:
        logging.info("Restarting all cloned bots........")
        bots = list(clonebotdb.find())
        botNumber = 1
        for bot in bots:
            bot_token = bot["token"]

            url = f"https://api.telegram.org/bot{bot_token}/getMe"
            response = requests.get(url)
            if response.status_code != 200:
                logging.error(f"Invalid or expired token for bot: {bot_token}")
                clonebotdb.delete_one({"token": bot_token})
                continue

            ai = Client(
                f"{bot_token}",
                API_ID,
                API_HASH,
                bot_token=bot_token,
                plugins=dict(root="ScarletV5.cplugin"),
             )
             try:
                 await ai.start()
             except Exception as e:
                 if "database is locked" in str(e).lower():
                     logging.warning(f"Database locked for bot {bot_token}. Skipping it.")
                 else:
                     logging.error(f"Error starting bot {bot_token}: {e}")
                 continue
             
             print(botNumber)
             botNumber += 1

            bot = await ai.get_me()
            if bot.id not in CLONES:
                try:
                    CLONES.add(bot.id)
                except Exception:
                    pass

            await asyncio.sleep(5)

        await app.send_message(
                CLONE_LOGGER,
"""
<b><blockquote><u>❖ ᴄʟσηєᴅ ʙσᴛ ʀєsᴛᴧʀᴛ ᴄσϻᴘʟєᴛєᴅ</u></blockquote></b>
<blockquote><b>✦ <u>sᴛᴧᴛυs</u> : ᴧᴄᴛɪᴠє ʙσᴛs sᴛᴧʀᴛєᴅ</b>
<b>✦ <u>ғʟσσᴅᴡᴧɪᴛ</u> : ᴘєηᴅɪηɢ ʙσᴛs ᴡɪʟʟ ᴧυᴛσ-sᴛᴧʀᴛ</b>
<b>✦ <u>ϻσᴅє</u> : ʙᴧᴄᴋɢʀσυηᴅ ʀєᴄσᴠєʀʏ єηᴧʙʟєᴅ</b></blockquote>
<b><blockquote><u>❖ ᴧʟʟ ᴄʟσηєs ᴘʀσᴄєssєᴅ sυᴄᴄєssғυʟʟʏ.</u></blockquote></b>
"""
            )
    except Exception as e:
        logging.exception("Error while restarting bots.")

# Zeo
@app.on_message(filters.command("delallclone") & filters.user(OWNER_ID))
@language
async def delete_all_cloned_bots(client, message, _):
    try:
        await message.reply_text(_["C_B_H_14"])

        clonebotdb.delete_many({})

        CLONES.clear()

        await message.reply_text(_["C_B_H_15"])
    except Exception as e:
        await message.reply_text("An error occurred while deleting all cloned bots.")
        logging.exception(e)


@app.on_message(filters.command(["mybot", "mybots"], prefixes=["/", "."]))
@language
async def my_cloned_bots(client, message, _):
    try:
        user_id = message.from_user.id
        cloned_bots = list(clonebotdb.find({"user_id": user_id}))
        
        if not cloned_bots:
            await message.reply_text(_["C_B_H_16"])
            return
        
        total_clones = len(cloned_bots)
        text = f"**ʏᴏᴜʀ ᴄʟᴏɴᴇᴅ ʙᴏᴛs : {total_clones}**\n\n"
        
        for bot in cloned_bots:
            text += f"**ʙᴏᴛ ɴᴀᴍᴇs:** {bot['name']}\n"
            text += f"**ʙᴏᴛ ᴜsᴇʀɴᴀᴍᴇ:** @{bot['username']}\n\n"
        
        await message.reply_text(text)
    except Exception as e:
        logging.exception(e)
        await message.reply_text("An error occurred while fetching your cloned bots.")



@app.on_message(filters.command("cloned") & SUDOERS)
@language
async def list_cloned_bots(client, message, _):
    try:
        cloned_bots = list(clonebotdb.find())
        if not cloned_bots:
            await message.reply_text(_["C_B_H_13"])
            return

        total_clones = len(cloned_bots)
        text = f"**ᴛᴏᴛᴀʟ ᴄʟᴏɴᴇᴅ ʙᴏᴛs: `{total_clones}`**\n\n"

        chunk_size = 10
        chunks = [cloned_bots[i:i + chunk_size] for i in range(0, len(cloned_bots), chunk_size)]

        for chunk in chunks:
            chunk_text = text
            for bot in chunk:
                try:
                    owner = await client.get_users(bot['user_id'])
                    owner_name = owner.first_name
                    owner_profile_link = f"tg://user?id={bot['user_id']}"
                except pyrogram.errors.PeerIdInvalid:
                    owner_name = "Unknown User"
                    owner_profile_link = "#"
                except Exception as e:
                    logging.error(f"Error fetching user {bot['user_id']}: {e}")
                    owner_name = "Unknown User"
                    owner_profile_link = "#"

                chunk_text += f"**ʙᴏᴛ ɪᴅ :** `{bot['bot_id']}`\n"
                chunk_text += f"**ʙᴏᴛ ɴᴀᴍᴇ :** {bot['name']}\n"
                chunk_text += f"**ʙᴏᴛ ᴜsᴇʀɴᴀᴍᴇ :** @{bot['username']}\n"
                chunk_text += f"**ᴏᴡɴᴇʀ :** [{owner_name}]({owner_profile_link})\n\n"

            await message.reply_text(chunk_text)

    except Exception as e:
        logging.exception(e)
        await message.reply_text("An error occurred while listing cloned bots.")



#total clone
@app.on_message(filters.command("totalbots") & SUDOERS)
@language
async def list_cloned_bots(client, message, _):
    try:
        cloned_bots = list(clonebotdb.find())
        if not cloned_bots:
            await message.reply_text("No bots have been cloned yet.")
            return

        total_clones = len(cloned_bots)
        text = f"**ᴛᴏᴛᴀʟ ᴄʟᴏɴᴇᴅ ʙᴏᴛs : `{total_clones}`**\n\n"         

        await message.reply_text(text)
    except Exception as e:
        logging.exception(e)
        await message.reply_text("An error occurred while listing cloned bots.")
