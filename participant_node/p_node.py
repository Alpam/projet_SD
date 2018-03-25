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
import time

#choisit une destination aleatoire qui n'est pas mon adresse
#si une destination est possible renvoie une destination
#sinon renvoie False
def p_dstnt(dstnt,my_ad):
    if(len(dstnt)==1):
        return False
    target = random.randint(0,len(dstnt)-1)
    if(cmp_dstnt(dstnt[target],my_ad)):
        return dstnt[target-1]
    return dstnt[target]

#compare 2 destinations renvoie True si identique, False sinon
def cmp_dstnt(a,b):
    if(a[0]==b[0] and a[1]==b[1]):
        return True
    return False

#simule un participant : dort x miliseconde (meilleur simulation ever)
def p_slp(slp):
    time_sleep = random.randint(slp[0],slp[1])
    time.sleep(time_sleep/100.0)

#simule décision d'un participant
def p_trans(vl):
    value_transaction = random.randint(vl[0],vl[1])
    return value_transaction

#détermine aléatoirement la vie d'un participant (nombre de 
#transactions au totale)
def p_life(x,y):
    return random.randint(x,y)

if __name__ == '__main__' :
    life = p_life(1,1)
    print(life)
    while(life):
        life -= 1
        p_slp([1,75])
        print(p_trans([1,100]))
    d = [0,0]
    b = [0,0]
    c = [1,2]
    print(cmp_dstnt(d,b))
    print(cmp_dstnt(b,c))
    print(p_dstnt([b,c,[4,5],[5,6]],[5,6]))
    print(p_dstnt([b],b))
