# -*- coding:utf-8 -*-
"""make data for insert."""
import codecs as dc

org_all = """""V_UID" CHAR(15) NOT NULL DEFAULT ' ', "V_SN" CHAR(40), "V_GIVENNAME" CHAR(40), "V_MIDDLENAME" CHAR(40), "V_UPPERSN" CHAR(40), "V_UPPERGIVENNAME" CHAR(40), "V_NET23MAILADDRESS" CHAR(100), "V_MAIL" CHAR(100), "V_TELEPHONENUMBER" CHAR(20), "V_EXTENSIONNUMBER" CHAR(20), "V_TITLELEVEL" CHAR(1), "V_COMPANYCODE" CHAR(10), "V_COMPANY" CHAR(100), "V_UPPERCOMPANY" CHAR(100), "V_CONNECTIVETYPE" CHAR(1), "V_GLOBALCOMPANYCODE" CHAR(12), "V_UPPERGLOBALCOMPANYCODE" CHAR(12), "V_LOCALOUCODE" CHAR(6), "V_OU" VARCHAR(255), "V_UPPEROU" VARCHAR(255), "V_LOCALDEPARTMENTCODE" CHAR(6), "V_GLOBALFUNCTIONCODE" CHAR(12), "V_UPPERGLOBALFUNCTIONCODE" CHAR(12), "V_TITLE" CHAR(80), "V_OFFICECODE" CHAR(4), "V_OFFICENAME" CHAR(100)"""
dis_all = """--------------- ---------------------------------------- ---------------------------------------- ---------------------------------------- ---------------------------------------- ---------------------------------------- ---------------------------------------------------------------------------------------------------- ---------------------------------------------------------------------------------------------------- -------------------- -------------------- ------------ ------------- ---------------------------------------------------------------------------------------------------- ---------------------------------------------------------------------------------------------------- ---------------- ------------------- ------------------------ ------------- --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- --------------------- -------------------- ------------------------- -------------------------------------------------------------------------------- ------------ ----------------------------------------------------------------------------------------------------"""

org_user = """""V_UID" CHAR(15) NOT NULL DEFAULT ' ', "V_LOCALSN" CHAR(40), "V_LOCALGIVENNAME" CHAR(40), "V_COMPANYCODE" CHAR(10), "V_LOCALCOMPANY" CHAR(100), "V_OFFICECODE" CHAR(4), "V_LOCALOFFICENAME" CHAR(100)"""
dis_user = """--------------- ---------------------------------------- ---------------------------------------- ------------- ---------------------------------------------------------------------------------------------------- ------------ ----------------------------------------------------------------------------------------------------"""

org_role = """"v_Roleid" CHAR(6) NOT NULL DEFAULT ' ', "v_MemberUserid" CHAR(15)"""
dis_role = """-------- ---------------"""


def getsize(instr):
    for word in instr.strip().split(" "):
        x = word.strip()
        if x.find("CHAR(") >= 0:
            return int(x[x.find("CHAR(") + 5:-1])
    return 0


def mkzip(org, disp):
    llen = [len(x) for x in disp.split(" ")]
    ltype = list(map(lambda x: 0 if x.find('TIMESTAMP') < 0 else 1, org.split(",")))
    ldlen = list(map(getsize, org.split(",")))
    #print(sum(ldlen))
    return zip(max(llen, ldlen), zip(ldlen, ltype))


def mkvalue(zips, value):
    out = "("
    offset = 0
    for item in zips:
        org_value = value[offset:offset + item[0]]
        #print(org_value.replace(" ", "#"), offset, item[0])
        offset += item[0] + 1
        if org_value.strip() == "NULL":
            out += "null,"
        else:
            if item[1][1] == 1:
                out += "TIMESTAMP('{}'),".format(org_value.strip())
            else:
            	#out += "'{}',".format(org_value.replace("'", "''").strip())
                out += "'{}',".format(org_value.replace("'", "''")[:item[1][0]])
    print(out[:-1] + ")")

#all_zip = mkzip(org_all, dis_all)
#user_zip = mkzip(org_user, dis_user)
#role_zip = mkzip(org_role, dis_role)


with dc.open("../pr_role.rpt", 'r', 'utf-8') as frole:
    print("Table:VROLEUSER")
    print("Header: ")
    for role in frole.readlines():
        mkvalue(mkzip(org_role, dis_role), role.rstrip('\r\n'))

with dc.open("../pr_alluser.rpt", 'r', 'utf-8') as fall:
    print("Table:VALLUSERS2U")
    print("Header: ")
    for vall in fall.readlines():
        mkvalue(mkzip(org_all, dis_all), vall.rstrip('\r\n'))

with dc.open("../pr_user.rpt", 'r', 'utf-8') as fuser:
    print("Table:VUSERS")
    print("Header: ")
    for vuser in fuser.readlines():
        mkvalue(mkzip(org_user, dis_user), vuser.rstrip('\r\n'))
