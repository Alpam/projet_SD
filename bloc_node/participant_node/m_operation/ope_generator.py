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

class Missive:

    def __init__(self):
        self.m_type = ""
        self.str_obj = ""
        self.transmitter = ""

    def str_injection(self,string):
        self.m_type = string[0]
        i=2
        while(i < len(string) and string[i]!=' '):
            self.transmitter += string[i]
            i+=1
        i+=1
        while(i < len(string)):
            self.str_obj += string[i]
            i+=1
    
    def obj_injection(self,m_type,string,transmitter):
        self.m_type = m_type
        self.str_obj = string
        self.transmitter = transmitter

    def translation(self):
        string = self.m_type + ' '      \
               + self.transmitter + ' ' \
               + self.str_obj
        return string

class Operation:
#il faudrait rajouter des exceptions pour gérer les strings/args invalides
    def __init__(self,mt=None,i=None,org=None,dst=None,mh="", \
                nc="",vl=None):

            self.m_type = mt
            self.ident  = i
            self.origin = org
            self.dstntn = dst
            self.m_hash = mh
            self.nonce  = nc
            self.value  = vl

    def str_injection(self, string):
        self.m_type = None
        self.origin = None
        self.dstntn = None
        self.m_hash = None
        self.nonce  = None
        self.value  = None
        self.ident  = None
        self.transmitter = None
        foo = []
        tmp = ""
        for c in string :
            if(c!=' '):
                tmp += c
            else:
                foo.append(tmp)
                tmp = ""
        foo.append(tmp)
        self.m_type = foo[0]
        self.ident  = int(foo[1])
        if(self.m_type == 'T'):
            self.origin = [int(foo[2]),int(foo[3])]
            self.dstntn = [int(foo[4]),int(foo[5])]
            self.value  = int(foo[6])
        elif(self.m_type == 'G'):
            self.origin = int(foo[2])
            self.m_hash = foo[3]
            self.nonce  = foo[4]
            i = 5
            while(i<len(foo)):
                self.nonce += ' ' + foo[i]
                i += 1
        elif(self.m_type == 'C' or self.m_type == 'D' or self.m_type == 'E'):
            self.origin = [int(foo[2]),int(foo[3])]
            if(self.m_type == 'E'):
                self.value = [int(foo[4])]
        return

    def __str__(self):
        rtr = ""
        rtr += "Type :" + self.m_type + " Id :" + str(self.ident)
        if(self.m_type == 'T'):
            rtr += " Origine :" + str(self.origin[0]) + "-" + str(self.origin[1]) +     \
                   " Destination :" + str(self.dstntn[0]) + "-" + str(self.dstntn[1]) + \
                   " Valeur :"+ str(self.value)
        elif(self.m_type == 'G'):
            rtr += " Origine :" + str(self.origin) + "\nHash :" + self.m_hash + "\nNonce:" + self.nonce
        elif(self.m_type == 'C' or self.m_type == 'D' or self.m_type == 'E'):
            rtr += " Origine :" + str(self.origin[0]) + "-" + str(self.origin[1])
            if(self.m_type == 'E'):
                rtr += " Nombres de test avant arrêt :" + str(self.value)
        return rtr

    def translation(self):
        rtr = ""
        rtr += self.m_type + ' ' + str(self.ident) + ' '
        if(self.m_type == 'T'):
            rtr += str(self.origin[0]) + ' ' + str(self.origin[1]) + ' ' + \
                   str(self.dstntn[0]) + ' ' + str(self.dstntn[1]) + ' ' + str(self.value)
        elif(self.m_type == 'G'):
            rtr += str(self.origin) + ' ' + self.m_hash + ' ' + self.nonce
        elif(self.m_type == 'C' or self.m_type == 'D' or self.m_type == 'E'):
            rtr += str(self.origin[0]) + ' ' + str(self.origin[1])
            if(self.m_type == 'E'):
                rtr += ' ' + str(self.value)
        return rtr

    def __eq__(self, obj):
        if(type(obj) == type(self)):
            if (self.m_type == obj.m_type and \
                self.ident  == obj.ident):
                if(self.m_type == 'G' and \
                   self.origin == obj.origin):
                    return True
                elif(self.origin[0] == obj.origin[0] and\
                     self.origin[1] == obj.origin[1]):
                    return True
        return False

