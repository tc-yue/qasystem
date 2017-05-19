"""通用候选答案提取组件"""
from model.candidate_answer_collection import CandidateAnswerCollection
from model.candidate_answer import CandidateAnswer
from parser.word_parser import WordParser
import logging


class CandidateAnswerSelect:

    @staticmethod
    def common_candidate_answer_select(question, evidence):
        candidate_answer_collection = CandidateAnswerCollection()
        words = WordParser.parse(evidence.get_title() + evidence.get_snippet())
        for word in words:
            if len(word[0]) < 2:
                logging.debug('忽略长度小于2的候选答案'+word[0])
                continue
            #  todo   词性确认需要修改
            if word[1] == question.get_question_type().get_pos():
                answer = CandidateAnswer()
                answer.set_answer(word[0])
                candidate_answer_collection.add_answer(answer)
                logging.debug('成为候选答案： '+word[0])
        evidence.set_candidate_answer_collection(candidate_answer_collection)

    """
    如果候选答案出现在问题中，则过滤
    """

    @staticmethod
    def candidate_answer_filter(question, candidate_answers):
        """

        :param question: Question
        :param candidate_answers: list of CandidateAnswer
        :return: list of CandidateAnswer
        """
        question_words = WordParser.lcut(question)
        string = '对问题分词:'
        for question_word in question_words:
            string += question_word + ' '
        logging.debug(string)
        # 答案不能在问题中
        candidate_answers[:] = [i for i in candidate_answers if i.get_answer() not in question_words]
        return candidate_answers


