#
############################################################
#
#        Filename:bloc.py
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

class Bloc:

    def __init__(self, creator, depth, mhash="", nonce="", nbope=0):
        self.creator = creator
        self.depth = depth
        self.mhash = mhash
        self.nbope = nbope
        self.listope = list()
        self.nonce = nonce

    def __str__(self):
        string = "Creator : " + self.creator + '\n'                \
               + "Depth : " + str(self.depth) + '\n'               \
               + "Hash : " + self.mhash + '\n'                     \
               + "Nonce : "
        for x in self.nonce:
            string += str(ord(x)) +':'
        string += '\n'
        string += "Number of Operations : " + str(self.nbope) + '\n'
        for l in self.listope :
            string += str(l) + '\n'
        return string

    def str_injection(self, string):
        l = string.split('\n')
        self.creator = l[0]
        self.depth = int(l[1])
        self.nbope = int(l[2])
        self.mhash = l[3]
        self.nonce = l[4]
        if(len(l)==6):
            for ope in l[5].split(';'):
                o = og.Operation()
                o.str_injection(ope)
                self.listope.append(o)

    def translation(self):
        string = self.creator + '\n' + str(self.depth) + '\n' \
                 + str(self.nbope) + '\n' + self.mhash + '\n' \
                 + str(self.nonce) + '\n'
        for l in self.listope :
            string += l.translation() + ';'
        return string[:-1]

    def __add__(self, obj):
        return str(self)+':'+str(obj)


