# -*- coding: utf-8 -*-
import globals, pymongo, time, datetime, random, string, requests, os, sys, glob, shutil, httplib, httplib2
from db import *
from apiclient.discovery import build
from apiclient.errors import HttpError
from apiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow
from fake_useragent import UserAgent
from helpers import *
from colorama import init, Fore, Back, Style
init()

httplib2.RETRIES = 1

MAX_RETRIES = 10

RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError, httplib.NotConnected,
  httplib.IncompleteRead, httplib.ImproperConnectionState,
  httplib.CannotSendRequest, httplib.CannotSendHeader,
  httplib.ResponseNotReady, httplib.BadStatusLine)

RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

videoid = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(globals.VIDEO_LENGHT_ID))

def banner():
    print(Fore.MAGENTA + '''

   ____  ____  ____________  _____  _______
  / __ \/ __ \/_  __/  _/  |/  / / / / ___/
 / / / / /_/ / / /  / // /|_/ / / / /\__ \ 
/ /_/ / ____/ / / _/ // /  / / /_/ /___/ / 
\____/_/     /_/ /___/_/  /_/\____//____/  

Modulo de descarga, producción y subida de videos
        ''')


def run():
    banner()
    check_dir()
    get_content()
    time.sleep(globals.TIME_SLEEP_PRODUCE)
    produce()
    upload()

def check_dir():
    if not os.path.exists(globals.COUBS_TMP_DIR):
        os.makedirs(globals.COUBS_TMP_DIR)
    else:
       files = glob.glob("./"+globals.COUBS_TMP_DIR+"/*")
       for f in files:
            os.remove(f)

    if not os.path.exists(globals.COUNS_SOURCES_DIR):
        os.makedirs(globals.COUNS_SOURCES_DIR)
    else:
       files = glob.glob("./"+globals.COUNS_SOURCES_DIR+"/*")
       for f in files:
            os.remove(f)

    if not os.path.exists(globals.VIDEO_OUT_DIR):
        os.makedirs(globals.VIDEO_OUT_DIR)
    else:
       files = glob.glob("./"+globals.VIDEO_OUT_DIR+"/*")
       for f in files:
            os.remove(f)

def get_content():
    num_coubs = random.randint(globals.COUBS_PER_VIDEO_MIN,globals.COUBS_PER_VIDEO_MAX)
    count = col_coubs.find({"use":"","nsfw":False,"categories.id":{"$nin":[36,24]}}).count()
    print(Fore.YELLOW + logwrite("NUMERO DE VIDEOS: %d"%num_coubs))
    #coubs = col_coubs.find({"use":""}).limit(num_coubs).skip(random.randrange(count-num_coubs))
    order = ["likes","views"]
    ro = order[random.randint(0,1)]
    print(Fore.YELLOW + logwrite("ORDENADOS POR: %s"%ro))
    coubs = col_coubs.find({"use":"","nsfw":False,"categories.id":{"$nin":[36,24]}}).limit(num_coubs).sort(ro,pymongo.DESCENDING)
    for coub in coubs:
        col_coubs.update_one({'_id':coub['_id']}, {"$set": {"use": videoid}}, upsert=False)
        try:
            print(Fore.YELLOW + logwrite("BAJANDO COUBS: %s"%coub['permalink']))
            download(coub['permalink'])
            logwrite("Temp: "+getTemp()+" C'")
            print(Fore.YELLOW + logwrite("COMPILANDO COUBS: %s"%coub['permalink']))
            compile(coub['permalink'])
            logwrite("Temp: "+getTemp()+" C'")
            col_coubs.update_one({'_id':coub['_id']}, {"$set": {"use": videoid}}, upsert=False)
        except:
            print(Fore.RED + logwrite("ERROR COUBS: %s"%coub['permalink']))
            continue
        time.sleep(globals.TIME_SLEEP_RENDER)
    print(videoid)

