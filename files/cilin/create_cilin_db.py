# -*- coding:utf-8 -*-
import sqlite3
import re
import requests


# 创建表
def create_table(cursor1):
    #                PRECAUTIONS       TEXT);''')
    cursor1.execute('''CREATE TABLE CILIN
                  (ID INT PRIMARY   KEY   NOT NULL,
                 LABELS               TEXT   NOT NULL,
                  WORD               TEXT  NOT NULL);''')


# 清空表
def delete_items(cursor1):
    cursor1.execute("DELETE FROM CILIN")


# 添加
def add(cursor1):
    with open('../files/cilin.txt','rb') as f:
        lines = f.readlines()
    num = 0
    for i in lines:
        item = i.decode('gbk')
        label = item[0:8]
        words_list = item[9:].replace('\r\n','').split(' ')
        for j in words_list:
            cursor1.execute("insert into CILIN(ID,LABELS,WORD) values(?,?,?)", (num, label, j))
            num += 1




def show_table(cursor1):
    cursor1.execute("select * from CILIN where word = '骄傲'")
    # cursor1.execute("select * from CILIN where WORD like '%牙龈出血%'")
    values = cursor1.fetchall()
    for i in values:
        print(i)


if __name__ == '__main__':
    conn = sqlite3.connect('cilin.db')
    cursor = conn.cursor()
    # create_table(cursor)
    # add(cursor)
    show_table(cursor)
    cursor.close()
    conn.commit()
    conn.close()

