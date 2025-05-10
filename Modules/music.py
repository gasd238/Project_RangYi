from io import StringIO
import asyncio
import yt_dlp as youtube_dl
import discord
import pymongo, certifi
from Modules.setting import *  # Import Settings

client = pymongo.MongoClient(database, tlsCAFile=certifi.where())

contents = open('./Modules/cookies.txt').read()

cookies = StringIO(contents)

youtube_dl.utils.bug_reports_message = lambda: ''
 
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',  # bind to ipv4 since ipv6 addresses cause issues sometimes
    'cache-dir' : './',
    'cookiefile' : cookies,
    "extractor_args": {"youtube": {"player_clinet": "ios"}},
}

ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
 
 
# youtube 음악과 로컬 음악의 재생을 구별하기 위한 클래스 작성.
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
 
        self.data = data
 
        self.title = data.get('title')
        self.url = data.get('url')
 
    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
 
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
 
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data), data
    
class MusicChanDB:
    def __init__(self):
        self.db = client.rangyibot
        self.collection = self.db.Music

    def IsAlreadyHasMusicChan(self, channel):
        result = self.collection.find_one({"guildId": channel.guild.id})
        print(result)
        if result:
            return True
        return False
    
    def isFromMusicChan(self, channel):
        result = self.collection.find_one({"guildId": channel.guild.id, "channelId":channel.id})
        if result:
            return True
        return False
    
    def addMusicChan(self, channel, msg):
        musicchann = {
            "name" : channel.name,
            "channelId" : channel.id,
            "guildId" : channel.guild.id,
            "msgId" : msg.id
        }
        self.collection.insert_one(musicchann)

    def getMusicChan(self, guild):
        result = self.collection.find_one({"guildId": guild.id})
        if result:
            return result["msgId"]
        return False
