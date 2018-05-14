#
############################################################
#
#        Filename:
#
#     Description:
#
#         Version:  1.0
#  Python Version:  3.x
#
#          Author:  Paul Robin , paul.robin@etu.unistra.fr
#
############################################################

#!/usr/bin/python3

import rpyc
from rpyc.utils.server import ThreadedServer

from queue import *
from threading import Thread

from .participant_node import ope_generator as og


class Neighborhood():
    def __init__(self):
        self.neighbours = []

    def connect_node(self,idt,port):
        self.neighbours.append(Neighbour(idt,port))
        self.neighbours[-1].connect()

    def for_all_but_one(self, mess, the_one):
        for n in self.neighbours:
            if(the_one != n.idt):
                n.c.root.dist_queue(mess)

    def for_all(self, mess):
        for n in self.neighbours:
            n.c.root.dist_queue(mess)

class Neighbour():
    def __init__(self,idt,port):
        self.idt = idt
        self.port = port
        self.c = None
    
    def connect(self):
        self.c = rpyc.connect("localhost",self.port)

class Bridge(Thread):
    def __init__(self,ip,port):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.t = None

    def run(self):
        self.t = ThreadedServer(InConnectService, port=self.port)
        self.t.start()
        print("fin")


class InConnectService(rpyc.Service):
    def on_connect(self):
        print("connection")
        pass

    def on_disconnect(self):
        pass

    def exposed_dist_queue(self,in_come):
        global queue
        mess = og.Missive()
        mess.str_injection(in_come)
        queue.put(mess)
        pass

if __name__ == '__main__' :
    queue = Queue()
    t = ThreadedServer(InConnectService,port=18861)
    t.start()
