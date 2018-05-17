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

"""
    core_node est la fonction principale.
    elle lance les threads dédier aux participants,
    au serveur d'écoute, à la génération de hash
    et au monitor.
    elle gère égale la réception et gestion des différentes
    opération et missive quel génère via ces threads fils
    ou quelle réception des autres nodes
"""

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
    my_destination = {}
    running = True
    count_bl_vide = 0

    #set up voisinage et connection
    bridge = Bridge(ip,port)
    bridge.start()
    
    #temps d'attente utilisé pour s'assurer que tous
    #les serveurs soient bien lancés
    time.sleep(5)

    nghbrhd = Neighborhood()
    #connection aux nodes voisins
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
        #mise en log de l'état des participants
        q.put(d_str(my_destination))
        n_ope = None
        n_bc  = list()
        #reception d'une missive ou d'une opération
        #sur la Queue puis traitement
        m = queue.get()
        #si missive 'S' (contenant une opération)
        if(m.m_type == "S"):
            #on inject l'op contenue dans un obj
            n_ope = og.Operation()
            n_ope.str_injection(m.str_obj)
            #on vérifie si elle est connue
            v = is_in(l_ope,n_ope,blocChain)
            #si non connue
            if(not(v)):
                #la traite au cas pas cas
                last = m.transmitter
                #transmission au monitor
                q.put(m.copy())
                m.transmitter = name
                #elle retransmise à tous sauf à celui qui la envoyée
                nghbrhd.for_all_but_one(m.translation(),last)
                if(n_ope.m_type == "T"):
                    l_ope.append(n_ope)
                    m=None
                elif(n_ope.m_type == "C"):
                    if(is_not_in_dest(n_ope,destination)):
                        l_ope.append(n_ope)
                        destination.append([n_ope.origin[0],n_ope.origin[1]])
                    m=None
                elif(n_ope.m_type == "D"):
                    l_ope.append(n_ope)
                    #pour une raison inconnue il arrive que certaine deconnection
                    #arrive plusieurs fois ou avant une connection (qui n'arrive jamais
                    #en vrai) lors de testes sur des réseaux complexes
                    #d'où le cath de l'erreur raised par python
                    try:
                        destination.remove([n_ope.origin[0],n_ope.origin[1]])
                    except ValueError:
                        pass
                    m=None
                elif(n_ope.m_type == "E"):
                    l_ope.append(n_ope)
                    m=None
            else:
                #la missive est transmise au monitor avec le type Q
                m.m_type = 'Q'
                q.put(m.copy())
                m=None
        elif(m.m_type == "R"):
            #on récupère la bloc chaine entrante
            n_bc = generate_bc(m.str_obj)
            if(n_bc[0].depth > depth):
                #si valide on stop l'ancienne génération de hash
                pw.exit()
                depth = n_bc[0].depth
                blocChain = n_bc
                clean_l_ope(blocChain,l_ope)
                last = m.transmitter
                #on la donne au monitor puis on la transmet au reseau
                #sauf émetteur
                q.put(m.copy())
                m.transmitter = name
                nghbrhd.for_all_but_one(m.translation(),last)
                #si la profondeur est suffisante on valide les transactions
                #a depth_max-3
                if(depth > 2):
                    validation_transaction(blocChain[2], my_destination)
                #si plus d'opération en attente et plus de destination fin
                if(len(l_ope)==0 and len(destination)==0):
                    bridge.t.close()
                    q.put("end")
                    return
                #on redemarre le calcule de hash
                pw = bp.HashFactory(aggregation_bloc(blocChain)\
                                   ,required,depth+1,name,queue)
                pw.start()
            else:
                #si bloc chaine invalide transmis au monitor avec le type P
                m.m_type = 'P'
                q.put(m.copy())
            m=None
        else:
            #si message sur la queue est une opération
            if(m.m_type == "G"):
                #si création de bloci
                if(m.ident <= depth):
                    #si invalide on drop et relance le calcule de hash
                    m = None
                    pw = bp.HashFactory(aggregation_bloc(blocChain)\
                                   ,required,depth+1,name,queue)
                    pw.start()
                else:
                    #si valide on 'paye' nos participants
                    #et on met à jour la bloc chain avant de la transmettre
                    pay_all(my_destination)
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
                    q.put(mess.copy())
                    #pour empécher de tourner en boucle sur la terminaison
                    #on vérifie si il y eut plus de 10 bloc vide crée
                    #si oui on quitte
                    if(blocChain[0].nbope==0):
                        count_bl_vide+=1
                    else:
                        count_bl_vide=0
                    if(count_bl_vide>10):
                        bridge.t.close()
                        q.put("end")
                        print(name + " : trop de bloc vide créé, arrêt")
                        return
                    if(depth > 2):
                        validation_transaction(blocChain[2], my_destination)
                    pw = bp.HashFactory(aggregation_bloc(blocChain)\
                                       ,required,depth+1,name,queue)
                    pw.start()
                    m=None
            elif(m.m_type == "T"):
                #si T on augment la contribution du participant
                #puis on calcule la valeur qu'il envoie
                #puis transmission
                pay_prtcp(my_destination,d_k(m.origin))
                m.value = round(my_destination[d_k(m.origin)][1]*m.value/100,3)
                l_ope.append(m)
                mess = og.Missive()
                mess.obj_injection('S',m.translation(),name)
                nghbrhd.for_all(mess.translation())
                q.put(mess.copy())
                m=None
            elif(m.m_type == "C"):
                #connection d'un de nos participants
                destination.append([m.origin[0],m.origin[1]])
                my_destination[d_k(m.origin)]=[1,1,0]
                arr_prtcp(my_destination,d_k(m.origin))
                l_ope.append(m)
                mess = og.Missive()
                mess.obj_injection('S',m.translation(),name)
                nghbrhd.for_all(mess.translation())
                q.put(mess.copy())
                m=None
            elif(m.m_type == "D"):
                #deconnection d'un de nos participants
                destination.remove([m.origin[0],m.origin[1]])
                my_destination[d_k(m.origin)][0]=0
                dec_prtcp(my_destination,d_k(m.origin))
                l_ope.append(m)
                mess = og.Missive()
                mess.obj_injection('S',m.translation(),name)
                nghbrhd.for_all(mess.translation())
                q.put(mess.copy())
                m=None
            elif(m.m_type == "E"):
                #message d'erreur d'un de nos participants
                mess = og.Missive()
                mess.obj_injection('S',m.translation(),name)
                q.put(mess.copy())
                m=None
        #cas de terminaison
        if(len(l_ope)==0 and len(destination)==0):
            pw.exit()
            try:
                bridge.t.close()
            except OSError:
                pass
            q.put("end")
            return
    pw.exit()
    try:
        bridge.t.close()
    except OSError:
        pass
    q.put("end")
    return

