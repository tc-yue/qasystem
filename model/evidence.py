from model.candidate_answer_collection import CandidateAnswerCollection
from parser.word_parser import WordParser
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
                    filename='test.log',
                    filemode='w')
"""
证据由title：问题 和snippet：回答 组成 对于同一个问题来说
不同证据的重要性不一样，所以证据有分值，证据有多个候选答案
jieba.load dict
"""


class Evidence:

    def __init__(self):
        # 元素类型CandidateAnswer的实例
        self.__candidate_answer_collection = CandidateAnswerCollection()
        self.__title = ''
        self.__score = 1.0
        self.__snippet = ''

    def get_title_words(self):
        return WordParser.lcut(self.__title)

    def get_snippet_words(self):
        return WordParser.lcut(self.__snippet)

    def get_words(self):
        return WordParser.lcut(self.__title + self.__snippet)

    def get_title(self):
        return self.__title

    def set_title(self, title):
        self.__title = title

    def get_snippet(self):
        return self.__snippet

    def set_snippet(self, snippet):
        self.__snippet = snippet

    def get_score(self):
        return self.__score

    def add_score(self, score):
        self.__score += score

    def get_candidate_answer_collection(self):
        return self.__candidate_answer_collection

    def set_candidate_answer_collection(self, candidate_answer_collection):
        self.__candidate_answer_collection = candidate_answer_collection
