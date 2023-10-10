from socket import *
import json
import time

dnsrecord={}
ttl={}
registertime={}

serverport=53533
serversocket=socket(AF_INET,SOCK_DGRAM)
serversocket.bind(('',serverport))
print("socket listening!")
while True:
    message, clientaddress = serversocket.recvfrom(2048)
    modifiedmessage = json.loads(message.decode()) # type:dict
    #accept register
    if "VALUE" in modifiedmessage:
        currenttime=time.time()
        type=modifiedmessage["TYPE"]
        fsname=modifiedmessage["NAME"]
        fsip=modifiedmessage["VALUE"]
        ttl_s=modifiedmessage["TTL"]
        dnsrecord.update({fsname:fsip})
        ttl.update({fsname:ttl_s})
        registertime.update({fsname:currenttime})
        serversocket.sendto("success".encode(),clientaddress)
        print("AS registered")
    else:
        #accpet query
        type=modifiedmessage["TYPE"]
        fsname=modifiedmessage["NAME"]
        fsip=dnsrecord[fsname]
        currentttl=ttl[fsname]
        if time.time()-registertime[fsname]<=currentttl:
            serversocket.sendto(json.dumps({"TYPE":"A","NAME":fsname,"VALUE":fsip,"TTL":time.ctime(currentttl)}).encode(),clientaddress)
        else:
            serversocket.sendto("498".encode(),clientaddress)
