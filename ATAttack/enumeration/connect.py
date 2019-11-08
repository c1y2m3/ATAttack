# !/usr/bin/env python
# coding:utf-8

from ATAttack.framework.prints import *
import _winreg
import os


key = r"Software\Microsoft\Terminal Server Client\Servers"
open_key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, key)
countkey = _winreg.QueryInfoKey(open_key)[0]
values = []
K = 0



class login_():

    @staticmethod

    def ListLogged_inUsers():
        # User = getpass.getuser()
        try:
            for i in range(int(countkey)):
                db = _winreg.EnumKey(open_key, i)
                servers = _winreg.OpenKey(
                    _winreg.HKEY_CURRENT_USER, key + "\\" + db)
                name, value, type = _winreg.EnumValue(servers, K)
                values.append(db + "|" + value)
                # values['current_user'] = User
                # values['Server'] = db
                # values['UsernameHint'] = value
            _winreg.CloseKey(open_key)
        except WindowsError:
            pass

    # ListAllUsers RDP Connections History
    def powershell(self,cmd):
        powershell = os.popen(r"powershell.exe " + cmd).read()
        stdout = powershell.split('\n')
        return stdout

    def AllUser(self):

        cmd = "$AllUser = Get-WmiObject -Class Win32_UserAccount;" \
              "foreach($User in $AllUser)" \
              "{Write-Host $User.Caption};"
        cmder = "$AllUser = Get-WmiObject -Class Win32_UserAccount;" \
            "foreach($User in $AllUser)" \
            "{Write-Host $User.SID};"

        user_name = self.powershell(cmd)
        sid = self.powershell(cmder)

        num = {}
        for y in range(len(user_name)):
            num[user_name[y]] = sid[y]

        for id in sid:
            try:
                dba = _winreg.OpenKey(_winreg.HKEY_USERS, id + "\\" + key)
                count = _winreg.QueryInfoKey(dba)[0]
                for s in range(int(count)):
                    dbs = _winreg.EnumKey(dba, s)
                    server = _winreg.OpenKey(
                        _winreg.HKEY_USERS,
                        id + os.sep + key + "\\" + dbs)
                    name, value, type = _winreg.EnumValue(server, K)

                    # print values
                    for www in num:
                        if num[www] == id:
                            # print "SID :" + id
                            values.append(dbs + "|" + value )
                            # print "User:" + www + ":" + value + ":" + dbs
            except WindowsError:
                pass

    def rdplogin_(self):

        print_warning("ListLogged-inUsers RDP Connections History")
        self.ListLogged_inUsers()
        print_warning("ListAllUsers RDP Connections History")
        self.AllUser()
        print list(set(values))

