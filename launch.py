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

import csv
import os
import sys

if(len(sys.argv)<2):
    print("donner fichier en arg")
    quit()
with open(sys.argv[1],'r') as csvfile :
    s = []
    i = 0
    r = csv.reader(csvfile, delimiter=' ',quotechar='\n',quoting=csv.QUOTE_MINIMAL)
    #une ligne : nbr participant simultané, nbr total de participant, nbr de transaction par particpant, nom voisin, .....
    l_arg = []
    for l in r:
        if(l == []):
            continue
        n_arg = ""
        n_arg += str(i)+' '\
                +"localhost"+' '\
                +str(i+17880)+' '\
                +l[0]+' '\
                +l[1]+' '\
                +l[2]
        j=3
        while(j<len(l)):
            if(i==int(l[j])):
                print("erreur voisinage pour "+str(i))
                quit()
            n_arg +=' '+ l[j]+' '+ str(17880 + int(l[j]))
            j+=1
        l_arg.append(n_arg)
        i+=1
    pid=[]
    for l in l_arg :
        pmn = "python3 master_node.py "
        pmn += l
        print(pmn)
        i = os.fork()
        pid.append(i)
        if(not(i)):
            os.system(pmn)
            quit()
    if(not(i)):
        for p in pid:
            os.waitpid(p)
    

