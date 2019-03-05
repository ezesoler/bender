# -*- coding: utf-8 -*-
import globals, pymongo, requests, time
from db import *
from fake_useragent import UserAgent
from helpers import *
from colorama import init, Fore, Back, Style
init()


def banner():
	print(Fore.MAGENTA + '''

  _____  ___  _____ ___  
 |  __ \|__ \|  __ \__ \ 
 | |__) |  ) | |  | | ) |
 |  _  /  / /| |  | |/ / 
 | | \ \ / /_| |__| / /_ 
 |_|  \_\____|_____/____|

Modulo de estadistícas
		''')

def run():
    banner()
    get_data_channel()
    get_data_videos()

def get_data_channel():
    print(Fore.YELLOW + logwrite("OBTENIENDO ESTADÍSTICAS DEL CANAL"))
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    try:
        data_chanel = requests.get("https://www.googleapis.com/youtube/v3/channels?part=id,statistics,snippet&id=%s&key=%s"%(globals.YOUTUBE_CHANNEL_ID,globals.YOUTUBE_API_KEY), headers=headers)
        json_data = data_chanel.json()
        col_stats.insert([{"subscibers":json_data["items"][0]["statistics"]["subscriberCount"],"views": json_data["items"][0]["statistics"]["viewCount"],"videos":json_data["items"][0]["statistics"]["videoCount"]}])
        #sendMessage("%%F0%%9F%%93%%8A *ESTADISTICAS CANAL*%%0A%%0A%%E2%%9C%%94%%EF%%B8%%8FSubscriptores: *%s*%%0A%%E2%%9C%%94%%EF%%B8%%8FVistas: *%s*%%0A%%E2%%9C%%94%%EF%%B8%%8FVideos: *%s*"%(json_data["items"][0]["statistics"]["subscriberCount"],json_data["items"][0]["statistics"]["viewCount"],json_data["items"][0]["statistics"]["videoCount"]))
    except Exception as e:
        print(Fore.RED + logwrite("ERROR: %s"%e))
        raise

def get_data_videos():
    videos = col_videos.find()
    for video in videos:
        print(Fore.YELLOW + logwrite("OBTENIENDO ESTADISTICAS DEL VIDEO %s"%video["yt"]))
        ua = UserAgent()
        headers = {'User-Agent': ua.random}
        try:
            data_chanel = requests.get("https://www.googleapis.com/youtube/v3/videos?part=id,statistics&id=%s&key=%s"%(video["yt"],globals.YOUTUBE_API_KEY), headers=headers)
            json_data = data_chanel.json()
            if json_data["pageInfo"]["totalResults"] > 0:
                col_videos.update_one({'_id':video['_id']}, {"$set": {"views": json_data["items"][0]["statistics"]["viewCount"], "likes": json_data["items"][0]["statistics"]["likeCount"], "dislike": json_data["items"][0]["statistics"]["dislikeCount"], "comments": json_data["items"][0]["statistics"]["commentCount"] }}, upsert=True)
        except Exception as e:
            print(Fore.RED + logwrite("ERROR: %s"%e))