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
    return message


if __name__ == '__main__' :
    print(m_builder(0,[1,1],'C'))
    print(m_builder(0,[1,0],'T',[2,1],14))

