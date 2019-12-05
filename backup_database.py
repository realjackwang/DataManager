# encoding = utf-8
# =====================================================
#   Copyright (C) 2019 All rights reserved.
#
#   filename : backup_database.py
#   version  : 0.1
#   author   : Jack Wang / 544907049@qq.com
#   date     : 2019-12-04 下午 4:22
#   desc     : 
# =====================================================

# import winreg
# import os
from shutil import copy
from time import strftime, localtime


# def get_desktop():
#     key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
#     return str(winreg.QueryValueEx(key, "Personal")[0])
#
#
# def create_dir():
#     document = get_desktop()
#     if not os.path.exists(os.path.join(document, 'DataManager')):
#         os.mkdir(os.path.join(document, 'DataManager'))


def backup():
    try:
        copy('./database/data.db',
             './database/data' + strftime("%Y-%m-%d %H:%M:%S", localtime()) + '.db')
    except IOError as e:
        print("Unable to copy file. %s" % e)
