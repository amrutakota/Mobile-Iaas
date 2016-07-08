#!/usr/bin/python

import socket 
import os
from threading import Thread
import time
from pinger import Pinger
from dbops import createTable,insert,pingips,updatedead,select

PORT=12345

def monitor():
    ping = Pinger()
    ping.thread_count = 4
    while True:
        ping.hosts = pingips()
        nodes=ping.start()
        for ip in nodes['dead']:
            updatedead(ip)
        time.sleep(1)
        os.system("clear")
        select()

s = socket.socket()
host = socket.gethostname()
port = PORT
s.bind(('', port))
s.listen(5)
createTable()
healthmonitor=Thread(target=monitor)
healthmonitor.start()
while True:
	c, addr = s.accept()
	data=c.recv(47)
	mac,ip,disk,ram,wifi=data.split()
	insert(mac,ip,disk,ram,wifi)
	c.close()
s.close()
healthmonitor.close()
