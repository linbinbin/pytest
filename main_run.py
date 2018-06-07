# -*- coding: utf-8 -*-
import logging
import logging.handlers
import subprocess
import platform
import time
import os
import shutil
import sys
import win32api
import win32con
import win32evtlog
import win32security
import win32evtlogutil
import glob

class EventLog:
    def __init__(self):
        '''
        - SID の生成
         - refer to http://www.atmarkit.co.jp/ait/articles/0306/28/news004.html
        '''
        self.ph  = win32api.GetCurrentProcess()
        self.th  = win32security.OpenProcessToken(self.ph, win32con.TOKEN_READ)
        self.sid = win32security.GetTokenInformation(self.th, win32security.TokenUser)[0]
  
        '''
        - イベントログの共通情報
         - appName = アプリケーション名を指定 
         - data = LogName を指定
        '''
        self.appName = "Springboard"
        self.data = "Application\Springboard_Log".encode("ascii")
         
    ''' 
    - EventLog.info
     - eventID = 任意のイベント ID を指定（0 ～ 65535 を指定可能）
     - type = win32evtlog の EVENTLOG_INFORMATION_TYPE を指定
    '''
    def info(self, message):
        eventID = 65500
        type = win32evtlog.EVENTLOG_INFORMATION_TYPE
        desc = [message]
        self.write_event_log(eventID, type, desc)
         
    ''' 
    - EventLog.warn
     - eventID = 任意のイベント ID を指定（0 ～ 65535 を指定可能）
     - type = win32evtlog の EVENTLOG_WARNING_TYPE を指定
    '''
    def warn(self, message):
        eventID = 65501
        type = win32evtlog.EVENTLOG_WARNING_TYPE
        desc = [message]
        self.write_event_log(eventID, type, desc)
 
    ''' 
    - EventLog.warn
     - eventID = 任意のイベント ID を指定（0 ～ 65535 を指定可能）
     - type = win32evtlog の EVENTLOG_ERROR_TYPE を指定
    '''
    def crit(self, message):
        eventID = 65502
        type = win32evtlog.EVENTLOG_ERROR_TYPE
        desc = [message]
        self.write_event_log(eventID, type, desc)
 
    ''' 
    - イベントログへの書き込み
     - win32evtlogutil の ReportEvent メソッドを利用
    '''
    def write_event_log(self, eventID, type, desc):
        win32evtlogutil.ReportEvent(
            self.appName,
            eventID,
        eventType=type,
            strings=desc,
            data=self.data,
            sid=self.sid
        )

def putlog(msgid, severity, locale, message):
    logger = logging.getLogger('springboard_batch')
    if severity == 'E':
        logger.error("{0} {1} {2} {3} {4} {5} {6} {7} {8}".format(msgid, severity, platform.uname()[0], os.getpid(), time.strftime("%x"), time.strftime("%X"), locale, platform.uname()[1], message))
    else:
        logger.warning("{0} {1} {2} {3} {4} {5} {6} {7} {8}".format(msgid, severity, platform.uname()[0], os.getpid(), time.strftime("%x"), time.strftime("%X"), locale, platform.uname()[1], message))

def load_properties(filepath, sep='=', comment_char='#'):
    """
    Read the file passed as parameter as a properties file.
    """
    props = {}
    with open(filepath, "rt") as f:
        for line in f:
            l = line.strip()
            if l and not l.startswith(comment_char):
                key_value = l.split(sep)
                key = key_value[0].strip()
                value = sep.join(key_value[1:]).strip().strip('"')
                props[key] = value
    return props

def int32(x):
    if x>0xFFFFFFFF:
      raise OverflowError
    if x>0x7FFFFFFF:
      x=int(0x100000000-x)
      if x<2147483648:
        return -x
      else:
        return -2147483648
    return x

def exec_process(commands):
    msg = ""
    process = subprocess.Popen(commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=-1)
    out, err = process.communicate()
    #print("process: {0}".format(int32(process.returncode)))
    # Wait process end and judg the result
    process.wait()
    msg = err.decode('utf-8').replace('\r', '').replace("\n", '')
    return (int32(process.returncode), msg)


