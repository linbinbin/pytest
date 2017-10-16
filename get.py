# coding: utf-8

#!/usr/bin/python

import base64
import sys
import os
import datetime
import json
import hmac
import hashlib
import requests
from requests.auth import HTTPProxyAuth
import time

proxies_s = {
"http":'http://"FJT02198":"!QAZ5tgb"@10.16.1.103:8080',
"https":'https://"FJT02198":"!QAZ5tgb"@10.16.1.103:8080'
}

proxies = {
"http":"http://proxypac.jp.nissan.biz/proxy/proxy.pac",
"https":"https://proxypac.jp.nissan.biz/proxy/proxy.pac"
}
auth = HTTPProxyAuth("FJT02198", "!QAZ5tgb")

URL_TOKEN = "https://identity.jp-east-1.cloud.global.fujitsu.com/v3/auth/tokens" # URL GET TOKEN
URL_GET = "https://objectstorage.jp-east-1.cloud.global.fujitsu.com/v1/AUTH_2c52bad8d9d04b02abb78389c27ac5fa/OS-FQIDRV-007/pytest/1g.dummy" # URL PUT DATA

TOKEN_BODY = {"auth":{"identity":{"methods":["password"],"password":{"user":{"domain":{"name":"BeY246eW"}, "name": "FJT00871", "password":"k-~}q55P6Un8QV~k"}}}, "scope": { "project": {"id": "2c52bad8d9d04b02abb78389c27ac5fa"}}}}

class K5:
    def __init__(self, size_count):
        self.base = ""
        self.count = size_count
        
    def GetToken(self):
        s = requests.Session()
        #s.keep_alive = False
        s.proxies = proxies
        s.auth = auth
        self.session = s
        #r = s.get("http://www.google.co.jp/", proxies=proxies, auth=auth)
        #print(r)
        headers = {"Accept": "application/json", "Content-Type" : "application/json", "User-Agent":"Mozilla/5.0"}
        resp=s.post(URL_TOKEN, headers=headers, json=TOKEN_BODY)
        self.token = resp.headers['X-Subject-Token']
        print(self.token)
        
    def GetData(self):
        s = self.session
        headers = {"X-Auth-Token":self.token}
        resp=s.get(URL_GET, headers=headers)
        print(resp.headers['Content-Length'])

if __name__ == '__main__':
    k5=K5(10)
    k5.GetToken()
    start = time.time()
    k5.GetData()
    elapsed_time = time.time() - start
    print ("Get 1G elapsed_time:{0}".format(elapsed_time) + "[sec]")