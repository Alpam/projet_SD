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

class Bloc:

    def __init__(self, creator, depth, mhash, nbope, listope):

        self.creator = creator
        self.depth = depth
        self.mhash = mhash
        self.nbope = nbope
        self.listope = listope
        self.nonce = ""

    def __str__(self):
        return self.creator + self.depth + self.mhash + \
               self.nbope + self.listope + self.nonce

    def __add__(self, obj):
        return str(self)+':'+str(obj)


