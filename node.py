#simple python peer to peer network using the p2pnetwork module. It uses a simple model for information exchange between peers.
# Author: Giannis Tsolakis
# no liscence do whatever you want

from p2pnetwork.node import Node
import time
import json
import sys

#don't have to add a lot of peers
#just one so the node can connect to the network
peers = ['192.168.1.6']
maxpeers = 5
connected_peers = 0
node1 = None
PORT = 65432


def ConnectToNodes(nn):
    global connected_peers
    global peers
    global maxpeers

    if connected_peers+nn>maxpeers:
        nn = maxpeers-connected_peers

    if connected_peers >== maxpeers:
        print("FUCK FUCK FUCK, too much peers, how did this happen?? fuck")
        return
    if nn > len(peers):
        nn = len(peers)

    for i in range(nn):
        node1.connect_with_node(peers[i], PORT)
    return

def message(dict):
    buf = json.dumps(dict)
    return buf

def peers_packet():
    global peers
    buf = {'peers': peers}
    buf = json.dumps(buf)
    return buf

def send_peers():
    node.send_to_nodes(peers_packet())
    return

def data_handler(data):
    global peers
    dta = {'test': 'lol'}
    dta = json.loads(data)
    if "peers" in dta:
        new = [i for i in peers if i not in dta["peers"]]
        peers = dta["peers"] + new
        print("new neighbours: " + str(new))
        ConnectToNodes(len(new)) # cpnnect to new nodes
        return
    elif "msg" in dta:
        print("msg: " + dta["msg"])
        node.send_to_nodes(dta)
        return

def node_callback(event, node, other, data):
    if (event == 'node_request_to_stop'):
        print("node request to stop")
    elif ( event == "inbound_node_disconnected" ):
        print("NODE (" + node.getName() + "): " + "event:" + event + "\n")
    elif ( event == "outbound_node_disconnected" ):
        print("NODE (" + node.getName() + "): " + "event:" + event + "\n")
    elif ( event == "outbound_node_connected" ):
        print("NODE (" + node.getName() + "): " + "event:" + event + "\n")
    elif ( event == "inbound_node_connected" ):
        send_peers()
        print("NODE (" + node.getName() + "): " + "event:" + event + "\n")
    elif ( event == "node_message" ):
        data_handler(data.encode('utf-8'))
    else:
        print("NODE (" + node.getName() + "): Event is not known " + event + "\n")

node = Node("", PORT, node_callback) # start the node
node.start()
time.sleep(1)

ConnectToNodes(1) # connect to the start node to enter the network
while 1:
    buf = str(message({'msg': "test123"}))
    node.send_to_nodes(buf)
    time.sleep(2)
time.sleep(5)

node.stop()
print('end')
