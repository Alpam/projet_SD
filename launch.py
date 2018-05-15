#
############################################################
#
#        Filename: launch.py
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

import os

# nom serveur, ip, port, nbr participant simultané, nbr total de participant, nbr de transaction par particpant, nom voisin, port voisin, nom voisin, port voisin
i = os.fork()
if(not(i)):
    os.system("python3 master_node.py 0 localhost 18886 2 4 2 1 18887 2 18888")
else:
    j = os.fork()
    if(not(j)):
        os.system("python3 master_node.py 1 localhost 18887 2 4 2 2 18888 0 18886")
    else:
        os.system("python3 master_node.py 2 localhost 18888 2 4 2 1 18887 0 18886")


