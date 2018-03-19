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


def proof_of_work(string,required):
    work = True
    while(work):
        nonce = ""
        i=32
        while(i):
            i -= 1
            c = random.randint(0,255)
            nonce = nonce+chr(c)
        h = generate_hash(string+nonce)
        work = wrong_hash(h,required)
    return h

def generate_hash(string):
    h = hashlib.sha512(bytes(string))
    return h.hexdigest()

def wrong_hash(string,required):
    nb_zero = 0
    for c in string:
        if c =='0':
            nb_zero += 1
            if nb_zero == required :
                return False
        else :
            nb_zero = 0
    return True

if __name__ == '__main__' :
    str = "N100"
    print("result ::"+proof_of_work(str,6))
