from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser
from model.evidence import Evidence
import os
import sqlite3
from collections import Counter
import logging
from model.question import Question


class DataSource:

    @staticmethod
    def index_open(word):
        results_list = []
        ix = open_dir(os.path.abspath(os.path.dirname(__file__)+os.path.sep+os.pardir)+'/evidence_retrieval/indexer')
        with ix.searcher() as search:
            # or query 调整共现 与 高单出现 评分
            # og = qparser.OrGroup.factory(0.5)
            # search 多field
            # parser = MultifieldParser(['title', 'content'], schema=ix.schema, group=og).parse(word)
            parser = MultifieldParser(['title', 'content'], schema=ix.schema).parse(word)
            print(parser)
            # 最多5个结果
            results = search.search(parser, limit=5)
            # 每个结果最多300个字符
            # results.fragmenter.charlimit = 200
            for hit in results:
                results_list.append((hit['title'], hit['content']))
        return results_list

    @staticmethod
    def search_evidence(query):
        evidences = []
        elements = DataSource.index_open(query)
        for item in elements:
            evidence = Evidence()
            evidence.set_title(item[0])
            evidence.set_snippet(item[1])
            evidences.append(evidence)
        return evidences

    @staticmethod
    def get_evidence(question):
        question_str = question.get_question()
        evidences = DataSource.search_evidence(question_str)
        question.add_evidences(evidences)
        return question

    @staticmethod
    def select_medicine(question):
        conn = sqlite3.connect(os.path.dirname(__file__)+'/medicine.db')
        cursor = conn.cursor()
        medicine_list = []
        disease_list = question.get_disease()
        for i in disease_list:
            cursor.execute("select NAME from MEDICINE where INDICATIONS like ?", ['%'+i+'%'])
            values = cursor.fetchall()
            medicine_list += [item[0] for item in values]
        top_list = Counter(medicine_list).most_common(3)
        logging.info(top_list)
        question.set_expect_answer(' '.join([i[0] for i in top_list]))
        cursor.close()
        conn.commit()
        conn.close()
        return question

if __name__ == '__main__':
    a = Question()
    a.set_question('牙疼怎么办')
    b = DataSource.get_evidence(a)
