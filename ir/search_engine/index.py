# -*-coding:utf-8 -*-
# 建立索引
from whoosh.fields import *
from whoosh.index import create_in,open_dir
from whoosh.qparser import QueryParser
from whoosh.analysis import RegexAnalyzer,Tokenizer,Token
from whoosh import  scoring
import jieba
import os
class ChineseTokenizer(Tokenizer):
    def __call__(self, value, positions=False, chars=False,keeporiginal=False, removestops=True,start_pos=0, start_char=0, mode='', **kwargs):
        # 去除停用词及符号
        with open('usr/stop_words_ch.txt','r')as f:
            stop_list=f.read().split('\n')
        assert isinstance(value, text_type), "%r is not unicode" % value
        t = Token(positions, chars, removestops=removestops, mode=mode,**kwargs)
        #使用结巴搜索引擎模式分词库进行分词
        seglist=jieba.cut_for_search(value)
        for w in seglist:
            if w not in stop_list:
                t.original = t.text = w
                t.boost = 1.0
                if positions:
                    t.pos=start_pos+value.find(w)
                if chars:
                    t.startchar=start_char+value.find(w)
                    t.endchar=start_char+value.find(w)+len(w)
                yield t
                #通过生成器返回每个分词的结果token
def ChineseAnalyzer():
    return ChineseTokenizer()
# html预处理 提取问题标题和细节
def preprocessing(path):
    with open(path,'r')as f:
        passage=f.readlines()
        title=passage[0]
        content=''.join(passage[1:])
    return content,title
def index_create():
#用中文分词器代替原先的正则表达式解释器。
    analyzer=ChineseAnalyzer()
    # 列出index的所有域
    schema=Schema(title=TEXT(stored=True,analyzer=analyzer),path=ID(stored=True),content=TEXT(stored=True,analyzer=analyzer))
    if not os.path.exists('indexer'):
        os.mkdir('indexer/')
    ix=create_in('indexer',schema)
    # 将所有文本加入索引
    writer=ix.writer()
    for root,dirs,files in os.walk('qa_tooth/'):
        for file in files:
            path2=os.path.join(root,file)
            content2,title2=preprocessing(path2)
            writer.add_document(title=title2,path=path2.split('/')[1],content = content2)
    writer.commit()
if __name__ == '__main__':
    index_create()