def download(coubid):
        ua = UserAgent()
        headers = {'User-Agent': ua.random}

        url = globals.COUB_PREFIX_URL+coubid

        page_str = requests.get(url, headers=headers)

        json_obj = page_str.json()

        video_url = None
        audio_url = None

        video_size = 0
        if 'high' in json_obj['file_versions']['html5']['video']:
            video_url = json_obj["file_versions"]["html5"]["video"]["high"]["url"]
            video_size = json_obj["file_versions"]["html5"]["video"]["high"]["size"]
        elif 'med' in json_obj['file_versions']['html5']['video']:
            video_url = json_obj["file_versions"]["html5"]["video"]["med"]["url"]
            video_size = json_obj["file_versions"]["html5"]["video"]["med"]["size"]

        if 'high' in json_obj['file_versions']['html5']['audio']:
            audio_url = json_obj["file_versions"]["html5"]["audio"]["high"]["url"]
        elif 'med' in json_obj['file_versions']['html5']['audio']:
            audio_url = json_obj["file_versions"]["html5"]["audio"]["med"]["url"]

        if not (video_url or audio_url):
            print(Fore.RED + "Error al validar la url: {}".format(url))
            return

        headers["Referer"] = url
        range_download_video(video_url, video_size, url, coubid, headers)

        audio_response = requests.get(audio_url, headers=headers, stream=True)
        audio_blob = audio_response.raw

        if audio_url:
            save_mp3_to(audio_blob, coubid)
        else:
            print(Fore.RED + logwrite("Error al bajar el archivo: {}".format(audio_url)))


def fix_first_byte_video(fragment):
    video_fragment = bytearray(fragment)
    video_fragment[0] = 0
    video_fragment[1] = 0
    return str(video_fragment)

def range_download_video(video_url, video_size, referer, name, headers):

    video_options = requests.options(video_url, headers=headers, stream=True)

    
    headers['Access-Control-Request-Headers'] = 'range'
    headers['Access-Control-Request-Method'] = 'GET'
    headers['Origin'] = 'https://coub.com'

    
    headers['Range'] = 'bytes=0-'
    video_response = requests.get(video_url, headers=headers, stream=True)
    reset_file_binary = True
    with open("./"+globals.COUBS_TMP_DIR+"/"+name+".mp4", 'wb') as f:
        for chunk in video_response.iter_content(chunk_size=1024):
            if chunk:
                if reset_file_binary:
                    chunk = fix_first_byte_video(chunk)
                    reset_file_binary = False
                f.write(chunk)


def save_mp3_to(blob_file, name):
    with open("./"+globals.COUBS_TMP_DIR+"/"+name+".mp3", 'wb') as file_handle:
        shutil.copyfileobj(blob_file, file_handle)

def compile(coubid):
    os.system("ffmpeg -i \"{1}{0}.mp4\" -i \"{1}{0}.mp3\" -vcodec libx264 -vf \"scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2\" -acodec copy -shortest {2}{0}.mp4".format(coubid,"./"+globals.COUBS_TMP_DIR+"/","./"+globals.COUNS_SOURCES_DIR+"/"))

def produce():
    logwrite("Temp: "+getTemp()+" C'")
    print(Fore.YELLOW + logwrite("PRODUCIENDO VIDEO: %s"%videoid))
    textfile = open("list.txt", "w")
    sources = glob.glob("./"+globals.COUNS_SOURCES_DIR+"/*")
    for s in sources:
        textfile.write("file './%s/%s'\n" % (globals.COUNS_SOURCES_DIR,os.path.basename(s)))
        textfile.write("file './%s/cut.mp4'\n" % globals.ASSETS_DIR)
    textfile.write("file './%s/end.mp4'\n" % globals.ASSETS_DIR)
    textfile.close()
    os.system("ffmpeg -f concat -safe 0 -i list.txt -i ./{1}/watermark.png -filter_complex \"[0:v][1:v]overlay=x=400:y=560\" -acodec copy -vcodec libx264 {0}/{2}.mp4".format(globals.VIDEO_OUT_DIR,globals.ASSETS_DIR,videoid))
    logwrite("Temp: "+getTemp()+" C'")

