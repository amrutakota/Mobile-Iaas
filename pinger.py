#!/usr/bin/python

import subprocess
import threading
import sqlite3


class Pinger(object):
    status = {'alive': [], 'dead': []}
    hosts = []
    thread_count = 4
    lock = threading.Lock()

    def ping(self, ip):
        ret = subprocess.call(['ping', '-c', '1', '-W', '1', ip],
                              stdout=open('/dev/null', 'w'), stderr=open('/dev/null', 'w'))
        return ret == 0

    def pop_queue(self):
        ip = None
        self.lock.acquire()
        if self.hosts:
            ip = self.hosts.pop()
        self.lock.release()
        return ip

    def dequeue(self):
        while True:
            ip = self.pop_queue()
            if not ip:
                return None
            result = 'alive' if self.ping(ip) else 'dead'
            self.status[result].append(ip)

    def start(self):
        threads = []
        for i in range(self.thread_count):
            t = threading.Thread(target=self.dequeue)
            t.start()
            threads.append(t)
        [ t.join() for t in threads ]
        return self.status

