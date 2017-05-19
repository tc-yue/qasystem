# -*-coding:utf-8 -*-
from flask import Flask, request,render_template
import requests

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return render_template('form.html')


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
    result = chat(request.form['word'])
    return render_template('form2.html', page_list=result)


@app.route('/test', methods=['GET'])
def test():
    if request.method == 'GET':
        return render_template('form3.html')
    # 需要从request对象读取表单内容：
    # result = chat(request.form['word'])
    # print(result)
    # return render_template('form3.html', page_list=result)


@app.route('/test', methods=['POST'])
def test2():
    print(request.form['word'])
    sentence = chat(request.form['word'])
    return sentence


def chat(word):
    args = {'key': '525ef6b3a42043c196e9df0d549bc68f', 'info': word}
    response = requests.post(url='http://www.tuling123.com/openapi/api', data=args)
    data = response.json()['text']
    return data


def index_open(a):
    return 'first'
if __name__ == '__main__':
    app.run()
