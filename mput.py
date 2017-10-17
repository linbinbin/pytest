
# coding: utf-8

#!/usr/bin/python
import subprocess
import base64
import sys
import os
import datetime
import json
import hmac
import hashlib
import requests
from requests.auth import HTTPProxyAuth
from requests.exceptions import ProxyError
import time
from datetime import datetime
from optparse import OptionParser
from logging import getLogger,StreamHandler,FileHandler,DEBUG,ERROR
from selenium import webdriver
logger = getLogger(__name__)

fir=webdriver.Firefox()
fir.get("https://www.google.com")
fir.quit()

proxies_s = {
"http":'http://"FJT02198":"!QAZ5tgb"@10.16.1.103:8080',
"https":'http://"FJT02198":"!QAZ5tgb"@10.16.1.103:8080',
}

proxies = {
"http":"http://proxypac.jp.nissan.biz/proxy/proxy.pac",
"https":"http://proxypac.jp.nissan.biz/proxy/proxy.pac"
}
auth = HTTPProxyAuth("FJT02198", "!QAZ5tgb")

URL_TOKEN = "https://identity.jp-east-1.cloud.global.fujitsu.com/v3/auth/tokens" # URL GET TOKEN
URL_PUT = "https://objectstorage.jp-east-1.cloud.global.fujitsu.com/v1/AUTH_2c52bad8d9d04b02abb78389c27ac5fa/OS-FQIDRV-007/pytest/{0}" # URL PUT DATA

TOKEN_BODY = {"auth":{"identity":{"methods":["password"],"password":{"user":{"domain":{"name":"BeY246eW"}, "name": "FJT00871", "password":"k-~}q55P6Un8QV~k"}}}, "scope": { "project": {"id": "2c52bad8d9d04b02abb78389c27ac5fa"}}}}

class K5:
    def __init__(self, infile, outfile):
        self._infile = infile
        self._outfile = outfile
    @property
    def outfile(self):
        return self._outfile
        
    def GetToken(self):
        try:
            s = requests.Session()
            #s.keep_alive = False
            s.trust_env=False
            s.proxies = proxies_s
            s.auth = auth
            self.session = s
            #r = s.get("https://www.google.co.jp/", proxies=proxies)
            #print(r)
            headers = {"Accept": "application/json", "Content-Type" : "application/json", "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"}
            resp=s.post(URL_TOKEN, headers=headers, json=TOKEN_BODY, timeout=(10, 30))
            self.token = resp.headers['X-Subject-Token']
            logger.debug("Token: {0}".format(self.token))
            #print("Proxy with request headers:{0}".format(self.session.headers))
        except ProxyError:
            print("Proxy Error with request headers:{0}".format(self.session.headers))
    def PutData(self):
        s = self.session
        headers = {"Content-Type": "application/octet-stream", "Content-Length": 'os.stat("3G.dummy").st_size', "X-Detect-Content-Type" : "True", "X-Auth-Token":self.token, \
        "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"}
        with open(self._infile, 'rb', buffering=0) as f:
            #data = f.read()
            logger.debug("Start put {0} to {1} at {2}".format(self._infile, self._outfile, str(datetime.now())))
            resp=s.put(URL_PUT.format(self._outfile), headers=headers, data=f, stream=True, timeout=(10, 30))
        logger.debug("Put response code: {0}".format(resp))

if __name__ == '__main__':
    parser = OptionParser()
    (options, args) = parser.parse_args()
    shandler = StreamHandler()
    fhandler = FileHandler('log.txt', 'w')
    shandler.setLevel(DEBUG)
    fhandler.setLevel(DEBUG)
    logger.setLevel(DEBUG)
    logger.addHandler(shandler)
    logger.addHandler(fhandler)
    #subprocess.call('curl -p --proxy-user FJT02198:!QAZ5tgb -x 10.16.1.103:8080 -L https://www.google.c')
    k5=K5(args[0], "{0}_{1}_{2}".format(args[1], args[2], args[3]))
    k5.GetToken()
    start = time.time()
    k5.PutData()
    elapsed_time = time.time() - start
    logger.debug("PUT {0} end: {1}\nelapsed_time: {2}[sec]".format(k5.outfile, str(datetime.now()), elapsed_time))
"""
import requests

#http://docs.python-requests.org/en/latest/user/quickstart/#post-a-multipart-encoded-file

url = "http://localhost:5000/"
fin = open('simple_table.pdf', 'rb')
files = {'file': fin}
try:
  r = requests.post(url, files=files)
    print r.text
finally:
fin.close()
"""
