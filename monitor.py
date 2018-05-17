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

"""
    La classe Monitor sert à la création des logs
    Elle réceptionne des Missives et les inscrits
    Est lancé depuis core_node, stoper à la réception
    de "end"
"""

class Monitor(Thread):
    def __init__(self,queue,name):
        Thread.__init__(self)
        #Queue sur la quelle core_node transmet les missives
        self.queue = queue
        #Nom du node parent
        self.name = name

    def run(self):
        f = open(self.name, 'w')
        f.close()
        f = open(self.name, 'a+')
        while(True):
            op = og.Operation()
            m = self.queue.get()
            if(type(m)==str):
                if(m=="end"):
                    return
                else:
                    f.write(m)
            elif(m.m_type == 'S' or m.m_type == 'Q'):
                if (m.m_type == 'Q'):
                    f.write("REFUSED from " + m.transmitter)
                else:
                    f.write("ACCEPTED from " + m.transmitter)
                op.str_injection(m.str_obj)
                f.write("\nOperation : ")
                f.write(str(op))
            elif (m.m_type == 'R' or m.m_type == 'P'):
                if (m.m_type == 'P'):
                    f.write("REFUSED from " + m.transmitter)
                else:
                    f.write("ACCEPTED from " + m.transmitter)
                f.write("\nBloc Chain :\n")
                for blc in m.str_obj.split(' '):
                    b = bc.Bloc("","")
                    b.str_injection(blc)
                    f.write(str(b))
                    f.write("--------------------------\n")
            f.write("\n@@@@@@@@@@@@@@@@@@@@@@\n")
        f.close()

if __name__ == '__main__':
    class Foo:
        def __init__(self):
            self.m_type = 'S'
            self.transmitter = 'b'
            self.str_obj = "C:0:0:0"
    q = Queue()
    m = Monitor(q,"golum")
    f = Foo()
    m.start()
    q.put(f)
    q.put(f)
    q.put("fin")
    m.join()
