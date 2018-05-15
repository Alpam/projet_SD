#
############################################################
#
#        Filename:master_node.py
#
#     Description:
#
#         Version:  1.0
#  Python Version:  3.x
#
#          Author:  Paul Robin , paul.robin@etu.unistra.fr
#                   Amarin Hutt, amarinhutt@hotmail.fr
#
############################################################

#!/usr/bin/python3

from queue import *
import threading
from threading import Thread
import time

import rpyc
from rpyc.utils.server import ThreadedServer

from bloc_node import p_manager as pm
from bloc_node import p_node as pn
from bloc_node import ope_generator as og
from bloc_node import bloc as bc
from bloc_node import b_pow as bp
from monitor import Monitor

import sys

def core_node(my_n,ip,port,init_particpant,init_neighbours,queue):

    #mise en place
    q = Queue()
    name = my_n
    fn = "log_"+name+".log"
    monitor = Monitor(q,fn)
    monitor.start()
    generate_bloc = 0
    depth = 0
    blocChain = []
    blocChain.append(bc.Bloc(name,0))
    required = 5
    l_ope = []
    destination = []
    running = True
    
    #set up voisinage et connection
    bridge = Bridge(ip,port)
    bridge.start()
    
    time.sleep(5)
    
    nghbrhd = Neighborhood()

    for nghbr in init_neighbours:
        nghbrhd.connect_node(nghbr[0],nghbr[1])

    
    #set up Manager et Hashage
    m = pm.Manager(queue, destination, init_particpant[0] \
                                     , init_particpant[1] \
                                     , init_particpant[2] \
                                     , init_particpant[3] \
                                     , init_particpant[4] \
                                     , init_particpant[5] \
                                     , init_particpant[6])
    pw = bp.HashFactory(aggregation_bloc(blocChain) \
                       ,required,1,name,queue)
    #démarrage
    m.start()
    pw.start()

    #gestion évènement sur la queue
    while(running):
        n_ope = None
        n_bc  = list()
        m = queue.get()
        if(m.m_type == "S"):
            n_ope = og.Operation()
            n_ope.str_injection(m.str_obj)
            v = is_in(l_ope,n_ope,blocChain)
            if(not(v)):
                last = m.transmitter
                q.put(m)
                m.transmitter = name
                nghbrhd.for_all_but_one(m.translation(),last)
                if(n_ope.m_type == "T"):
                    l_ope.append(n_ope)
                    m=None
                elif(n_ope.m_type == "C"):
                    l_ope.append(n_ope)
                    destination.append([n_ope.origin[0],n_ope.origin[1]])
                    m=None
                elif(n_ope.m_type == "D"):
                    l_ope.append(n_ope)
                    destination.remove([n_ope.origin[0],n_ope.origin[1]])
                    m=None
                elif(n_ope.m_type == "E"):
                    m=None
            else:
                m.m_type = 'Q'
                q.put(m)
                m=None
        elif(m.m_type == "R"):
            n_bc = generate_bc(m.str_obj)
            if(n_bc[0].depth > depth):
                pw.exit()
                depth = n_bc[0].depth
                blocChain = n_bc
                clean_l_ope(blocChain,l_ope)
                last = m.transmitter
                q.put(m)
                m.transmitter = name
                nghbrhd.for_all_but_one(m.translation(),last)
                if(len(l_ope)==0 and len(destination)==0):
                    bridge.t.close()
                    q.put("")
                    return
                pw = bp.HashFactory(aggregation_bloc(blocChain)\
                                   ,required,depth+1,name,queue)
                pw.start()
            else:
                m.m_type = 'P'
                q.put(m)
            m=None
        else:
            if(m.m_type == "G"):
                if(m.ident <= depth):
                    m = None
                    pw = bp.HashFactory(aggregation_bloc(blocChain)\
                                   ,required,depth+1,name,queue)
                    pw.start()
                else:
                    depth = m.ident
                    n_bloc = bc.Bloc(name,m.ident)
                    n_bloc.mhash = m.m_hash
                    n_bloc.nonce = m.nonce
                    n_bloc.listope = list()
                    n_bloc.nbope = 0
                    for ope in l_ope :
                        n_bloc.nbope += 1
                        n_bloc.listope.append(ope)
                    l_ope = list()
                    n_lst = [n_bloc]
                    n_lst.extend(blocChain)
                    blocChain = list(n_lst)
                    n_bloc = None
                    mess = og.Missive()
                    mess.obj_injection('R',generate_string_from_bc(blocChain),name)
                    nghbrhd.for_all(mess.translation())
                    q.put(mess)
                    pw = bp.HashFactory(aggregation_bloc(blocChain)\
                                       ,required,depth+1,name,queue)
                    pw.start()
                    m=None
            elif(m.m_type == "T"):
                l_ope.append(m)
                mess = og.Missive()
                mess.obj_injection('S',m.translation(),name)
                nghbrhd.for_all(mess.translation())
                q.put(mess)
                m=None
            elif(m.m_type == "C"):
                destination.append([m.origin[0],m.origin[1]])
                l_ope.append(m)
                mess = og.Missive()
                mess.obj_injection('S',m.translation(),name)
                nghbrhd.for_all(mess.translation())
                q.put(mess)
                m=None
            elif(m.m_type == "D"):
                destination.remove([m.origin[0],m.origin[1]])
                l_ope.append(m)
                mess = og.Missive()
                mess.obj_injection('S',m.translation(),name)
                nghbrhd.for_all(mess.translation())
                q.put(mess)
                m=None
            elif(m.m_type == "E"):
                mess = og.Missive()
                mess.obj_injection('S',m.translation(),name)
                q.put(mess)
                m=None
        if(len(l_ope)==0 and len(destination)==0):
            pw.exit()
            bridge.t.close()
            q.put("")
            return
            
