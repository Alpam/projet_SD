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

class BlocChain:

    def __init__(self, creator, depth, mhash, nbope, listope):

        self.creator = creator
        self.depth = depth
        self.mhash = mhash
        self.nbope = nbope
        self.listope = listope
        self.nonce = ""

    def bc_to_str(self):
        return self.creator + self.depth + self.mhash + \
               self.nbope + self.listope + self.nonce

if __name__ == '__main__' :
    bc = BlocChain("N0","0","","0","")
    print(bc.bc_to_str())
