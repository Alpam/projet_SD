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

def m_builder(nb_op,exp,tra,dest=None,value=None):
    message = str(nb_op) + "P" + str(exp[0]) + "B" + str(exp[1]) + tra
    if(tra == 'T'):
        message = message + "P" + str(dest[0]) + "B" + str(dest[1]) \
                + ":" + str(value)
    if(tra == 'E'):
        message = message + str(value)
    return message


