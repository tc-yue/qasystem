from whoosh.fields import *
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from whoosh.analysis import Tokenizer, Token
from whoosh import scoring
import jieba
from model.question import Question
from model.evidence import Evidence
import os


class ChineseTokenizer(Tokenizer):
    def __call__(self, value, positions=False, chars=False, keeporiginal=False, removestops=True, start_pos=0,
                 start_char=0, mode='', **kwargs):
        # 去除停用词及符号
        with open(os.path.abspath(os.path.dirname(__file__)+os.path.sep+os.pardir)+'/ir/usr/stop_words_ch.txt', 'r')as f:
            stop_list = f.read().split('\n')
        assert isinstance(value, text_type), "%r is not unicode" % value
        # 使用结巴搜索引擎模式分词库进行分词
        t = Token(positions, chars, removestops=removestops, mode=mode, **kwargs)
        seg_list = jieba.cut_for_search(value)
        for w in seg_list:
            if w not in stop_list:
                t.original = t.text = w
                t.boost = 1.0
                if positions:
                    t.pos = start_pos + value.find(w)
                if chars:
                    t.startchar = start_char + value.find(w)
                    t.endchar = start_char + value.find(w) + len(w)
                yield t
                # 通过生成器返回每个分词的结果token


class DataSource:
    @staticmethod
    def ChineseAnalyzer():
        return ChineseTokenizer()

    @staticmethod
    def index_open(word):
        results_list = []
        ix = open_dir(os.path.abspath(os.path.dirname(__file__)+os.path.sep+os.pardir)+'/ir/indexer')
        with ix.searcher(weighting=scoring.TF_IDF()) as search:
            parser = QueryParser('content', ix.schema).parse(word)
            # 最多30个结果
            results = search.search(parser, limit=30)
            # 每个结果最多300个字符
            results.fragmenter.charlimit = 200
            for hit in results:
                results_list.append((hit['title'], hit['content']))
        return results_list

    @staticmethod
    def get_evidence(question_str):
        question = Question()
        question.set_question(question_str)
        evidences = DataSource.search_evidence(question_str)
        question.add_evidences(evidences)
        return question

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


if __name__ == '__main__':
    a = DataSource
    print(a.get_evidence('牙疼怎么办').get_evidences())
