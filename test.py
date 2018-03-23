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

from bloc_node import bloc_chain as bc, b_pow as bp
from participant_node import p_node as pn
from threading import Thread, RLock
from queue import *

class Slave(Thread):

    def __init__(self,nom,queue):
        Thread.__init__(self)
        self.nom = nom+":"
        self.q = queue
        self.lock = RLock()

    def run(self):
        self.lock.acquire(False)
        life = 3
        while(life):
            message = self.nom+"M"+str(life)+":"+str(pn.p_work())
            self.q.put(message)
            life -= 1
        self.lock.release()

class Master(Thread):

    def __init__(self,queue,slaves,list_operations):
        Thread.__init__(self)
        self.q = queue
        self.ss = slaves
        self.ope = list_operations

    def run(self):

        while(len(self.ss) or not(self.q.empty())):
            self.ope.append(self.q.get())
            for s in self.ss:
                if(s.lock.acquire()):
                    self.ss.remove(s)
            
if __name__ == '__main__' :
    queue = Queue()
    list_operations = []
    slaves = [Slave("S1",queue), Slave("S2",queue)]
    master = Master(queue, slaves,list_operations)
    for s in slaves:
        s.start()
    master.start()
    master.join()
    print(list_operations)

