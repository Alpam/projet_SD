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

if __name__ == '__main__' :
    print("::::test bloc chaine::::")
    bl   = bc.Bloc("N0","0","","0","")
    bll  = bc.Bloc("N0","1","hash","0","154")
    blll = bc.Bloc("N0","2","hash2","0","155554")
    print(bl)
    r=bl+(bll+blll)
    print(r)
    print("\n::::test p_node::::")
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
    m1 = og.m_builder(0,[1,0],'T',[2,1],14)
    m2 = og.m_builder(0,[1,1],'C')
    print(m1)
    print(m2)
    print(og.m_type(m1))
    print(og.m_type(m2))
    print(og.m_origin(m1))
    print(og.m_origin(m2))
    print(og.m_destination(m1))
    print(og.m_destination(m2))

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