def aff_bc(bc):
    for b in bc:
        print(b)

def is_in(list_ope,ope,blc):
    for ele in list_ope:
        if(ope == ele):
            return True
    for b in blc:
        for ele in b.listope:
            if(ope == ele):
                return True
    return False

def aggregation_bloc(blocs):
    string = ""
    for b in blocs:
        string += b.translation()
    return string

def generate_bc(str_obj):
    blc = []
    for n in str_obj.split(' '):
        b = bc.Bloc("","")
        b.str_injection(n)
        blc.append(b)
    return blc

def generate_string_from_bc(blc):
    s =""
    for b in blc:
        s += b.translation() + " "
    return s[:-1]

def clean_l_ope(blc, l_ope):
    for b in blc:
        for op in b.listope:
            if(l_ope.count(op)):
                l_ope.remove(op)

class Neighborhood():
    def __init__(self):
        self.neighbours = []

    def connect_node(self,idt,port):
        self.neighbours.append(Neighbour(idt,port))
        self.neighbours[-1].connect()

    def for_all_but_one(self, mess, the_one):
        for n in self.neighbours:
            if(the_one != n.idt):
                try:
                    n.c.root.dist_queue(mess)
                except EOFError:
                    pass

    def for_all(self, mess):
        for n in self.neighbours:
            try:
                n.c.root.dist_queue(mess)
            except EOFError:
                pass
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
    if(len(sys.argv)<11):
        print("err argv")
    else:
        queue = Queue()
        core_node(sys.argv[1] \
             ,sys.argv[2] \
             ,int(sys.argv[3]) \
             ,[int(sys.argv[1]) \
             ,int(sys.argv[4]) \
             ,int(sys.argv[5]) \
             ,int(sys.argv[6]) \
             ,[0,100] \
             ,1 \
             ,[2,0.025]] \
             ,[[sys.argv[7],int(sys.argv[8])],[sys.argv[9],int(sys.argv[10])]]\
             ,queue)

