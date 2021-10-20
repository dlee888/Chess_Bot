import os

DATA_DIR = 'data'
LOGS_DIR = 'logs'

ASSETS_DIR = os.path.join(DATA_DIR, 'assets')
TEMP_DIR = os.path.join(DATA_DIR, 'temp')

LOG_FILE_PATH = os.path.join(LOGS_DIR, 'debug.log')
DB_DIR =  os.path.join(DATA_DIR, 'db')

THEMES_DIR = os.path.join(ASSETS_DIR, 'themes')

ERROR_CHANNEL_ID = 799761964401819679
LOG_CHANNEL_ID = 798277701210341459
SUPPORT_SERVER_ID = 733762995372425337
STATUS_CHANNEL_ID = 823579566756986930
STATS_CHANNEL_ID = 855151698035998761
AVATAR_URL = 'https://i.imgur.com/n1jak68.png'
THONK_EMOJI_ID = 814285875265536001

BETA_CHANNELS = [813838854581780492, 874406756577599528]
DEVELOPERS = [716070916550819860, 721043620060201051]

DEFAULT_RATING = 1200
LEADERBOARD_IGNORE = []
MAX_LEADERBOARD_SIZE = 40
DEFAULT_LEADERBOARD_SIZE = 10

CACHE_REFRESH_TIME = 3600

MAX_TIME_PER_MOVE = 3 * 24 * 60 * 60
LOW_TIME_WARN = 24 * 60 * 60

INVITE_LINK = r'https://discord.com/api/oauth2/authorize?client_id=801501916810838066&permissions=2147795008&scope=bot%20applications.commands'
GITHUB_LINK = 'https://github.com/jeffarjeffar/Chess_Bot'
SUPPORT_SERVER_INVITE = 'https://discord.gg/Bm4zjtNTD2'
TOPGG_LINK = 'https://top.gg/bot/801501916810838066/vote'

ALL_DIRS = (attrib_value for attrib_name, attrib_value in list(globals().items())
            if attrib_name.endswith('DIR'))
