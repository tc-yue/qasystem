# -*-coding:utf-8 -*-
# 检索web服务
from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser
from whoosh import qparser
from jieba.analyse import ChineseAnalyzer
from flask import Flask, request,render_template
import requests

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

@app.route('/chat', methods=['POST','GET'])
def chatbot():
    if request.method == 'GET':
        return render_template('form2.html')
    # 需要从request对象读取表单内容：
    result=chat(request.form['word'])
    return render_template('form2.html', page_list=result)


def chat(word):
    args = {'key': '525ef6b3a42043c196e9df0d549bc68f', 'info': word}
    response = requests.post(url='http://www.tuling123.com/openapi/api', data=args)
    data=response.json()['text']
    return data

def index_open(word):
    results_list = []
    ix = open_dir('search_engine/indexer')
    with ix.searcher() as search:
        # or query 调整共现 与 高单出现 评分
        og = qparser.OrGroup.factory(0.9)
        # search 多field
        parser = MultifieldParser(['title', 'content'], schema=ix.schema, group=og).parse(word)
        # parser = MultifieldParser(['title', 'content'], schema=ix.schema).parse(word)
        print(parser)
        # 最多30个结果
        results=search.search(parser, limit=20)
        # 显示每个结果最多300个字符
        # results.fragmenter.charlimit = 300
        for i in results:
            # 匹配高亮
            print(i)
            results_list.append((i['path'], i['title'], i.highlights('content').replace(r'">', '" style="color:red">')))
    return results
if __name__ == '__main__':
    app.run()
