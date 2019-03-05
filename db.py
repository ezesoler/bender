import globals
from pymongo import MongoClient

#MongoDB 2.4:
client = MongoClient(globals.DATABASE_CONFIG['host'])
client.admin.authenticate(globals.DATABASE_CONFIG['user'], globals.DATABASE_CONFIG['password'])

#MongoDB 3.2:
#client = MongoClient(globals.DATABASE_CONFIG['host'],
#						username=globals.DATABASE_CONFIG['user'],
#						password=globals.DATABASE_CONFIG['password'],
#						authSource=globals.DATABASE_CONFIG['auth'])


db = client.benderdb

col_coubs = db.coubs
col_videos = db.videos
col_stats = db.stats
col_tags = db.tags

col_coubs.create_index("permalink",unique=True)

def logwrite(text):
	db.log.insert([{"text":text}])
	return text
