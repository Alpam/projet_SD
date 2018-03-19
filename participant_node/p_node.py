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

import random
import time

def p_work():
    time_sleep = random.randint(1,75)
    value_transaction = random.randint(1,100)
    time.sleep(time_sleep/100.0)
    return value_transaction

def p_life():
    return random.randint(20,100)

if __name__ == '__main__' :
    life = p_life()
    print(life)
    while(life):
        life -= 1
        print(p_work())

