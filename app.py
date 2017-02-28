import requests
import threading
import redis
import json
from flask import Flask, request, render_template

redisPool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)
app = Flask(__name__)

def getVariable(variable_name):
    my_server = redis.Redis(connection_pool=redisPool)
    response = my_server.get(variable_name)
    return response

def setVariable(variable_name, variable_value):
    my_server = redis.Redis(connection_pool=redisPool)
    my_server.set(variable_name, variable_value)

def sync():
  threading.Timer(300.0, sync).start()
  data = requests.get("https://www.nseindia.com/live_market/dynaContent/live_analysis/gainers/niftyGainers1.json").text
  setVariable("niftyGainers", data)


#APP ROUTES
@app.route('/', methods=['GET'])
def index():
	return render_template("index.html", niftyGainers=getVariable("niftyGainers"))

if __name__ == '__main__':
	sync()
	app.run(host='0.0.0.0', port=8000, debug=True)