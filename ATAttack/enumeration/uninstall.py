import subprocess
import json

def powershell(cmd):

    arg = [r"powershell.exe", cmd]
    ps = subprocess.Popen(arg, stdout=subprocess.PIPE)
    num = ps.stdout.read().decode('gbk')
    write = num.split('\r\n')
    return write


def query_results():
    apply = []
    version = [
        r'HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\\',
        r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\\']
    for x in version:
        QueryPath = r'$RegPath = "Registry::{}\\";'.format(
            x) + '$QueryPath = dir $RegPath -Name;' + 'foreach($Name in $QueryPath)' + '{(Get-ItemProperty -Path $RegPath$Name).DisplayName}'
        apply.append(powershell(QueryPath))
    return json.dumps(apply, encoding="UTF-8", ensure_ascii=False)
