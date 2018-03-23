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

from bloc_node import bloc_chain as bc, b_pow as bp
from participant_node import p_node as pn

if __name__ == '__main__' :
    string = "N100"
    print("result ::"+bp.proof_of_work(string,6))