def is_not_in_dest(ope,destination):
    for d in destination:
        if(ope.origin[0]==d[0] and\
           ope.origin[1]==d[1]):
            return False
    return True

#transaction à depth_max-3, on la rend effective
def validation_transaction(bl, d):
    for ope in bl.listope:
        if (ope.m_type == 'T'):
            if(d_k(ope.origin)in d):
                d[d_k(ope.origin)][1]-=ope.value
            elif(d_k(ope.dstntn)in d):
                d[d_k(ope.dstntn)][1]+=ope.value

#transforme une liste en str (pour clef dicotionnaire
#my_destination
def d_k(l):
    return str(l[0])+'-'+str(l[1])

#recalcule de la distribution de contribution à
#l'arriver d'un participant
def arr_prtcp(d,n_p):
    nb_co=0
    for e in d:
        if(d[e][0]):
            nb_co += 1
    d[n_p][2]+=100/nb_co
    if(nb_co==1):
        return
    for e in d:
        if(e!=n_p and d[e][0]):
            d[e][2]-=(100/(nb_co*(nb_co-1)))
    return

#recalcule de la distribution de contribution à
#la déconnection d'un participant
def dec_prtcp(d,l_p):
    nb_co=0
    for e in d:
        if(d[e][0]):
            nb_co += 1
    for e in d:
        if(d[e][0]):
            d[e][2] += (d[l_p][2]/nb_co)

