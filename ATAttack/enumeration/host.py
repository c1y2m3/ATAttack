#!/usr/bin/python
# coding=utf-8

import threading
import subprocess
import Queue


adder = []
queue = Queue.Queue()


class ThreadUrl(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):

        while True:
            host = self.queue.get()
            cmd = 'ping -n 2 -w 5 {}'.format(
                host,)
            p = subprocess.Popen(cmd,
                                 stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 shell=True
                                 )
            result = p.stdout.read().decode('cp936').encode('utf-8').strip()
            if "TTL=" in result:
                ipadder = host.split('.')[0] + '.' + host.split('.')[1] + '.' + host.split('.')[2] + ".1/24"
                adder.append(ipadder)
            self.queue.task_done()

def ipfind(cidr):

    for i in range(100):
        t = ThreadUrl(queue)
        t.setDaemon(True)
        t.start()
    for host in cidr:
        queue.put(host)
    queue.join()
    return adder
