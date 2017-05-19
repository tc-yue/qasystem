# -*-coding:utf-8 -*-
# 建立索引
from whoosh.fields import *
from whoosh.index import create_in, open_dir
import os
from jieba.analyse import ChineseAnalyzer


def pre_processing(path):
    with open(path, 'r')as f:
        passage = f.readlines()
        try:
            title = passage[0]
            # 有些问句 有多个解决答案
            content = ''.join(passage[1:])
            return content, title
        except Exception as e:
            print(e)
            print(path)
            return None


def index_create():
    # 用中文分词器代替原先的正则表达式解释器。
    analyzer = ChineseAnalyzer()
    # 列出index的所有域,title 评分×3
    schema = Schema(title=TEXT(stored=True, analyzer=analyzer, field_boost=3.0),
                    path=ID(stored=True), content=TEXT(stored=True, analyzer=analyzer))
    if not os.path.exists('indexer'):
        os.mkdir('indexer')
    ix = create_in('indexer', schema)
    # 将所有文本加入索引
    writer = ix.writer()
    dir_list = ['qa_bone', 'qa_dermatological', 'qa_ear', 'qa_eye', 'qa_internal', 'qa_surgery', 'qa_tooth']
    for i in dir_list:
        print(i)
        for root, dirs, files in os.walk('../qa_data/'+i+'/'):
            for file in files:
                path2 = os.path.join(root, file)
                data = pre_processing(path2)
                if data is not None:
                    content2, title2 = data
                    writer.add_document(title=title2, path=path2.split('/')[-1], content=content2)
    writer.commit()


def add_index():
    ix = open_dir('/home/tianchiyue/learn/chatrobot/whoosh_search/search_engine/indexer')
    writer = ix.writer()
    dir_list = ['05-'+str(i).zfill(2) for i in range(2, 15)]
    for i in dir_list:
        print(i)
        for root, dirs, files in os.walk('../qa_data/'+i+'/'):
            for file in files:
                path2 = os.path.join(root, file)
                data = pre_processing(path2)
                if data is not None:
                    content2, title2 = data
                    writer.add_document(title=title2, path=path2.split('/')[-1], content=content2)
    writer.commit()

if __name__ == '__main__':
    add_index()
