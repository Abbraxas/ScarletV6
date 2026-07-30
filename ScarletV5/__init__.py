from ScarletV5.core.bot import Axiom
from ScarletV5.core.dir import dirr
from ScarletV5.core.git import git
from ScarletV5.core.userbot import Userbot
from ScarletV5.misc import dbb, heroku
from pyrogram import Client
from SafoneAPI import SafoneAPI
from .logging import LOGGER

dirr()
# git()
dbb()
heroku()

app = Axiom()
api = SafoneAPI()
userbot = Userbot()

from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()
