#!/usr/bin/python
# coding=utf-8

import threading
# import paramiko
import subprocess
import Queue
import re

adder = []
queue = Queue.Queue()
# out_queue = Queue.Queue()

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
            if re.findall("TTL=\d+",result,re.S):
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


# class DatamineThread(threading.Thread):
#     def __init__(self, out_queue):
#         threading.Thread.__init__(self)
#         self.out_queue  = out_queue
#         self.port = int(22)
#         self.timeout = 2.5
#         self.user = ['root','oracle']
#         self.passwd = ['root','oracle']
#
#     def run(self):
#
#         while True:
#             host = self.out_queue.get()
#             try:
#                 ssh = paramiko.SSHClient()
#                 ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#                 ssh.connect(host, self.port, '', '', timeout=self.timeout)
#                 ssh.close()
#             except Exception as e:
#                 try:
#                     if 'Authentication' in str(e):
#                         for user in self.user:
#                             for passwd in self.passwd:
#                                 ssh.connect(host, self.port, user, passwd, timeout=self.timeout)
#                                 print host + " ssh Weak password " + self.user + "//" + self.port
#                 except Exception as e:
#                     print e
#                     ssh.close()
#             self.out_queue.task_done()

# def creakssh(cidr):
#     # with open('host_dic.txt') as inFile:
#     #     while True:
#     #         pwd = inFile.readline().strip()
#     #         if len(pwd) == 0: break
#     #         cidr.append(pwd)
#     for i in range(100):
#         t = DatamineThread(out_queue)
#         t.setDaemon(True)
#         t.start()
#     for host in cidr:
#         out_queue.put(host)
#     out_queue.join()


