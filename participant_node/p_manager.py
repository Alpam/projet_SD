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

from threading import Thread, Semaphore
from . import p_node as pn
from .m_operation import ope_generator as mg


class Participant(Thread):
    def __init__(self, queue, dest, host, mtrcl, sem, l_prt, lf, mm_tr, mm_slp, test):
        Thread.__init__(self)
        self.q = queue
        self.dest = dest
        self.address= [mtrcl,host]
        self.sem = sem
        self.l_prt = l_prt
        self.lf = lf
        self.mm_tr = mm_tr
        self.mm_slp = mm_slp
        self.test = test[0]
        self.t_slp = test[1]

    def run(self):
        counter = 0
        self.dest.append(self.address)
        message = mg.m_builder(counter,self.address,'C')
        self.q.put(message)
        life = pn.p_random(self.lf)
        ctest = self.test
        while(life):
            counter += 1
            life -= 1
            v = pn.p_random(self.mm_tr)
            pn.p_slp(self.mm_slp)
            dstnt = pn.p_dstnt(self.dest,self.address)
            #bout de code pour verifier qu'il y ai bien une destination
            #si il n'y en a pas att un petit temps, et reessaye
            #au bout d'un certain nombre d'essai non concluant successif
            #le participant s'arretera
            #pour le faire attendre indéfiniment initialiser test[0] sur -1
            if(not(dstnt)):
                if(not(ctest)):
                    message = mg.m_builder(counter,self.address,'E',None,self.test)
                    self.q.put(message)
                    break
                else :
                    ctest -= 1
                    pn.p_slp(self.t_slp)
                    counter -= 1
                    life += 1
                    continue
            ctest = self.test
            message = mg.m_builder(counter,self.address,'T',dstnt,v)
            self.q.put(message)
        counter += 1
        message = mg.m_builder(counter,self.address,'D')
        self.q.put(message)
        self.dest.remove(self.address)
        self.l_prt.remove(self)
        self.sem.release()
        return

class Manager(Thread):
    #nb : float('inf') represente l'infinit, marche aussi pour des comparaisons d'int
    def __init__(self, queue, dest, host, max_p = 50, tot_p = float('inf'), \
                 lf = 3, mm_tr = [1,100], mm_slp = 0.05, test = [2,0.025]):
        Thread.__init__(self)
        self.q = queue
        self.dest = dest
        self.h = host
        self.tot_p = tot_p
        self.lf = lf
        self.mm_tr = mm_tr
        self.mm_slp = mm_slp
        self.sem = Semaphore(max_p)
        self.t = test
        #use semaphore to stop the manager thread to create more 
        #participants than expect

    def run(self):
        nb_prtcpt = 0
        cur_prts = []
        while(nb_prtcpt < self.tot_p):
            self.sem.acquire()
            cur_prts.append(Participant(self.q,     \
                                        self.dest,  \
                                        self.h,     \
                                        nb_prtcpt,  \
                                        self.sem,   \
                                        cur_prts,   \
                                        self.lf,    \
                                        self.mm_tr, \
                                        self.mm_slp,\
                                        self.t))
            cur_prts[-1].start()
            nb_prtcpt += 1
        return


