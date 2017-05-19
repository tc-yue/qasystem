from model.candidate_answer import CandidateAnswer
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
                    filename='../qa.log',
                    filemode='w')
"""
候选答案集合
包含多个候选答案
"""


class CandidateAnswerCollection:

    def __init__(self):
        # 元素类型CandidateAnswer的实例
        self.__candidate_answers = []

    def is_empty(self):
        if self.__candidate_answers:
            return True
        else:
            return False

    def get_all_candidate_answer(self):
        # 按候选答案分值排序
        return sorted(self.__candidate_answers, key=lambda ans: ans.get_score(), reverse=True)

    def show_all(self):
        for candidate_answer in self.get_all_candidate_answer():
            logging.debug(candidate_answer.get_answer() + '' + str(candidate_answer.get_score()))

    def get_topn_candidate_answer(self, topn):
        # 按分值排序返回topN
        result = []
        candidate_answers = self.get_all_candidate_answer()
        length = len(candidate_answers)
        if topn > length:
            topn = length
        for i in range(topn):
            result.append(candidate_answers[i])
        return result

    def show_topn(self, topn):
        for candidate_answer in self.get_topn_candidate_answer(topn):
            logging.debug(candidate_answer.get_answer()+' '+str(candidate_answer.get_score()))

    def add_answer(self, candidate_answer):
        """

        :type candidate_answer: CandidateAnswer
        """
        if candidate_answer not in self.__candidate_answers:
            self.__candidate_answers.append(candidate_answer)

    def remove_answer(self, candidate_answer):
        self.__candidate_answers.remove(candidate_answer)

if __name__ == '__main__':
    a = CandidateAnswer()
    a.set_answer('10asd')
    a.set_score(10)
    b = CandidateAnswer()
    b.set_score(5)
    b.set_answer('5asd')
    c = CandidateAnswer()
    c.set_score(8)
    c.set_answer('8asd')
    col = CandidateAnswerCollection()
    col.add_answer(a)
    col.add_answer(b)
    col.add_answer(c)
    col.show_topn(2)

