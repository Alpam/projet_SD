#
############################################################
#
#        Filename:b_pow.py
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

from .participant_node import ope_generator as og
import random
import hashlib
from threading import Thread

class HashFactory(Thread):

    def __init__(self,string,required,depth,host,queue):
        Thread.__init__(self)
        #stop_flag ne doit pas être un type natif mais un objet
        self.string = string
        self.required = required
        self.q = queue
        self.hst = host
        self.d = depth
        self.stop = False

    def run(self):
        work = True
        while(work):
            if(self.stop):
                break
            nonce = ""
            i=32
            while(i):
                if(self.stop):
                    return
                i -= 1
                c = random.randint(0,255)
                if(chr(c) == '\n' or chr(c) == '\0' or \
                   chr(c) == ':'  or chr(c) == ';' or chr(c) == ' '):
                    i+=1
                    continue
                nonce = nonce+chr(c)
            h = self.generate_hash(self.string+nonce)
            work = self.wrong_hash(h,self.required)
        m = og.Operation('G',self.d,self.hst,None,h,nonce)
        if(self.stop):
            return
        self.q.put(m)
        return

    def exit(self):
        self.stop = True
    #genere un hash à partir d'une string, retourne une string
    def generate_hash(self,string):
        string = string.encode('utf-8')
        h = hashlib.sha512(bytes(string))
        return h.hexdigest()

    #regard si il y a une suite de 0 de la taille 'required' dans 'string'
    def wrong_hash(self,string,required):
        nb_zero = 0
        for c in string:
            if c =='0':
                nb_zero += 1
                if nb_zero == required :
                    return False
            else :
                nb_zero = 0
        return True

