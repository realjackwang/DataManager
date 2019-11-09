# encoding = utf-8
# =====================================================
#   Copyright (C) 2019 All rights reserved.
#
#   filename : mysql.py
#   version  : 0.1
#   author   : Jack Wang / 544907049@qq.com
#   date     : 2019/11/7 下午 12:03
#   desc     : 用于对数据库进行操作
# =====================================================

import sqlite3


# import configparser

# # 读取config
# conf = configparser.ConfigParser()
# conf.read('config.ini', encoding="utf-8-sig")
# items = conf.get("DETAIL", "columns").split('，')


def init_database():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    c.execute('''create table user_tb(
        _id integer primary key autoincrement,
        name text,
        phone integer,
        card integer,
        balance double,
        gender text,
        birth text,
        note text
        )''')

    c.execute('''create table bill_tb(
           _id integer primary key autoincrement,
           time text,
           type text,
           cost double,
           balance double,
           name text,
           phone integer,
           card integer
           )''')

    c.execute('''create table balance_tb(
           _id integer primary key autoincrement,
           time text,
           balance double
           )''')

    c.execute('insert into balance_tb values(null, ?, ?)',
              ('0', '0'))
    conn.commit()
    c.close()
    conn.close()





def add_person(name, phone, card, balance, gender, birth, note):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('insert into user_tb values(null, ?, ?, ?, ?, ?, ?, ?)',
              (name, phone, card, balance, gender, birth, note))
    conn.commit()

    c.close()
    conn.close()


def del_person(phone):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('select * from user_tb where phone = ' + phone)
    result = c.fetchall()
    if result:
        print(result[0][0])
        c.execute('delete from user_tb where _id = ' + str(result[0][0]))
        conn.commit()
    c.close()
    conn.close()


def query(table, key, value):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('select * from ' + table + ' where +' + key + ' = ' + value)
    result = c.fetchall()
    c.close()
    conn.close()
    if result:
        return result
    return None


def change(id, key, value):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('update user_tb set ' + key + ' = ' + value + ' where _id = ' + id)
    conn.commit()
    c.close()
    conn.close()


def add_bill(time, type, cost, balance, name, phone, card):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('insert into bill_tb values(null, ?, ?, ?, ?, ?, ?, ?)',
              (time, type, cost, balance, name, phone, card))
    conn.commit()
    c.close()
    conn.close()


def change_balance(time, balance):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('update balance_tb set balance =?,time =? where _id = 1', (balance, time))
    conn.commit()
    c.close()
    conn.close()
