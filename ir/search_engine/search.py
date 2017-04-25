# -*-coding:utf-8 -*-
# 检索web服务
from whoosh.fields import *
from whoosh.index import create_in,open_dir
from whoosh.qparser import QueryParser
from whoosh.analysis import RegexAnalyzer,Tokenizer,Token
from whoosh import  scoring
import jieba
import os
from flask import Flask,request,render_template
app = Flask(__name__)
@app.route('/', methods=['GET'])
def home():
    return render_template('form.html')
@app.route('/sub',methods=['GET'])
def quer():
    # 需要从request对象读取表单内容：
    resultslist=index_open('牙科')
    return render_template('form.html', page_list=resultslist)

@app.route('/', methods=['POST'])
def query():
    # 需要从request对象读取表单内容：
    resultslist=index_open(request.form['word'])
    return render_template('form.html', page_list=resultslist)

class ChineseTokenizer(Tokenizer):
    def __call__(self, value, positions=False, chars=False,keeporiginal=False, removestops=True,start_pos=0, start_char=0, mode='', **kwargs):
        # 去除停用词及符号
        with open('usr/stop_words_ch.txt','r')as f:
            stop_list=f.read().split('\n')
        assert isinstance(value, text_type), "%r is not unicode" % value
        #使用结巴搜索引擎模式分词库进行分词
        t = Token(positions, chars, removestops=removestops, mode=mode,**kwargs)
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
def index_open(word):
    resultslist=[]
    ix = open_dir('indexer')
    #
    with ix.searcher(weighting=scoring.TF_IDF()) as search:
        parser=QueryParser('content',ix.schema).parse(word)
        print(parser)
        # 最多30个结果
        results=search.search(parser,limit=30)
        # 每个结果最多300个字符
        results.fragmenter.charlimit = 200
        for i in results:
            # 匹配高亮
            print(i)
            resultslist.append((i['path'],i['title'],i.highlights('content').replace(r'">','" style="color:red">')))
    return resultslist
if __name__ == '__main__':
    app.run()
