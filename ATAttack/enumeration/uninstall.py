import os
import json

def powershell(cmd):

    arg = r"powershell.exe " + cmd
    powershell_ = os.popen(arg).read()
    num = powershell_.decode('gbk')
    write = num.split('\r\n')
    return write

def regedit():
    list_ = []
    version = [
        r'HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\\',
        r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\\']
    for os in version:
        query = r"$RegPath = 'Registry::{}\\';".format(os)+ '$QueryPath = dir $RegPath -Name;' \
                    + 'foreach($Name in $QueryPath)' + '{(Get-ItemProperty -Path $RegPath$Name).DisplayName}'
        list_.append(powershell(query))
    return json.dumps(list_, encoding="UTF-8", ensure_ascii=False)

