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
    message = str(nb_op) + "OP" + str(exp[0]) + "OB" + str(exp[1])+ "%" + tra
    if(tra == 'T'):
        message = message + "DP" + str(dest[0]) + "DB" + str(dest[1]) \
                + "%" + str(value)
    if(tra == 'E'):
        message = message + str(value)
    if(tra == 'G'):
        message = message + str(dest) + '%' + str(value)
    return message

def m_reader(string):
    pos_eo = string.find("%")
    if(pos_eo == -1):
        return None
    pos_op = string.find("OP")
    if(pos_op == -1):
        return None
    pos_ob = string.find("OB")
    if(pos_ob == -1):
        return None
    mes_t = string[pos_eo+1]
    num_o = string[:pos_op]
    org_p = string[pos_op+2:pos_ob]
    org_b = string[pos_ob+2:pos_eo]
    dst_p = None
    dst_b = None
    val   = None
    if(mes_t == "T"):
        pos_dp = string.find("DP")
        if(pos_dp == -1):
            return None
        pos_db = string.find("DB")
        if(pos_db == -1):
            return None
        pos_ed = string.rfind("%")
        if(pos_ed == -1):
            return None
        dst_p = string[pos_dp+2:pos_db]
        dst_b = string[pos_db+2:pos_ed]
        val   = string[pos_ed+1:]
    elif(mes_t == 'C' or mes_t == 'D' or mes_t == 'E'):
        if(mes_t == 'E'):
            dst_p = string[pos_eo+2:]
    elif(mes_t == 'G'):
        pos_ed = string.rfind("%")
        if(pos_ed == -1):
            return None
        dst_p = string[pos_eo+2:pos_ed]
        dst_b = string[pos_ed+1:]
    else :
        return None
    return mes_t,num_o,org_p,org_b,dst_p,dst_b,val

def m_type(string):
    i = string.find('%')
    return string[i+1]

def m_origin(string):
    pos_op = string.find("OP")
    if(pos_op == -1):
        return None
    pos_ob = string.find("OB")
    if(pos_ob == -1):
        return None
    pos_eo = string.find("%")
    if(pos_eo == -1):
        return None
    op = string[pos_op+2:pos_ob]
    ob = string[pos_ob+2:pos_eo]
    if(op.isdigit()):
        return int(op),int(ob)
    else:
        return int(ob)

def m_destination(string):
    if(m_type(string)!='T'):
        return None
    pos_dp = string.find("DP")
    if(pos_dp == -1):
        return None
    pos_db = string.find("DB")
    print(pos_db)
    if(pos_db == -1):
        return None
    pos_eo = string.rfind("%")
    print(pos_eo)
    if(pos_eo == -1):
        return None
    dp = string[pos_dp+2:pos_db]
    db = string[pos_db+2:pos_eo]
    print(string)
    print(dp)
    print(db)
    if(dp.isdigit()):
        return int(dp),int(db)
    else:
        return int(db)
