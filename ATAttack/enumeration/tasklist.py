#! /usr/bin/python
# -*- coding: utf-8 -*-

import platform
import string
import os
import re
import json
from ATAttack.framework.constant import constant
from ATAttack.framework.prints import print_success

temp_list = []


def get_platform():
    return platform.machine()


def disk():

    disk_list = []
    for c in string.ascii_uppercase:
        disk = c + ':'
        if os.path.isdir(disk):
            disk_list.append(disk)
    return disk_list


def tasklist():
    load = os.popen('tasklist').read()
    tasklist = re.findall(r'\w+.exe', load, re.S)
    ing = []
    print_success('Current Machine Existence ' + str(disk()))
    try:
        for av in constant.av_json.keys():
            for task in tasklist:
                if task in av:
                    process = (constant.av_json.setdefault(task, 0))
                    if process != 0:
                        ing.append(process)
        return json.dumps(ing, encoding="UTF-8", ensure_ascii=False)
    except Exception:
        pass


def token():

    tasklist_v_fo_csv = os.popen('tasklist /v /fo csv').read()
    tasklist_v_fo_csv_list = tasklist_v_fo_csv.split("\n")
    try:

        for tasklist in tasklist_v_fo_csv_list:
            tasklist = tasklist.replace(
                "[", "").replace(
                "]", "").replace(
                "\"", "")
            temp = tasklist.split(",")
            sessions = re.findall('[a-zA-Z]+.+', temp[7], re.S)
            if sessions:
                for session in sessions:
                    session = re.sub('CPU.+', '', session)
                    if r"Running" not in session:
                        temp_list.append(session)
    except Exception:
        pass
    finally:
        return ([i for i in list(set(temp_list)) if i != ''])
