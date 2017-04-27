# -*- coding:utf-8 -*-
"""Operate Local SQL Server by sqlalchemy."""
import sqlalchemy as sa
import pyodbc
import os
import gab_models as gab
from datetime import datetime
from sqlalchemy.orm import sessionmaker
import random

class Creator:
    """ODBC creater."""

    def __init__(self, db_name='ASP20010'):
        """Initialization procedure to receive the database name."""
        self.db_name = db_name

    def __call__(self):
        """Custom creator to be passed to sqlalchemy.create_engine."""
        if os.name == 'posix':
            return pyodbc.connect('DRIVER={FreeTDS};'
                                  'Server=my.db.server;'
                                  'Database=%s;'
                                  'UID=myuser;'
                                  'PWD=mypassword;'
                                  'TDS_Version=8.0;'
                                  'Port=1433;' % self.db_name)
        elif os.name == 'nt':
            # use development environment
            return pyodbc.connect('DRIVER={SQL Server};'
                                  'Server=127.0.0.1;'
                                  'Database=%s;'
                                  'UID=sa;'
                                  'PWD=Zaq12wsxcde34rfv!;'
                                  'Trusted_Connection=Yes;'
                                  'Port=1433;' % self.db_name)


def en(db_name):
    """Return a sql_alchemy engine."""
    engine = sa.create_engine('mssql://', creator=Creator(db_name))
    return engine

engine = en('ASP20010')
connection = engine.connect()
# rows = connection.execute("select * from VUSERS;")
# for row in rows:
#     print(row)

def get_mobile_number():
    num1 = ['070', '080', '090', '010', '100']
    idx = random.randint(0, 4)
    return num1[idx] + '-' + '{0:0>4}'.format(random.randint(0, 9999)) +\
            '-' + '{0:0>4}'.format(random.randint(0, 9999))

def get_comp():
    l_comp = [['ASOL','JA-EZZY','ja',[],['AXT','Y01']], ['NIC','JA-ZA01','ja',['IB2','IC0'],['G1','TS']],\
                ['AK','GS-B104','ja',['G6'],['1','2']],['NNA','NA-NNA','en',[], ['M8A', 'NNA']],\
                ['VVV','GS-VVV','ja',[], ['001','002']],['MMM','JB-0000','us',[], ['1A1', '1A2']]]
    return l_comp[random.randint(0,5)]   


def get_name():
    l_name = [['もも','たろう','Momo','Taro'], ['千尋','れい','Tihiro','Rei'],\
                ['ととろ','たろう','Totoro','Taro'], ['Wang','Smith','Wang','Smith'],\
                ['スズキ','マコト','Suzuki','Makoto']]
    return l_name[random.randint(0,4)]    


def get_sn():
    l_sn = ['aichi','tokyo','yokohama','kobe','osaka',\
            'new york','bei jing','paris','dobie']
    return l_sn[random.randint(0,8)]


def get_phon_number():
    num1 = ['010', '03', '06', '044', '+81-021', '+86-028', '+01-032', '+01-011', '033']
    idx = random.randint(0, 8)
    return num1[idx] + '-' + '{0:0>4}'.format(random.randint(0, 9999)) +\
            '-' + '{0:0>4}'.format(random.randint(0, 9999))


def get_fun():
    fun = ['AFFL','ALLIANCE','AMG','AS','AS(GOM)','AS(J)','AUD Office', 'BRAND',\
            'CEO-COOOffi' ,'G&A BT(G)', 'G&A BT(J)', 'G&A BT(S)', 'R&D', 'IAM', \
            'FORK', 'FACILITY', 'M&A', 'HR']                         
    return fun[random.randint(0,17)]


def setperson(idx):
    person = gab.PERSON()
    comp = get_comp()
    number = idx[comp[0]]
    idx[comp[0]] = number + 1
    name = get_name()
    sn = get_sn()
    # No1
    person.uid = comp[0] + '{0:0>4}'.format(number)
    person.companyCode = comp[1]
    person.employeeNumber = '{0:0>4}'.format(number)
    person.locale = comp[2]
    person.sn = sn
    person.givenName = name[2]
    person.middleName = name[3]
    person.localSn = sn
    person.localGivenName = name[0]
    person.localMiddleName = name[1]
    # No10
    person.jpYomiSn = name[2]
    person.jpYomiGivenName = name[3]
    #person.managerUid = ''
    #person.net23MailAddress = ''
    person.mail = person.uid + '@' + comp[1] + '.com'
    person.localMailAddress = person.uid + '@' + comp[1] + '.com'
    person.mobile = get_mobile_number()
    #person.pager = ''
    person.telephoneNumber = get_phon_number()
    person.telephoneNumber2 = get_phon_number()
     # No20   
    person.telephoneNumber3 = get_phon_number()
    person.extensionNumber = get_phon_number()
    person.extensionNumber2 = get_phon_number()
    person.extensionNumber3 = get_phon_number()
    person.facsimileTelephoneNumber = get_phon_number()
    person.extensionFacsimileNumber = get_phon_number()
    person.employmentType = ['1','2','3','4'][random.randint(0,3)]
    #person.contractorCode = ''
    person.teamCode = ['T1','T2','T3','T4'][random.randint(0,3)]
    #person.description = ''
    # No30
    #person.localDescription = ''    
    if len(comp[3]) > 0:
        person.localOuCode = comp[3][random.randint(0,len(comp[3])-1)]
    #else:
    #    person.localOuCode = ''
    #person.ou = ''
    #person.localOu = ''
    #person.localTitleCode = ''
    #person.title = ''
    #person.localTitle = ''
    #person.rankCode = ''
    #person.titleLevel = ''   
    person.localOfficeCode = comp[4][random.randint(0,len(comp[4])-1)]
    # No40
    #person.expirationDate = 
    #person.expirationMailFlag = ''
    #person.idCardNumber = ''
    #person.globalBusinessCode = ''
    person.globalFunctionCode = get_fun()
    person.flagResource = '1'
    person.createDate = datetime.utcnow()
    person.updateDate = datetime.utcnow()
    #person.directoryReflectStartDate = ''
    # No50
    #person.directoryReflectEndDate = ''
    person.upperSn = person.sn.upper()
    person.upperGivenName = person.givenName.upper()
    person.upperMiddleName = person.middleName.upper()
    person.upperGlobalFunctionCode = person.globalFunctionCode.upper()
    #person.upperOu = ''
    #person.upperTitle = ''
    person.directoryCreateDate = datetime.utcnow()
    person.directoryUpdateDate = datetime.utcnow()
    return person

# session を作成する
# session は面倒なようで、用途によっては非常にありがたかったりする
Session = sessionmaker(bind=engine)
session = Session()
idx ={'ASOL':20, 'NIC':20, 'AK':20, 'NNA':20, 'VVV':20, 'MMM':20}
for i in range(10000):
    person = setperson(idx)
    session.add(person)
session.commit()
connection.close()
