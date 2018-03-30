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

if __name__ == '__main__' :
    print("::::test p_node::::")
    life = pn.p_random(1)
    print(life)
    while(life):
        life -= 1
        pn.p_slp([0.01,0.075])
        print(pn.p_random([1,100]))
    d = [0,0]
    b = [0,0]
    c = [1,2]
    print(pn.cmp_dstnt(d,b))
    print(pn.cmp_dstnt(b,c))
    print(pn.p_dstnt([b,c,[4,5],[5,6]],[5,6]))
    print(pn.p_dstnt([b],b))

    print("\n::::test m_operation::::")
    print(og.m_builder(0,[1,1],'C'))
    print(og.m_builder(0,[1,0],'T',[2,1],14))

    print("\n::::test p_manager::::")
    queue = Queue()
    l_ope = []
    destination = []
    m = pm.Manager(queue, destination, 0, 4, 4)
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
