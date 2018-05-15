#
############################################################
#
#        Filename:monitor.py
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
from bloc_node import ope_generator as og
from bloc_node import bloc as bc
from threading import Thread
    
class Monitor(Thread):
    def __init__(self,queue,name):
        Thread.__init__(self)
        self.queue = queue
        self.name = name
        #running est une liste pour passer un boolean
        #pour stoper la boucle quand qu'on veut

    def run(self):
        f = open(self.name, 'a+')
        while(True):
            b = bc.Bloc("","")
            op = og.Operation()
            m = self.queue.get()
            if(type(m)==str):
                return
            if (m.m_type == 'S' or m.m_type == 'Q'):
                if (m.m_type == 'Q'):
                    f.write("unaccepted ")
                else:
                    f.write("accepted ")
                op.str_injection(m.str_obj)
                f.write("opération : \n")
                f.write(str(op))
                f.write("\n")
            elif (m.m_type == 'R' or m.m_type == 'P'):
                if (m.m_type == 'P'):
                    f.write("unaccepted ")
                else:
                    f.write("accepted ")
                f.write("bloc chain : \n")
                for blc in m.str_obj.split(' '):
                    b.str_injection(blc)
                    f.write(str(b))
                    f.write("\n")

