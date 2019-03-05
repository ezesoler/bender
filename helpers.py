import requests, globals, subprocess
from fake_useragent import UserAgent


def sendMessage(message):
	ua = UserAgent()
	headers = {'User-Agent': ua.random}
	requests.get('https://api.telegram.org:443/bot{0}/sendMessage?chat_id={1}&parse_mode=Markdown&text={2}'.format(globals.BOT_TELEGRAM_TOKEN,globals.BOT_TELEGRAM_CHAT_ID,message), headers=headers)

def getTemp():
	output = subprocess.check_output("vcgencmd measure_temp",shell = True).split("=")
	return output[1].split("'")[0]