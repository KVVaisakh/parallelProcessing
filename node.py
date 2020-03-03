import socket
import sys
import _thread as thread
import random
import time
from datetime import datetime

nodes = []
leader=0

s = socket.socket()
port = int(sys.argv[1])
noOfNodes=int(sys.argv[2])
s.bind(('', port))
s.listen(100)
print("socket binded to "+str(port))

for i in range(noOfNodes):
    node = 5000+i
    nodes.append(node)

leader=nodes[0]
time.sleep(2)

electionProcess=0

def declareLeader():
    global electionProcess
    for i in range(noOfNodes):
        sendMessage(nodes[i],str(port)+" New Leader")
    electionProcess=0

def election():
    global electionProcess
    electionProcess=1
    success=0
    for i in range(noOfNodes):
        if nodes[i]!=port:
            success+=sendMessage(nodes[i],str(port)+" election initiated")
        else:
            break
    if success==0:
        declareLeader()

def sendMessage(sendTo,message):
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        c.connect(("localhost", sendTo))
    except:
        print("node "+str(sendTo)+" is dead")
        if sendTo==leader:
            if electionProcess==0:
                print("election")
                election()
        return 0
    else:
        print("sent -"+str(sendTo)+" - "+message+" "+str(datetime.now()))
        message+=" "+str(datetime.now())
        c.send(message.encode('ascii'))
        c.close()
        return 1

def sendRandom():
    while(1):
        randomNode = random.randrange(noOfNodes)
        if nodes[randomNode]!=port:
            msg=str(port)
            if sendMessage(nodes[randomNode],msg)==0:
                while(electionProcess==1):
                    time.sleep(1)
            time.sleep(5)

try:
    thread.start_new_thread(sendRandom, ())
except:
    print ("Error: unable to start thread")

while(1):
    print("\nCurrent Leader - "+str(leader))
    c, addr = s.accept()
    message = c.recv(2048).decode()
    print("recv -       "+message)

    if message.find(" New Leader")!=-1:
        leader=int(message.split()[0])
        electionProcess=0

    elif message.find(" election initiated")!=-1:
        sendMessage(int(message.split()[0]),str(port)+" Process Started")
        election()

    elif message.find("Roger that")==-1:
        sendMessage(int(message.split()[0]),str(port)+" Roger that")

s.close()