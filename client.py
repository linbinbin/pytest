#!/usr/bin/env python
# -*- coding:utf-8 -*-
import socket

ADDR, PORT = 'localhost', 8001
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((ADDR, PORT))

while 1:
    cmd = input('>>:').strip()
    print(cmd)
    if len(cmd) == 0: continue
    client.send(cmd.encode('utf-8'))
    data = client.recv(1024)
    print(data)
    #print('Received', repr(data))

client.close()