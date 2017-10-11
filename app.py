from flask import Flask, jsonify, request
import requests
import config
import sys
import pymongo
import json
from bson.json_util import dumps
from bson import json_util
apiKey=config.api_key
app=Flask(__name__)

# cnx = mysql.connector.connect(user='bsoares', password='GOmanny1436',
#                               host='rds-mysql-fanfootball.cwmwr07yxatm.us-east-1.rds.amazonaws.com',
#                               database='FanFootball')
# cursor = cnx.cursor()
# query = ("SELECT * FROM RBTable")
         


@app.route('/summoner/<string:name>', methods=['GET'])
def summoner(name):
	r=requests.get("https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/"+name+"?api_key="+apiKey)
	json=r.json()
	return jsonify(json)

@app.route('/matchlist/<string:accountId>', methods=['GET'])
def getMatchList(accountId):
	matchlist=requests.get("https://na1.api.riotgames.com/lol/match/v3/matchlists/by-account/"+accountId+"?queue=420&endIndex=20&beginIndex=0&api_key="+apiKey)
	json=matchlist.json()
	return jsonify(json)

@app.route('/league/<string:summonerId>', methods=['GET'])
def league(summonerId):
	league=requests.get("https://na1.api.riotgames.com/lol/league/v3/leagues/by-summoner/"+summonerId+"?api_key="+apiKey)
	json=league.json()
	return jsonify(json)

@app.route('/matchData/<string:matchId>', methods=['GET'])
def getMatchData(matchId):
	#need to upgrade this to match with the timing in the app
	#threading.Timer(1.0, getMatchData).start()
	matchData=requests.get("https://na1.api.riotgames.com/lol/match/v3/matches/"+matchId+"?api_key="+apiKey)
	json=matchData.json()
	return jsonify(json) 

@app.route('/')
def index():
	return ("Brian's API")

uri = "mongodb://bsoares:gomanny24@ds141474.mlab.com:41474/meanappdb_soares"
client = pymongo.MongoClient(uri)
db = client.get_default_database()
players = db['players']
@app.route('/ffb', methods='GET')
def index():
	documents = [doc for doc in players.find(sort=[("value",-1)]).limit(60)]
	return json_util.dumps({'cursor': documents})

if __name__ =='__main__':
	app.run()