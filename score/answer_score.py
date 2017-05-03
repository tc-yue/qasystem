from model.candidate_answer import CandidateAnswer
from parser.word_parser import WordParser
import re
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
                    filename='../qa.log',
                    filemode='w')
"""
候选答案评分组件
"""


class AnswerScore:
    def __init__(self):
        self.__term_frequency_weight = 1
        self.__term_distance_weight = 1
        self.__term_distance_mini_weight = 1
        self.__textual_alignment_weight = 1
        self.__more_textual_alignment_weight = 1
        self.__rewind_textual_alignment_weight = 1
        self.__hot_weight = 1
        self.__answer_scores = []

    def add_answer_score(self, answer_score):
        self.__answer_scores.append(answer_score)

    def remove_answer_score(self, answer_score):
        self.__answer_scores.remove(answer_score)

    # 热词评分，先找处问题中词频最高的词，然后找出离这个词最近的候选答案，候选答案的分值翻倍
    def hot_score(self, question1, evidence1, candidate_answer_collection):
        mini_distance = 10000
        best_candidate_answer = CandidateAnswer()
        evidence_words = evidence1.get_words()
        hot = question1.get_hot()
        if hot is None:
            return None
        hot_term_offes = []
        # 热词的位置数组
        for i in range(len(evidence_words)):
            if hot == evidence_words[i]:
                hot_term_offes.append(i)
        # 候选答案的位置数组
        for candidate_answer in candidate_answer_collection.get_all_candidate_answer():
            candidate_answer_offes = []
            for i in range(len(evidence_words)):
                if evidence_words[i] == candidate_answer.get_answer():
                    candidate_answer_offes.append(i)
            #        计算热词和候选答案的最近距离
            for candidate_answer_off in candidate_answer_offes:
                for hot_term_off in hot_term_offes:
                    abs_value = abs(candidate_answer_off - hot_term_off)
                    if mini_distance > abs_value:
                        mini_distance = abs_value
                        best_candidate_answer = candidate_answer
        if best_candidate_answer is not None and mini_distance > 0:
            score = best_candidate_answer.get_score()
            score *= self.__hot_weight
            best_candidate_answer.add_score(score)

    # 词频评分组件，title中出现一次算title_weight次 snippet出现一次算一次 候选答案的分值+=词频×权重
    def term_frequency_score(self, question1, evidence1, candidate_answer_collection):
        title_list = evidence1.get_title_words()
        snippet_list = evidence1.get_snippet_words()
        for candidate_answer in candidate_answer_collection.get_all_candidate_answer():
            ans = candidate_answer.get_answer()
            word_frequency = title_list.count(ans)*2 + snippet_list.count(ans)
            if word_frequency is None:
                logging.debug('没找到候选答案的词频信息')
                continue
            score = word_frequency * self.__term_frequency_weight
            logging.debug('分值')
            candidate_answer.add_score(score)

    # 词距评分组件 分值+=原分值×（1/词距）
    def term_distance_score(self,question1, evidence1, candidate_answer_collection):
        logging.debug('词距评分开始')
        question_terms = question1.get_words()
        evidence_terms = evidence1.get_words()
        for candidate_answer in candidate_answer_collection.get_all_candidate_answer():
            distance = 0
            candidate_answer_offes = []
            for i in range(len(evidence_terms)):
                if candidate_answer.get_answer() == evidence_terms[i]:
                    candidate_answer_offes.append(i)
            for question_term in question_terms:
                question_term_offes = []
                for i in range(len(evidence_terms)):
                    if question_term == evidence_terms[i]:
                        question_term_offes.append(i)
                for candidate_answer_offe in candidate_answer_offes:
                    for question_term_offe in question_term_offes:
                        distance += abs(candidate_answer_offe - question_term_offe)
            score = candidate_answer.get_score()/distance
            score *= self.__term_distance_weight
            candidate_answer.add_score(score)

    # 最小词距评分 分值=原分值×（1/词距）候选答案的距离 = 候选答案和每一个问题词的最小距离之和
    def term_distance_mini_score(self, question1, evidence1, candidate_answer_collection):
        logging.debug('词距评分开始')
        question_terms = question1.get_words()
        evidence_terms = evidence1.get_words()
        for candidate_answer in candidate_answer_collection.get_all_candidate_answer():
            distance = 0
            candidate_answer_offes = []
            for i in range(len(evidence_terms)):
                if candidate_answer.get_answer() == evidence_terms[i]:
                    candidate_answer_offes.append(i)
            for question_term in question_terms:
                question_term_offes = []
                for i in range(len(evidence_terms)):
                    if question_term == evidence_terms[i]:
                        question_term_offes.append(i)
                mini_distance = 10000
                for candidate_answer_offe in candidate_answer_offes:
                    for question_term_offe in question_term_offes:
                        abs_distance = abs(candidate_answer_offe - question_term_offe)
                        if mini_distance > abs_distance:
                            mini_distance = abs_distance
                    if mini_distance != 10000:
                        distance += mini_distance
            score = candidate_answer.get_score()/distance
            score *= self.__term_distance_mini_weight
            candidate_answer.add_score(score)

    # 文本对齐评分
    def textual_align_score(self, question1, evidence1, candidate_answer_collection):
        logging.debug('文本对齐开始')
        question_terms = question1.get_words()
        question_terms_size = len(question_terms)
        evidence_text = evidence1.get_snippet() + evidence1.get_title()
        for candidate_answer in candidate_answer_collection.get_all_candidate_answer():
            for i in range(question_terms_size):
                textual_align = ''
                for j in range(question_terms_size):
                    if i == j:
                        textual_align += candidate_answer.get_answer()
                    textual_align += question_terms[j]
                if question1.get_question() == textual_align:
                    continue
                textual_align_pattern_terms = WordParser.lcut(textual_align)
                patterns = [textual_align]
                mohu_string = ''
                for t in range(len(textual_align_pattern_terms)):
                    mohu_string += textual_align_pattern_terms[t]
                    if t < len(textual_align_pattern_terms)-1:
                        mohu_string += '.{0,5}'
                patterns.append(mohu_string)
                count = 0
                length = 0
                for pattern in patterns:
                    match_list = re.findall(pattern, evidence_text)
                    count += len(match_list)
                    length += len(''.join(match_list))
                if count > 0:
                    avg_len = length/count
                    question_len = len(question1.get_question())
                    score = question_len/avg_len
                    score *= self.__textual_alignment_weight
                    candidate_answer.add_score(score)

    def score(self, question, evidence, candidate_answer_collection):
        self.term_frequency_score(question, evidence, candidate_answer_collection)
        # self.term_distance_mini_score(question, evidence, candidate_answer_collection)
        # self.term_distance_score(question, evidence, candidate_answer_collection)
        self.textual_align_score(question, evidence, candidate_answer_collection)
        self.hot_score(question, evidence, candidate_answer_collection)
