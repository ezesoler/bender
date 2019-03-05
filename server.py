import flask, pymongo, json, datetime, random
from flask import render_template, abort, request, jsonify
from bson.json_util import dumps
from bson.objectid import ObjectId
from helpers import *
from db import *

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/log', methods=['GET'])
def log():
	USE_TZ = True
	logs = []
	for document in db.log.find().limit(250).sort('_id', pymongo.DESCENDING):
		log = {}
		dlog = document['_id'].generation_time + datetime.timedelta(hours=-3)
		log['date'] = dlog.strftime('%d/%m/%Y %H:%M')
		log['text'] = document['text']
		logs.append(log)
	return render_template('log.html', result = logs)

@app.route('/tags', methods=['GET'])
def tags():
	return render_template('tags.html', result = col_tags.find())

@app.route('/minado', methods=['GET'])
def minado():
	data = {}
	data["total"] = col_coubs.find().count()
	data["notused"] = col_coubs.find({"use":""}).count()
	data["used"] = col_coubs.find({ "use": { "$ne": "" } }).count()
	return render_template('minado.html', result = data)

@app.route('/tag/set', methods=['POST']) 
def tset():
	if not request.json:
		abort(400)
	col_tags.update_one({'_id':ObjectId(request.json["id"])}, {"$set": {"active": request.json["val"]}}, upsert=False)
	return jsonify({"result":"ok"})

@app.route('/api/v1/simulate', methods=['POST']) 
def simulate():
	if not request.json:
		abort(400)
	num_coubs = random.randint(globals.COUBS_PER_VIDEO_MIN,globals.COUBS_PER_VIDEO_MAX)
	coubs = col_coubs.find({"use":"","nsfw":False,"categories.id":{"$nin":[36,24]}}).limit(num_coubs).sort(request.json["order"],pymongo.DESCENDING)
	return dumps(coubs)

@app.route('/api/v1/log', methods=['GET'])
def api_log():
    return dumps(db.log.find())

@app.route('/api/v1/temp', methods=['GET'])
def api_temp():
    return jsonify({"result":getTemp()})

app.run(host='0.0.0.0')