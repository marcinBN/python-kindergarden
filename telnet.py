#!/usr/bin/python
#-*- coding: utf-8 -*-

#-*- coding: utf-8 -*-

import select
from socket import *
import sys

def prompt():
    sys.stdout.write('> ')
    sys.stdout.flush()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Usage: telnet.py host port'
        sys.exit()
    host, port = sys.argv[1], int(sys.argv[2])
    buf = 4096
    s = socket(AF_INET, SOCK_STREAM)
    try:
        s.connect((host, port))
    except:
        print 'Unable to connect'
        sys.exit()
    sList = [sys.stdin, s]
    
    while 1:
        rS, wS, eS = select.select(sList, [], [])
        for sock in rS:
            if sock == s:
                data = sock.recv(buf)
                if not data:
                    print '\nDisconnected from chat server'
                    sys.exit()
                else:
                    sys.stdout.write(data)
                    prompt()
            else:
                data = sys.stdin.readline()
                s.send(data)
    
