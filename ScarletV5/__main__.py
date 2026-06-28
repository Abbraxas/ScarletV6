
import asyncio
import importlib

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from ScarletV5 import LOGGER, app, userbot
from ScarletV5.core.call import Axiom
from ScarletV5.misc import sudo
from ScarletV5.plugins import ALL_MODULES
from ScarletV5.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS
from ScarletV5.plugins.tools.clone import restart_bots


async def init():
    if not config.STRING1:
        LOGGER(__name__).error("String Session not filled, please Provide a valid session.")
        exit()
    await sudo()
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass
    await app.start()
    for all_module in ALL_MODULES:
        importlib.import_module("ScarletV5.plugins" + all_module)
    LOGGER("ScarletV5.plugins").info("Successfully imported every features...")
    await userbot.start()
    await Axiom.start()
    try:
        await Axiom.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("ScarletV5").error(
            "Please check the vc of logger gc is started or not?"
        )
        exit()
    except:
        pass
    await Axiom.decorators()
    await restart_bots()
    LOGGER("ScarletV5").info(
        "Axiom Clone Music Bot Successfully started......"
    )
    await idle()
    await app.stop()
    await userbot.stop()
    LOGGER("ScarletV5").info("Stopping Axiom Clone Music Bot.....")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
