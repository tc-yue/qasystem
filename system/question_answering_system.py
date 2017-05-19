from evidence_retrieval.data_source import DataSource
from question_type_analysis.pattern_based_question_classifier import PatternBasedMultiLevelQuestionClassifier
from selector.candidate_answer_select import *
from score.evidence_score import EvidenceScore
from score.answer_score import AnswerScore
from model.questiontype import QuestionType
from model.question import Question
from question_type_analysis.question_pattern import QuestionPattern
from question_type_analysis.pattern_match_strategy import PatternMatchStrategy
from question_type_analysis.pattern_match_result_selector import PatternMatchResultSelector
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
                    filename='../qa.log',
                    filemode='w')
"""
使用问答系统实现要指定4个组件
1：问答系统使用的数据源  2：候选答案提取器
3.证据评分组件 4.候选答案评分组件
"""


class QuestionAnsweringSystem:
    logging.info('开始构造问答系统')

    def __init__(self):
        self.__question_index = 1
        # todo 函数or类的静态方法
        self.__candidate_answer_select = CandidateAnswerSelect
        self.__evidence_score = EvidenceScore()
        self.__answer_score = AnswerScore()
        # 问题分类器
        pattern_match_strategy = PatternMatchStrategy()
        pattern_match_strategy.add_question_pattern(QuestionPattern.Question)
        pattern_match_strategy.add_question_pattern(QuestionPattern.TermWithNatures)
        pattern_match_strategy.add_question_pattern(QuestionPattern.Natures)
        pattern_match_strategy.add_question_pattern(QuestionPattern.MainPartPattern)
        pattern_match_strategy.add_question_pattern(QuestionPattern.MainPartNaturePattern)
        pattern_match_strategy.add_question_type_pattern_files('QuestionTypePatternLevel1_true.txt')
        pattern_match_strategy.add_question_type_pattern_files('QuestionTypePatternLevel2_true.txt')
        pattern_match_strategy.add_question_type_pattern_files('QuestionTypePatternLevel3_true.txt')
        pattern_match_result_selector = PatternMatchResultSelector()
        self.__question_classifier = PatternBasedMultiLevelQuestionClassifier(pattern_match_strategy, pattern_match_result_selector)

    # 问答使用的分类器
    def set_question_classifier(self, question_classifier):
        self.__question_classifier = question_classifier

    def get_question_classifier(self):
        return self.__question_classifier

    # 数据源
    # def set_data_source(self, data_source):
    #     self.__data_source = data_source
    #
    # def get_data_source(self):
    #     return self.__data_source

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

    # 回答问题
    def answer_question(self, question_str):
        question = Question()
        question.set_question(question_str)
        question = self.__question_classifier.classify(question)
        logging.info('开始处理Question:'+question.get_question()+'问题类型:'+str(question.get_question_type()))
        if question.get_question_type() == QuestionType.Null:
            logging.error('未知问题类型，拒绝回答')
        if question.get_question_type() != QuestionType.Solution:
            question = self.kb_based_answer_question(question)
        else:
            question = self.ir_based_answer_question(question)
        logging.info('候选答案: '+question.get_expect_answer())

    @staticmethod
    def kb_based_answer_question(question):
        question = DataSource.select_medicine(question)
        return question

    def ir_based_answer_question(self, question):
        question = DataSource.get_evidence(question)
        if len(question.get_evidences()) == 0:
            logging.debug('无evidence')
            return question
        i = 1
        for evidence in question.get_evidences():
            logging.debug('开始处理Evidence：' + str(i))
            i += 1
            self.__evidence_score.score(question, evidence)
            logging.debug(evidence.get_title_words())
        # 候选证据排序，获得评分第一的设定为期待答案
        evidences = sorted(question.get_evidences(), key=lambda ans: ans.get_score(), reverse=True)
        question.set_expect_answer(evidences[0].get_snippet())
        return question

    # 利用数据源搜索并回答所有问题
    def common_answer_question(self, question_str):
        question = DataSource.get_evidence(question_str)
        if question is not None:
            question = self.__question_classifier.classify(question)
            logging.info('开始处理Question:'+question.get_question()+'问题类型:'+str(question.get_question_type()))
            if question.get_question_type() == QuestionType.Null:
                logging.error('未知问题类型，拒绝回答')
            i = 1
            if len(question.get_evidences()) == 0:
                logging.debug('无evidence')
            for evidence in question.get_evidences():
                logging.debug('开始处理Evidence '+str(i))
                i += 1
                # 对证据进行评分 证据分值存储在evidence 对象里面
                self.__evidence_score.score(question, evidence)
                logging.debug('evidence detail')
                # 提取候选答案 存储在evidence对象里
                self.__candidate_answer_select.common_candidate_answer_select(question, evidence)
                candidate_answer_collection = evidence.get_candidate_answer_collection()
                if candidate_answer_collection is not None:
                    candidate_answer_collection.show_all()
                    self.__answer_score.score(question, evidence, candidate_answer_collection)
                    candidate_answer_collection.show_all()
                    logging.debug('候选答案已经评分')
                else:
                    logging.debug('无候选答案')
                for candidate_answer in question.get_all_candidate_answer():
                    logging.info(candidate_answer.get_answer()+' '+str(candidate_answer.get_score()))

if __name__ == '__main__':
    qa = QuestionAnsweringSystem()
    qa.answer_question('牙疼怎么办')