def upload():
    #hoy = datetime.datetime.now()
    #mes = hoy.strftime("%B").upper()
    #anio = hoy.strftime("%Y")
    num = col_videos.find().count()
    title = globals.BASE_TITLE_VIDEOS%(num+1)
    creadits = "";
    links = col_coubs.find({"use":videoid})
    for link in links:
        creadits = creadits + "https://coub.com/view/%s\n"%link['permalink']
    description = globals.DESCRIPTION_BASE + creadits
    
    count_tags_actives = col_tags.find({"active":1}).count()
    tags = col_tags.find({"active":1}).limit(globals.TAG_LIMIT).skip(random.randrange(count_tags_actives-globals.TAG_LIMIT))
    tags_list = []
    for tag in tags:
        tags_list.append(tag["text"])

    storage = Storage("api-oauth2.json")
    credentials = storage.get()
    youtube = build(globals.YOUTUBE_API_SERVICE_NAME, globals.YOUTUBE_API_VERSION,
    http=credentials.authorize(httplib2.Http()))
    #Upload
    body=dict(
    snippet=dict(
      title=title,
      description=description,
      tags=tags_list,
      categoryId=24
    ),
    status=dict(
      privacyStatus="public"
    )
    )

    insert_request = youtube.videos().insert(
    part=",".join(body.keys()),
    body=body,
    # The chunksize parameter specifies the size of each chunk of data, in
    # bytes, that will be uploaded at a time. Set a higher value for
    # reliable connections as fewer chunks lead to faster uploads. Set a lower
    # value for better recovery on less reliable connections.
    #
    # Setting "chunksize" equal to -1 in the code below means that the entire
    # file will be uploaded in a single HTTP request. (If the upload fails,
    # it will still be retried where it left off.) This is usually a best
    # practice, but if you're using Python older than 2.6 or if you're
    # running on App Engine, you should set the chunksize to something like
    # 1024 * 1024 (1 megabyte).
    media_body=MediaFileUpload(globals.VIDEO_OUT_DIR+"/"+videoid+".mp4", chunksize=-1, resumable=True)
    )
    response = None
    error = None
    retry = 0
    while response is None:
        try:
            print(Fore.YELLOW + logwrite("SUBIENDO VIDEO: %s"%videoid))
            status, response = insert_request.next_chunk()
            if 'id' in response:
                print(Fore.YELLOW + logwrite("VIDEO SUBIDO ID YOUTUBE: %s"%response['id']))
                logwrite("Temp: "+getTemp()+" C'")
                col_videos.insert([{"id":videoid,"yt":response['id']}])
                #sendMessage("NUEVO VIDEO SUBIDO https://www.youtube.com/watch?v=%s"%response['id'])
            else:
                print(Fore.YELLOW + logwrite("FALLO SUBIDA VIDEO %s : %s"%(videoid,response)))
                exit()
        except HttpError, e:
            if e.resp.status in RETRIABLE_STATUS_CODES:
                error = "A retriable HTTP error %d occurred:\n%s" % (e.resp.status,
                                                                 e.content)
                print(Fore.YELLOW + logwrite("A retriable HTTP error %d occurred:\n%s" % (e.resp.status,
                                                                 e.content)))
            else:
                raise
        except RETRIABLE_EXCEPTIONS, e:
            error = "A retriable error occurred: %s" % e
            print(Fore.YELLOW + logwrite("A retriable error occurred: %s" % e))

        if error is not None:
          print error
          retry += 1
          if retry > MAX_RETRIES:
                print(Fore.YELLOW + logwrite("Cantidad de intentos agotados"))
                exit()

          max_sleep = 2 ** retry
          sleep_seconds = random.random() * max_sleep
          print(Fore.YELLOW + logwrite("Esperando %f segundos para volver a intentar..." % sleep_seconds))
          time.sleep(sleep_seconds)

