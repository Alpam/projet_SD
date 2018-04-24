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

from .participant_node import ope_generator 

class Bloc:

    def __init__(self, creator, depth, mhash="", nonce="", nbope=0, listope=list()):

        self.creator = creator
        self.depth = depth
        self.mhash = mhash
        self.nbope = nbope
        self.listope = listope
        self.nonce = nonce

    def __str__(self):
        string = "Creator : " + self.creator + '\n'                \
               + "Depth : " + str(self.depth) + '\n'               \
               + "Hash : " + self.mhash + '\n'                     \
               + "Nonce : " + str(self.nonce) + '\n'               \
               + "Number of Operations : " + str(self.nbope) + '\n'
        for l in self.listope :
            string += str(l) + '\n'
        return string

    def __add__(self, obj):
        return str(self)+':'+str(obj)