#on ajoute de la valeur en fonction de la
#contribution du participant
def pay_all(d):
    for e in d:
        if(d[e][0]):
            d[e][1] += d[e][2]/100

#augmentation de la contribution d'un participant
#lors d'une transaction
def pay_prtcp(d,b_p):
    v = 100-d[b_p][2]
    if(not(v)):
        return
    for e in d:
        if(d[e][0]):
            if(e == b_p):
                d[e][2] += 1
            else:
                d[e][2] -= d[e][2]/v

#traduit un dico en str
def d_str(d):
    if(not(len(d))):
        return ""
    rtr = ""
    for e in d:
        rtr += e
        if (d[e][0]):
            rtr += "(c):"
        else:
            rtr += "(d):"
        rtr += str(round(d[e][1],3))+':'+str(round(d[e][2],3))+'||'
    return rtr[:-2]

#affiche une bloc chaine
def aff_bc(blc):
    for b in blc:
        print(b)

#vérifie si une operation est dans la
#liste d'opération en attente ou dans la
#bloc chaine
def is_in(list_ope,ope,blc):
    for ele in list_ope:
        if(ope == ele):
            return True
    for b in blc:
        for ele in b.listope:
            if(ope == ele):
                return True
    return False

#additionne plusieurs blocs en une grosse str
def aggregation_bloc(blocs):
    string = ""
    for b in blocs:
        string += b.translation()
    return string

#genere une bloc chaine à partir d'une str
def generate_bc(str_obj):
    blc = []
    for n in str_obj.split(' '):
        b = bc.Bloc("","")
        b.str_injection(n)
        blc.append(b)
    return blc

#genere une string formater à partir d'une bloc chaine
def generate_string_from_bc(blc):
    s =""
    for b in blc:
        s += b.translation() + " "
    return s[:-1]

#retire les operations presentes dans une bloc chaine
#d'une liste d'opération
def clean_l_ope(blc, l_ope):
    for b in blc:
        for op in b.listope:
            if(l_ope.count(op)):
                l_ope.remove(op)


"""
    classe représentant les voisins d'un node
"""
class Neighborhood():
    def __init__(self):
        self.neighbours = []
    #permet la connection à un node
    def connect_node(self,idt,port):
        self.neighbours.append(Neighbour(idt,port))
        self.neighbours[-1].connect()

    #envoie un message à tous les voisins sauf the_one
    def for_all_but_one(self, mess, the_one):
        for n in self.neighbours:
            if(the_one != n.idt):
                try:
                    n.c.root.dist_queue(mess)
                except EOFError:
                    continue
        pass

    #envoie un message à tous les voisins
    def for_all(self, mess):
        for n in self.neighbours:
            try:
                n.c.root.dist_queue(mess)
            except EOFError:
                continue
        pass

"""
    classe représentant un voisin
"""
class Neighbour():
    def __init__(self,idt,port):
        self.idt = idt
        self.port = port
        #self.c est l'objet issue de rpyc qui sert
        #à la connection à ce voisin
        self.c = None

    def connect(self):
        self.c = rpyc.connect("localhost",self.port)

"""
    classe gérant le serveur d'écoute
"""
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

"""
    classe gérant le service de connection et de déconnection
"""
class InConnectService(rpyc.Service):
    def on_connect(self):
        print("connection")
        pass
    
    def exposed_dist_queue(self,in_come):
        global queue
        mess = og.Missive()
        mess.str_injection(in_come)
        queue.put(mess)
        pass


if __name__ == '__main__' :
    if(len(sys.argv)<9):
        print("err argv")
    else:
        queue = Queue()
        l_voisin = []
        i=7
        while(i<len(sys.argv)):
            tmp = []
            tmp.append(sys.argv[i])
            i += 1
            tmp.append(int(sys.argv[i]))
            l_voisin.append(tmp)
            i += 1
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
             ,l_voisin\
             ,queue)

