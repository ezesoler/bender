# -*- coding: utf-8 -*-
import globals, pymongo, requests, time
from db import *
from fake_useragent import UserAgent
from colorama import init, Fore, Back, Style
init()

def banner():
	print(Fore.MAGENTA + '''                      
 _____     ___ ___ ___ 
|_   _|___| . |   |   |
  | | |___| . | | | | |
  |_|     |___|___|___|
                                                       	
Modulo de recolección de datos
		''')


def run():
	banner()
	gathering_tags()

def gathering_tags():
	ua = UserAgent()
	headers = {'User-Agent': ua.random}
	for c in globals.YOUTUBE_CHANNELS_TARGET:
		print(Fore.YELLOW + logwrite("OBTENIENDO TAGS DEL CANAL %s"%c))
		videos_chanel = requests.get("https://www.googleapis.com/youtube/v3/search?part=snippet,id&order=viewcount&maxResults=10&channelId=%s&key=%s"%(c,globals.YOUTUBE_API_KEY), headers=headers)
		json_data = videos_chanel.json()
		for v in json_data["items"]:
			try:
				video_data = requests.get("https://www.googleapis.com/youtube/v3/videos?part=id,snippet&id=%s&key=%s"%(v["id"]["videoId"],globals.YOUTUBE_API_KEY), headers=headers)
				json_data_video = video_data.json()
				for t in json_data_video["items"][0]["snippet"]["tags"]:
					col_tags.update_one({'text':t}, {"$set": {"text": t, "active":"0"}}, upsert=True)
			except:
				continue