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

from participant_node import p_node as pn
from op_factory import ope_generator as mg
from threading import Thread, Semaphore
from queue import *
import sys

class Participant(Thread):
    def __init__(self, queue, dest, host, mtrcl, sem, l_prt):
        Thread.__init__(self)
        self.q = queue
        self.dest = dest
        self.address= [mtrcl,host]
        self.sem = sem
        self.l_prt = l_prt

    def run(self):
        counter = 0
        self.dest.append(self.address)
        message = mg.m_builder(counter,self.address,'C')
        self.q.put(message)
        life = pn.p_life(3,6)
        test = 2
        while(life):
            counter += 1
            life -= 1
            v = pn.p_trans([1,10])
            pn.p_slp([1,20])
            dstnt = pn.p_dstnt(self.dest,self.address)
            #bout de code pour verifier qu'il y ai bien une destination
            #si il n'y en a pas att un petit temps, et reessaye
            #au bout d'un certain nombre d'essai non concluant successif
            #le participant s'arretera
            if(not(dstnt)):
                if(not(test)):
                    message = mg.m_builder(counter,self.address,'E')
                    self.q.put(message)
                    break
                else :
                    test -= 1
                    pn.p_slp([2,2])
                    counter -= 1
                    life += 1
                    continue
            test = 2
            message = mg.m_builder(counter,self.address,'T',dstnt,v)
            self.q.put(message)
        counter += 1
        message = mg.m_builder(counter,self.address,'D')
        self.q.put(message)
        self.dest.remove(self.address)
        self.l_prt.remove(self)
        self.sem.release()
        return

class Manager(Thread):
    #nb : float('inf') represente l'infinit, marche aussi pour des comparaisons d'int
    def __init__(self, queue, dest, host, max_p=50, tot_p=float('inf')):
        Thread.__init__(self)
        self.q = queue
        self.dest = dest
        self.h = host
        self.tot_p = tot_p
        self.sem = Semaphore(max_p)
        #use semaphore to stop the manager thread to create more 
        #participants than expect

    def run(self):
        nb_prtcpt = 0
        cur_prts = []
        while(nb_prtcpt < self.tot_p):
            self.sem.acquire()
            cur_prts.append(Participant(self.q, self.dest, self.h, nb_prtcpt, self.sem, cur_prts))
            cur_prts[-1].start()
            nb_prtcpt += 1
        return


if __name__ == '__main__' :

    queue = Queue()
    l_ope = []
    destination = []
    m = Manager(queue, destination, 0, 1, 3)
    m.start()
    while(True):
        try :
            tmp = queue.get(True,1)
        except Empty :
            print('fin')
            break
        l_ope.append(tmp)
    for i in l_ope:
        print(i)
