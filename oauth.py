# -*- coding: utf-8 -*-
import sys
import os
import httplib2
import globals
from oauth2client.file import Storage
from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.tools import argparser, run_flow
from colorama import init, Fore, Back, Style
init()

httplib2.RETRIES = 1

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the Developers Console
https://console.developers.google.com/

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   globals.CLIENT_SECRETS_FILE))


def main():
	banner()
	print(get_authenticated_service())


def clear():
	os.system('cls' if os.name == 'nt' else 'clear')


def banner():
	clear()
	print(Fore.GREEN + '''
  ___ ___ _  _ ___  ___ ___  
 | _ ) __| \| |   \| __| _ \ 
 | _ \ _|| .` | |) | _||   / 
 |___/___|_|\_|___/|___|_|_\ 
  by EzeSoler          v %s  
		''' % globals.VERSION['num'])
	print(Fore.CYAN + "Generador de OAUTH 2 API Youtube v3")

def get_authenticated_service():
  flow = flow_from_clientsecrets(globals.CLIENT_SECRETS_FILE,
    scope=globals.YOUTUBE_UPLOAD_SCOPE,
    message=MISSING_CLIENT_SECRETS_MESSAGE)

  storage = Storage("api-oauth2.json")
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    credentials = run_flow(flow, storage)

  return build(globals.YOUTUBE_API_SERVICE_NAME, globals.YOUTUBE_API_VERSION,
    http=credentials.authorize(httplib2.Http()))

main()