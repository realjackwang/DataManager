# encoding = utf-8
# =====================================================
#   Copyright (C) 2019 All rights reserved.
#
#   filename : bills.py
#   version  : 0.1
#   author   : Jack Wang / 544907049@qq.com
#   date     : 2019/11/7 下午 7:04
#   desc     : 
# =====================================================

import time
import mysql


def bill_in(cost, name, phone, card):
    balance = float(mysql.query('balance_tb', '_id', '1')[0][2])
    balance += float(cost)
    mysql.add_bill(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                   '收入', str(cost), str(balance), str(name), str(phone), str(card))
    mysql.change_balance(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), str(balance))


def bill_out(cost, name, phone, card):
    balance = float(mysql.query('balance_tb', '_id', '1')[0][2])
    balance -= float(cost)
    mysql.add_bill(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                   '支出', str(cost), str(balance), str(name), str(phone), str(card))
    mysql.change_balance(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), str(balance))
