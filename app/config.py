# Zironlink -- public redacted build. Full source in the private repo.

import os
from dotenv import load_dotenv
load_dotenv()

class Settings:
    HOST = os.getenv('LAVALINK_HOST', '0.0.0.0')
    PORT = int(os.getenv('LAVALINK_PORT', '2333'))
    PASSWORD = os.getenv('LAVALINK_PASSWORD', 'youshallnotpass')
    LAVALINK_API_VERSION = 4
    LAVALINK_SEMVER = '4.0.8'
    LAVALINK_BUILD = 'zironlink-1.0.0'
    JVM = 'n/a (python)'
    SOURCE_MANAGERS = ['youtube', 'soundcloud', 'http']
    FILTERS = ['volume', 'bassboost', 'lofi', 'slowmo']
    PLUGINS = []
    STATS_INTERVAL_SECONDS = 60
    PLAYER_UPDATE_INTERVAL_SECONDS = 5
    FFMPEG_PATH = os.getenv('FFMPEG_PATH', 'ffmpeg')
    DEBUG = os.getenv('ZIRONLINK_DEBUG', 'false').lower() in ('1', 'true', 'yes')
    QUEUE_LIMIT_PER_GUILD = int(os.getenv('LAVALINK_QUEUE_LIMIT', '100'))
    DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN', '')
settings = Settings()
