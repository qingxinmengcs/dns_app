import flask
from flask import Flask, abort
from socket import  *
import json
import requests

app = Flask(__name__)

@app.route("/fibonacci",methods = ['GET'])
def hello_world():
    hostname = flask.request.args.get("hostname")
    fs_port = flask.request.args.get("fs_port")
    number = flask.request.args.get("number")
    as_ip = flask.request.args.get("as_ip")
    as_port = flask.request.args.get("as_port")
    if (hostname==None or fs_port==None or number==None or as_ip==None or as_port==None):
        return "missing",400
    servername=as_ip
    serverport=int(as_port)
    clientsocket=socket(AF_INET,SOCK_DGRAM)
    message=json.dumps({"TYPE":"A","NAME":"fibonacci.com"})
    clientsocket.sendto(message.encode(),(servername,serverport))
    modifiedmessage,serveraddress=clientsocket.recvfrom(2048)
    modifiedmessage=modifiedmessage.decode()
    if modifiedmessage=="498":
        return "dns expired",498
    modifiedmessage=json.loads(modifiedmessage)
    fs_ip=modifiedmessage["VALUE"]
    fsquery="http://{}:{}/fibonacci?number={}".format(fs_ip,fs_port,number)
    value=requests.get(fsquery)
    value=value.content.decode()
    return "The result is "+str(value),200

app.run(host='0.0.0.0',
        port=8080,
        debug=True)