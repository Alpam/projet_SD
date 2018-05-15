#
############################################################
#
#        Filename:p_node.py
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

#simule un participant : dort x seconde (meilleur simulation ever)
#precision maximale est de l'ordre de la miliseconde
def p_slp(slp):
    if(type(slp)==list):
        time_sleep = random.uniform(slp[0],slp[1])
        time.sleep(time_sleep)
    else :
        time.sleep(slp)

#simule renvoit un nombre aleatorie entre les bornes données dans vl
#si vl n'est pas une liste, renvoie vl
def p_random(vl):
    if(type(vl)==list):
        vl = random.randint(vl[0],vl[1])
    return vl


