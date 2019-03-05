# -*- coding: utf-8 -*-
import globals, pymongo, requests, time
from db import *
from fake_useragent import UserAgent
from colorama import init, Fore, Back, Style
init()


def banner():
	print(Fore.MAGENTA + '''
 _       _____    __    __         ______
| |     / /   |  / /   / /        / ____/
| | /| / / /| | / /   / /  ______/ __/   
| |/ |/ / ___ |/ /___/ /__/_____/ /___   
|__/|__/_/  |_/_____/_____/    /_____/   
	
Modulo de búsqueda de contenido
		''')


def run():
	banner()
	mining()

def mining():
	ua = UserAgent()
	headers = {'User-Agent': ua.random}
	try:
		for t in globals.QUERY_MINING:
			for p in range(1,globals.PAGES_MINING+1):
				news = 0
				exist = 0
				print(Fore.YELLOW + logwrite("MINANDO QUERY %s pagina %d..."%(t,p)))
				query = requests.get("https://coub.com/api/v2%s?order_by=newest_popular&per_page=25&page=%d"%(t,p), headers=headers)
				json_data = query.json()
				for coub in json_data['coubs']:
					try:
						col_coubs.insert([{"permalink":coub['permalink'],"use": "", "likes":coub["likes_count"], "views":coub["views_count"],"categories":coub["categories"],"channelid":coub["channel_id"],"tags":coub["tags"],"nsfw":coub["not_safe_for_work"],"query":t}])
						news += 1
					except pymongo.errors.DuplicateKeyError:
						col_coubs.update_one({'permalink':coub['permalink']}, {"$set": {"likes": coub["likes_count"],"views":coub["views_count"],"categories":coub["categories"],"channelid":coub["channel_id"],"tags":coub["tags"],"nsfw":coub["not_safe_for_work"],"query":t}}, upsert=False)
						exist += 1
						continue
				print(Fore.YELLOW + logwrite("%d REGISTROS INGRESADOS, %d REGISTROS DUPLICADOS"%(news,exist)))
				time.sleep(globals.TIME_SLEEP)
	except Exception as e:
		print(Fore.RED + logwrite("ERROR: %s"%e))
		raise

	