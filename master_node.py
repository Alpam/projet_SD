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

from queue import *
import threading
import time

from bloc_node import p_manager as pm
from bloc_node import p_node as pn
from bloc_node import ope_generator as og
from bloc_node import bloc as bc
from bloc_node import b_pow as bp
from bloc_node import bridge as bdg

def core_node(my_n,ip,port,init_particpant,init_neighbours,lock):

    #mise en place
    name = my_n
    stopPowBC = [False]
    generate_bloc = 0
    queue = Queue()
    depth = 0
    blocChain = []
    blocChain.append(bc.Bloc(name,0))
    required = 6
    l_ope = []
    destination = []
    running = True
    
    #set up voisinage et connection
    bridge = bdg.Bridge(ip,port)
    bridge.start()
    
    lock.acquire()
    
    nghbrhd = bdg.Neighborhood()

    for nghbr in init_neighbours:
        nghbrhd.connect_node(nghbr[0],nghbr[1])

    print("fin")
    
    #set up Manager et Hashage
    m = pm.Manager(queue, destination, init_particpant[0] \
                                     , init_particpant[1] \
                                     , init_particpant[2])
    pw = bp.HashFactory(stopPowBC,aggregation_bloc(blocChain) \
                       ,required,depth,name,queue)
    #démarrage
    m.start()
    pw.start()

    #gestion évènement sur la queue
    while(running):
        m = queue.get()
        if(m.m_type == "S" or m.m_type == "R"):

        """print("operation : "+m.translation())
        mv = og.Missive()
        if(m.m_type == 'G'):
            n_bloc = None
            if(m.ident < depth):
                m = None
                continue
            generate_bloc += 1
            depth += 1
            n_bloc = bc.Bloc(name,depth)
            n_bloc.mhash = m.m_hash
            n_bloc.nonce = m.nonce
            n_bloc.listope = []
            c_ope = 0
            for ope in l_ope :
                c_ope += 1
                n_bloc.listope.append(ope)
            l_ope=[]
            n_bloc.nbope = c_ope
            n_lst = [n_bloc]
            n_lst.extend(blocChain)
            blocChain = list(n_lst)
            n_bloc = None
            diffusion(blocChain)
            pw = bp.HashFactory(stopPowBC,aggregation_bloc(blocChain)\
                           ,required,depth,name,queue)
            pw.start()
            string = ""
            for b in blocChain :
                string = string + b.translation()
            mv.obj_injection("R",string,name)
        else:
            l_ope.append(m)
            mv.obj_injection("S",m.translation(),name)
        print("missive :" + mv.translation())
        if(depth == 2):
            running = False
    bridge.t.close()"""
"""
def action(m):
    if(m.m_type == 'G'):
        n_bloc = None
        if(m.ident < depth):
            m = None
            continue
        generate_bloc += 1
        depth += 1
        n_bloc = bc.Bloc(name,depth)
        n_bloc.mhash = m.m_hash
        n_bloc.nonce = m.nonce
        n_bloc.listope = []
        c_ope = 0
        for ope in l_ope :
            c_ope += 1
            validation(ope)
            n_bloc.listope.append(ope)
        l_ope=[]
        n_bloc.nbope = c_ope
        n_lst = [n_bloc]
        n_lst.extend(blocChain)
        blocChain = list(n_lst)
        n_bloc = None
        diffusion(blocChain)
        pw = bp.HashFactory(stopPowBC,aggregation_bloc(blocChain)\
                           ,required,depth,name,queue)
        pw.start()
        string = ""
        for b in blocChain :
            string = string + b.translation()
        continue
    elif(m.m_type == 'T' or m.m_type == 'E' or \
         m.m_type == 'C' or m.m_type == 'D'):
        if(is_in(l_ope,m)):
            continue
        l_ope.append(m)
        diffusion(m)
        continue
    else :
        continue
"""
def aff_bc(bc):
    for b in bc:
        print(b)

#retransmet les messages arrivant au voisin /!\ doit connaitre la
#source pour ne pas lui retransmettre
#/!\ attention il faut egalement vérifier que le message n'existe pas
#deja dans la bloque chaine ou la liste courrante
#il ne fera aucun action sur le neoud local (il ne fera que regarder)
#à placer dans un thread indé pour ne pas bloquer le thread principal
#qui a deja assé à faire
def diffusion(m):
    return

def validation(o):
    return

def is_in(list_ope,ope):
    for ele in list_ope:
        if(ope == ele):
            return True
    return False

def aggregation_bloc(blocs):
    string = ""
    for b in blocs:
        string += str(b)
    return string

if __name__ == '__main__' :
    l = threading.Semaphore(3)
    l.acquire()
    l.acquire()
    l.acquire()
    t=threading.Thread(target=core_node,args=("0","localhost",18886 \
                                       ,[0,4,4] \
                                       ,[]\
                                       ,l))
    """tt=threading.Thread(target=core_node,args=("1","localhost",18887\
                                        ,[0,4,4]\
                                        ,[["0",18886],["2",18888]]\
                                        ,l))
    ttt=threading.Thread(target=core_node,args=("2","localhost",18888\
                                         ,[0,4,4]\
                                         ,[["1",18887],["0",18886]]\
                                         ,l))
    """
    t.start()
    #tt.start()
    #ttt.start()
    time.sleep(1)
    l.release()
    l.release()
    l.release()
