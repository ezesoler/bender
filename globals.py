VERSION = {
	'num':"1.0"
}

DATABASE_CONFIG = {
    'host': 'localhost',
    'auth': 'admin',
    'user': 'admin',
    'password': '<db_password>',
    'port': 27017
}

TIME_SLEEP = 10

TIME_SLEEP_RENDER = 60 * 2

TIME_SLEEP_PRODUCE = 60 * 5


PAGES_MINING = 5
QUERY_MINING = ["/timeline/tag/funny","/timeline/tag/meme","/timeline/tag/memes","/timeline/tag/mashup","/timeline/tag/comedy","/timeline/explore/mashup","/timeline/hot"]

COUBS_PER_VIDEO_MIN = 20
COUBS_PER_VIDEO_MAX = 35

VIDEO_LENGHT_ID = 10

COUB_PREFIX_URL = "http://coub.com/api/v2/coubs/"

COUBS_TMP_DIR = "tmp"

COUNS_SOURCES_DIR = "src"

VIDEO_OUT_DIR = "videos"

ASSETS_DIR = "assets"

CLIENT_SECRETS_FILE = "client_secrets.json"

YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

YOUTUBE_CHANNEL_ID = "<channel_id>"
YOUTUBE_API_KEY = "<google_api_key>"

YOUTUBE_CHANNELS_TARGET = [
	"UCqoOcEKFZnV1zQ4khXzG6kg",
	"UCM6yPd-dzKvHhGptvrAmT5w",
	"UCt7E8Qpue2TU9Yh47vkEbsQ",
    "UCd07rKJ7Q0pg5ths7Pz8k8Q"
]

BASE_TITLE_VIDEOS = "RANDOM VIDEOS COMPILATION #%d"

TAG_LIMIT = 30

DESCRIPTION_BASE = "SUBSCRIBE FOR MORE DAILY VIDEOS\nAll Copyrights belongs to their rightful owners.\n\n#randomvideos #memes #compilation #funny\n\nClips from:\n"

BOT_TELEGRAM_TOKEN = "<bot_telegram_token>"
BOT_TELEGRAM_CHAT_ID = "<id_chat_bot>"