if __name__ == '__main__':
    settings = load_properties('e:/springboard/conf/config.properties')
    # create logger with 'spam_application'
    logger = logging.getLogger('springboard_batch')
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    # 2018.02.16 change : FileHandler -> TimedRotatigFileHandler
    #fh = logging.FileHandler(settings['logfile'])
    fh = logging.handlers.TimedRotatingFileHandler(
        settings['logfile'], 
        when="D", 
        interval=1, 
        backupCount=int( settings['db.delete.days'] ) 
    )
    fh.setLevel(logging.ERROR)
    # create console handler with a higher log level
    #ch = logging.StreamHandler()
    #ch.setLevel(logging.DEBUG)

    # add the handlers to the logger
    logger.addHandler(fh)
    eventlog = EventLog()

    fd_date = time.strftime("%Y%m%d%H%M%S")
    msg = ""
    err_msg = ""
    ret = 0

    # wait for arrival 'ENTER.C00'
    totalWaitTime=0
    while os.path.exists(settings['ftp.recv.enterfileflag']) == False:
        time.sleep(int(settings['ftp.recv.chkinterval']))
        totalWaitTime += int(settings['ftp.recv.chkinterval'])
        if totalWaitTime >= int(settings['ftp.recv.chktimeout']):
            break
    if os.path.exists(settings['ftp.recv.enterfileflag']) == True:
        os.remove(settings['ftp.recv.enterfileflag'])
    putlog("SBSIB001", "I", 0, "Waited for arrival 'ENTER.C00' " + str(totalWaitTime) + " second(s).")

    #unzip the ENTER
    if os.path.exists(settings['ftp.recv.enterfile']):
        try:
            shutil.copyfile(settings['ftp.recv.enterfile'], os.path.join(settings['work.inputfile.path'], 'enter.d00'))
            shutil.move(settings['ftp.recv.enterfile'], os.path.join(settings['inputfile.backup.path'], 'enter.d00_' + fd_date))

            #delete overstorage of ENTER-TR backups
            backupFileList = sorted(glob.glob(settings['inputfile.backup.path'] + "enter.d00_*"), reverse=True)
            count = 0
            for file in backupFileList:
                count += 1
                if count > int(settings['db.delete.days'])*2:
                    os.remove(file)
            if count > int(settings['db.delete.days'])*2:
                putlog("SBSIB001", "I", 0, str(count-int(settings['db.delete.days'])*2) + " deleted overstorage of ENTER-TR backups")

            ret, msg = exec_process(r'"C:\Program Files\7-Zip\7z.exe" x ' + os.path.join(settings['work.inputfile.path'], 'enter.d00') + ' -o' + settings['work.inputfile.path'])
            os.remove(os.path.join(settings['work.inputfile.path'], 'enter.d00'))
            ret, msg = exec_process(r'"C:\Program Files\7-Zip\7z.exe" x ' + os.path.join(settings['work.inputfile.path'], 'enter') + ' -o' + os.path.join(settings['work.inputfile.path'],fd_date))
            if ret != 0:
                eventlog.crit("unzip error"+msg)
                putlog("SBSEB001", "E", ret, "unzip error"+msg)
                print("enter unizp error")
                sys.exit(1)
            os.remove(os.path.join(settings['work.inputfile.path'], 'enter'))
        except OSError as why:
            eventlog.crit("unzip error"+msg)
            putlog("SBSEB002", "E", ret, "enter error"+str(why))
            sys.exit(1)
        except Exception as err:
            eventlog.crit("unzip error"+msg)
            putlog("SBSEB002", "E", ret, "enter error"+str(err))
            sys.exit(2)
    else:
        putlog("SBSIB002", "I", 0, "No ENTER.D00 file")

    if os.path.exists(settings['ftp.recv.master']):
        try:
            shutil.copyfile(settings['ftp.recv.master'], os.path.join(settings['work.inputfile.path'], 'HANSYA_MASTER.csv'))
        except OSError as why:
            eventlog.crit("master error"+str(why))
            putlog("SBSEB003", "E", ret, "master error"+str(why))
            sys.exit(1)
        except Exception as err:
            eventlog.crit("master error"+str(err))
            putlog("SBSEB003", "E", ret, "master error"+str(err))
            sys.exit(2)
    else:
        putlog("SBSIB003", "I", 0, "No DEALER_MASER.csv file")

    has_error = ""
    for i in range(int(settings['max.retry'])):
        has_error = ""
        err_msg = ""
        #Insert TR to DB
        ret, msg = exec_process("java -jar e:/springboard/bin/XmlReader_2.jar")
        if ret != 0:
            if ret > 0:
               ret = 6
            has_error = "SBSEB10"+str(abs(ret))
            err_msg += msg
            print("enter file process error")
        else:
            print("get enter zip ok")
        #Get info from HANA
        ret, msg = exec_process("java -jar e:/springboard/bin/HANAInfoSearch_3.jar")
        if ret != 0:
            if ret > 0:
               ret = 3
            has_error = "SBSEB20"+str(abs(ret))
            err_msg += msg
            print("hanainfo error")
        else:
            print("hana ok")
        #Put Json to K5
        ret, msg = exec_process("java -jar e:/springboard/bin/K5Send_4.jar")
        if ret != 0:
            if ret > 0:
               ret = 4
            has_error = "SBSEB30"+str(abs(ret))
            err_msg += msg
            print("put error")
        else:
            print("put ok")
        if has_error == "":
            break
        time.sleep(3)
        i += 1
    if has_error != "":
        eventlog.crit(err_msg)
        putlog(has_error, "E", ret, err_msg)
        sys.exit(-1)
    else:
        putlog("SBSIB001", "I", str(ret), "Springboard Batch OK")
