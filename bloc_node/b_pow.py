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

import random
import hashlib
from threading import Thread

class HashFactory(Thread):

    def __init__(self,stop_flag,string,required,retour,queue):
        Thread.__init__(self)
        #stop_flag ne doit pas être un type natif mais un objet
        self.sf = stop_flag
        self.string = string
        self.required = required
        self.retour = retour
        self.q = queue

    def run(self):
        work = True
        while(work):
            if(self.sf[0]):
                return False
            nonce = ""
            i=32
            while(i):
                i -= 1
                c = random.randint(0,255)
                nonce = nonce+chr(c)
            h = generate_hash(self.string+nonce)
            work = wrong_hash(h,self.required)
        if(self.sf[0]):
            return False
        self.retour[0] = h
        self.retour[1] = nonce
        self.q.put('%G')
        return True

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

