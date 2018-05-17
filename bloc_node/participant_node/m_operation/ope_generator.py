#
############################################################
#
#        Filename:ope_generator.py
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
"""
    classe Missive : 4 types
    S et R : opération à valider (dans core_node) ou valide (dans monitor)
    Q et P : opérations invalides
    S et Q : continenent des opérations
    R et P : continenent des bloc chaines
    m_type : le Type
    str_obj : objet reduit sous forme de string
        une bloc chaine est representée comme suit : 
            chaque bloc est séparé par des espaces
            chaque champ d'un bloc par des '\n'
            chaque opération d'un bloc par des ';'
            chaque champ d'un opération par des ':'
    transmitter : dernier node à avoir transmis la missive
"""
class Missive:
    def __init__(self):
        self.m_type = ""
        self.str_obj = ""
        self.transmitter = ""

    def __str__(self):
        rtr = "Type : "+self.m_type+" L_hop : "+self.transmitter\
             +" Str_OBJ: " +self.str_obj
        return rtr

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

    def copy(self):
        cp = Missive()
        cp.m_type = self.m_type
        cp.str_obj = self.str_obj
        cp.transmitter = self.transmitter
        return cp
"""
    classe representan une opération : 5 types
    T : une transaction
    G : nouveau bloc
    C : une connection
    D : une deconnection
    E : une erreur provoquant la déconnection
    m_type : le Type
    ident : numéro du message du participant (si m_type == G alors ident peut soit etre la depth ou le node l'ayant généré)
    origin : identifiant du participant et du node (si G uniquement l'id du node)
    Destination : uniquement si transaction identifiant du participant et du node cible
    m_hashsh : remplit si G
    nonce : remplit si G
    value : valeur de la transaction (si E nombre de testes avant arrêt)
"""
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
        l = string.split(":")
        self.m_type = l[0]
        self.ident  = int(l[1])
        if(string[0]=='T'):
            self.origin = []
            self.origin.append(int(l[2]))
            self.origin.append(int(l[3]))
            self.dstntn = []
            self.dstntn.append(int(l[4]))
            self.dstntn.append(int(l[5]))
            self.value = round(float(l[6]),3)
        elif(string[0]=='G'):
            self.origin = int(l[2])
            self.m_hash = l[3]
            self.nonce  = l[4]
        elif(string[0]=='D' or string[0]=='C' or string[0]=='E'):
            self.origin = []
            self.origin.append(int(l[2]))
            self.origin.append(int(l[3]))

            if(string[0]=='E'):
                self.value = int(l[6])
        return

    def __str__(self):
        rtr = ""
        rtr += "Type :" + self.m_type + " Id :" + str(self.ident)
        if(self.m_type == 'T'):
            rtr += " Origine :" + str(self.origin[0]) + "-" + str(self.origin[1]) +     \
                   " Destination :" + str(self.dstntn[0]) + "-" + str(self.dstntn[1]) + \
                   " Valeur :"+ str(round(self.value,3))
        elif(self.m_type == 'G'):
            rtr += " Origine :" + str(self.origin) + "\nHash :" \
                   + self.m_hash + "\nNonce:"
            for x in self.nonce:
                rtr += str(ord(x)) +':'
            rtr += '\n'
        elif(self.m_type == 'C' or self.m_type == 'D' or self.m_type == 'E'):
            rtr += " Origine :" + str(self.origin[0]) + "-" + str(self.origin[1])
            if(self.m_type == 'E'):
                rtr += " Nombres de test avant arrêt :" + str(self.value)
        return rtr

    def translation(self):
        rtr = ""
        rtr += self.m_type + ':' + str(self.ident) + ':'
        if(self.m_type == 'T'):
            rtr += str(self.origin[0]) + ':' + str(self.origin[1]) + ':' + \
                    str(self.dstntn[0]) + ':' + str(self.dstntn[1]) + ':' + str(round(self.value,3))
        elif(self.m_type == 'G'):
            rtr += str(self.origin) + ':' + self.m_hash + ':' + self.nonce
        elif(self.m_type == 'C' or self.m_type == 'D' or self.m_type == 'E'):
            rtr += str(self.origin[0]) + ':' + str(self.origin[1])
            if(self.m_type == 'E'):
                rtr += ':' + str(self.value)
        return rtr

    def __eq__(self, obj):
        if(type(obj) == type(self)):
            if (self.m_type == obj.m_type):
                if(self.m_type == 'G'):
                    if(self.origin == obj.origin):
                        return True
                else:
                    if(self.origin[0] == obj.origin[0] and\
                       self.origin[1] == obj.origin[1] and\
                       self.ident == obj.ident):
                        return True
        return False

