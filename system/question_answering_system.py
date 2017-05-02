import logging
from ir.data_source import DataSource
from question_type_analysis.pattern_based_multilevel_question_classifier import PatternBasedMultiLevelQuestionClassifier
from selector.candidate_answer_select import *
from score.evidence_score import EvidenceScore
from score.answer_score import AnswerScore
from model.questiontype import QuestionType
"""
使用问答系统实现要指定4个组件 1：问答系统使用的数据源  2：候选答案提取器
3.证据评分组件 4.候选答案评分组件
"""


class QuestionAnsweringSystem:
    logging.info('开始构造问答系统')

    def __init__(self):
        self.__question_index = 1
        # todo 两个参数未定
        self.__question_classifier = PatternBasedMultiLevelQuestionClassifier()
        self.__data_source = DataSource()
        # todo 函数or类的静态方法
        self.__candidate_answer_select = CandidateAnswerSelect
        self.__evidence_score = EvidenceScore()
        self.__answer_score = AnswerScore()

    # 问答使用的分类器
    def set_question_classifier(self, question_classifier):
        self.__question_classifier = question_classifier

    def get_question_classifier(self):
        return self.__question_classifier

    # 数据源
    def set_data_source(self, data_source):
        self.__data_source = data_source

    def get_data_source(self):
        return self.__data_source

    # 候选答案提取器
    def set_candidate_answer_select(self, candidate_answer_select):
        self.__candidate_answer_select = candidate_answer_select

    def get_candidate_answer_select(self):
        return self.__candidate_answer_select

    # 候选答案评分组件
    def set_answer_score(self, answer_score):
        self.__answer_score = answer_score

    def get_answer_score(self):
        return self.__answer_score

    # 证据评分组件
    def set_evidence_score(self, evidence_score):
        self.__evidence_score = evidence_score

    def get_evidence_score(self):
        return self.__evidence_score

    # 利用数据源搜索并回答问题
    def answer_question(self, question_str):
        question = self.__data_source.get_evidence(question_str)
        if question is not None:
            question = self.__question_classifier.classify(question)
            logging.info('开始处理Question:'+question.get_question()+'问题类型:'+question.get_question_type())
            if question.get_question_type() == QuestionType.NUll:
                logging.error('未知问题类型，拒绝回答')
            i = 1
            for evidence in question.get_evidences():
                logging.debug('开始处理Evidence '+str(i))
                i += 1
                # 对证据进行评分 证据分值存储在evidence 对象里面
                self.__evidence_score.score(question, evidence)
                logging.debug('evidence detail')
                # 提取候选答案 存储在evidence对象里
                self.__candidate_answer_select.common_candidate_answer_select(question, evidence)
                candidate_answer_collection = evidence.get_candidate_answer_collection()
                if len(candidate_answer_collection) != 0:
                    candidate_answer_collection.show_all()
                    self.__answer_score.score(question, evidence, candidate_answer_collection)
                    candidate_answer_collection.show_all()
                    logging.debug('候选答案已经评分')
                else:
                    logging.debug('无候选答案')
                for candidate_answer in question.get_all_candidate_answer():
                    logging.info(candidate_answer.get_answer()+' '+candidate_answer.get_score())





