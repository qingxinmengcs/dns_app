import flask
from flask import Flask, abort,request
from socket import *
import json
import requests
import time

app = Flask(__name__)

def Fib(value):
    if value<=1:
        return value
    return(Fib(value-1)+Fib(value-2))

@app.route("/register", methods=['PUT'])
def hello_world():
    data=request.get_json()
    hostname=data["hostname"]
    ip=data["ip"]
    as_ip=data["as_ip"]
    as_port=data["as_port"]

    servername = as_ip
    serverport = int(as_port)
    clientsocket = socket(AF_INET, SOCK_DGRAM)
    message = json.dumps({"TYPE": "A", "NAME": hostname,"VALUE":ip,"TTL":10}) #10000seconds to test
    clientsocket.sendto(message.encode(), (servername, serverport))
    return "modified",201

@app.route("/fibonacci", methods=['GET'])
def fibonacci():
    value = int(flask.request.args.get("number"))
    if not isinstance(value,int):
        return 400
    value=Fib(value)
    return str(value),200

app.run(host='0.0.0.0',
        port=9090,
        debug=True)