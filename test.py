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
import sys

if __name__ == '__main__' :
    t=[True,True,True,True,True]
    if(len(sys.argv)>1):
        i = 1
        while(i<len(sys.argv)):
            if(sys.argv[i]=='n'):
                t[i-1]=False
            i += 1
    print(sys.argv)
    print(t)
    print("::::test bloc chaine::::")
    if(t[0]):
        bl   = bc.Bloc("N0","0","","0","")
        bll  = bc.Bloc("N0","1","hash","0","154")
        blll = bc.Bloc("N0","2","hash2","0","155554")
        print(bl)
        r=bl+(bll+blll)
        print(r)
    else:
        print("\tnot ask")
    print("\n::::test hash::::")
    if(t[1]):
        qh = Queue()
        sf = []
        hf = bp.HashFactory([False],str(bll),2,0,0,qh)
        hf.start()
        hf.join()
        rtr = qh.get()
        print(rtr)
        print(og.m_reader(rtr))
    else:
        print("\tnot ask")
    print("\n::::test p_node::::")
    if(t[2]):
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
    else:
        print("\tnot ask")
    print("\n::::test m_operation::::")
    if(t[3]):
        m1 = og.Operation('T',10,[0,1],[2,1],None,None,42)
        m2 = og.Operation('C',0,[1,0])
        m3 = og.Operation()
        m3.str_injection("G%24%0%hash%nonce%nonce%nonce")
        print(m1)
        print(m2)
        print(m3)
        print(m1.translation())
        print(m2.translation())
        print(m3.translation())
        m4 = og.Operation()
        m4.str_injection(m1.translation())
        print(m4)
        m4.str_injection(m2.translation())
        print(m4)
        m4.str_injection(m3.translation())
        print(m4)

    else:
        print("\tnot ask")
    print("\n::::test p_manager::::")
    if(t[4]):
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
            print(og.m_reader(i))
    else:
        print("\tnot ask")
