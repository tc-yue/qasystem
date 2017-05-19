# -*- coding:utf-8 -*-
import sqlite3
import re
import requests

# 去重列表
medicine_name_list = []
# 药物ID
medicine_id = [0]


# 获取疾病大类例如：肝炎的子链接
def get_sub_url():
    html = requests.get('http://www.a-hospital.com/w/%E8%A1%A5%E9%93%81%E5%92%8C%E8%A1%A5%E7%A1%92%E7%9A%84%E8%8D%AF%E5%93%81%E5%88%97%E8%A1%A8')
    li = re.findall(r'药品百科([\s|\S]*?)世界卫生', html.text)
    list2 = []
    li2 = re.findall(r'<li><a href=\"([\s|\S]*?)\" title=', li[0])
    for i in li2:
        list2.append('http://www.a-hospital.com'+i)
    return list2


# 创建表
def create_table(cursor1):
    # 名称，适应症，禁忌，用法，不良反应，注意
    # cursor1.execute('''CREATE TABLE DRUG
    #               (ID INT PRIMARY    KEY   NOT NULL,
    #                NAME              TEXT,
    #                INDICATIONS       TEXT,
    #                CONTRAINDICATIONS TEXT,
    #                DOSAGE            TEXT,
    #                ADVERSEREACTIONS  TEXT,
    #                COMPOSITION       TEXT,
    #                PRECAUTIONS       TEXT);''')
    cursor1.execute('''CREATE TABLE MEDICINE
                  (ID INT PRIMARY    KEY   NOT NULL,
                   NAME              TEXT  NOT NULL,
                   INDICATIONS       TEXT);''')


# 清空表
def delete_items(cursor1):
    cursor1.execute("DELETE FROM MEDICINE")


# 添加某个疾病的药物
def add(url, cursor1):
    html = requests.get(url)
    li = re.findall(r'<li>([\s|\S]*?)</li>', html.text)
    list2 = []
    for i in li:
        a = re.sub(r'<[\s|\S]*?>', '', i).split('\n\n')
        list2.append(a)
    print('----')
    for item in list2:
        if len(item) == 2 and item[0] not in medicine_name_list:
            print(item)
            medicine_name = item[0]
            medicine_name_list.append(medicine_name)
            disease_name = item[1]
            cursor1.execute("insert into MEDICINE(ID,NAME,INDICATIONS) values(?, ?, ?)", (medicine_id[0], medicine_name, disease_name))
            medicine_id[0] += 1


# 添加所有条
def add_all(cursor1):
    delete_items(cursor1)
    for sub_url in get_sub_url():
        try:
            add(sub_url,cursor1)
        except Exception as e:
            print(e)


def show_table(cursor1):
    cursor1.execute("select * from MEDICINE")
    # cursor1.execute("select * from MEDICINE where INDICATIONS like '%牙龈出血%'")
    values = cursor1.fetchall()
    for i in values:
        print(i)


if __name__ == '__main__':
    conn = sqlite3.connect('medicine.db')
    cursor = conn.cursor()
    show_table(cursor)
    cursor.close()
    conn.commit()
    conn.close()
