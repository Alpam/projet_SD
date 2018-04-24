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
from bloc_node import p_manager as pm
from bloc_node import p_node as pn
from bloc_node import ope_generator as og
from bloc_node import bloc as bc
from bloc_node import b_pow as bp

def main():
    stopPowBC = [False]
    generate_bloc = 0
    depth = 0
    rtrPoW = []
    blocChain = []
    required = 6
    name = "0"
    blocChain.append(bc.Bloc(name,0))
    queue = Queue()
    l_ope = []
    destination = []
    running = True
    m = pm.Manager(queue, destination, 0, 4, 4)
    pw = bp.HashFactory(stopPowBC,aggregation_bloc(blocChain) \
                       ,required,depth,name,queue)
    m.start()
    pw.start()
    aff_bc(blocChain)
    while(running):
        m = queue.get()
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
            blocChain.append(n_bloc)
            n_bloc = None
            transmission(blocChain)
            pw = bp.HashFactory(stopPowBC,aggregation_bloc(blocChain)\
                               ,required,depth,name,queue)
            pw.start()
            aff_bc(blocChain)
            continue
        elif(m.m_type == 'T' or m.m_type == 'E' or \
             m.m_type == 'C' or m.m_type == 'D'):
            if(is_in(l_ope,m)):
                continue
            l_ope.append(m)
            transmission(m)
            continue
        else :
            continue
    
    

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
def transmission(m):
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
    main()
