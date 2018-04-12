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
from participant_node import p_manager as pm
from participant_node import p_node as pn
from participant_node import ope_generator as og
from bloc_node import bloc as bc
from bloc_node import b_pow as bp

def main():
    stopPowBC = [False]
    rtrPoW = []
    blocChain = []
    required = 6
    name = "N0"
    blocChain.append(name,"0","","0","")
    queue = Queue()
    l_ope = []
    destination = []
    running = True
    m = pm.Manager(queue, destination, 0, 4, 4)
    pw = bp.HashFactory(stopPowBC,str(blocChain[0]),required,rtrPoW,queue)
    m.start()
    pw.start()
    while(running):
        in_coming = queue.get()
        ic_t = m_type(in_coming)
        if(ic_t == 'G'):
        else if(ic_t == 'T'):
        else if(ic_t == 'E'):
        else if(ic_t == 'C'):
        else if(ic_t == 'D'):
        else :
            continue
    
    



if __name__ == '__main__' :
    return
