import re
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
                    filename='../qa.log',
                    filemode='w')
"""
组合证据评分组件对证据评分：
二元模型bigram 构造出问题的所有正则表达式 在证据中进行匹配
"""


class EvidenceScore:
    def __init__(self, weight_list=(1, 1, 1)):
        # 初始化评分权重，evidence list
        self.__evidence_scores = []
        self.term_weight = weight_list[0]
        self.bigram_weight = weight_list[1]
        self.skip_weight = weight_list[2]

    def set_score_weight(self, weight_list):
        self.term_weight = weight_list[0]
        self.bigram_weight = weight_list[1]
        self.skip_weight = weight_list[2]

    # evidence Evidence实例
    def bigram_score(self, question1, evidence1):
        logging.debug('evidence二元评分开始')
        question_terms = question1.get_words()
        patterns = []
        for i in range(len(question_terms)-1):
            pattern = question_terms[i] + question_terms[i + 1]
            patterns.append(pattern)
        score = 0
        for pattern in patterns:
            count = self.count_bigram(evidence1.get_title() + evidence1.get_snippet(), pattern)
            if count > 0:
                score += count * 2
        score *= self.bigram_weight
        logging.debug('evidence 二元评分:' + str(score))
        evidence1.add_score(score)

    def term_score(self, question1, evidence1, idf_dict):
        logging.debug('evidence term评分开始')
        question_terms = question1.get_words()
        title_terms = evidence1.get_title_words()
        snippet_terms = evidence1.get_snippet_words()
        score = 0
        for question_term in question_terms:
            if len(question_term) < 2:
                logging.debug('忽略问题中长度为一的词' + question_term)
                continue
            idf = idf_dict[question_term]
            if idf > 0:
                idf = 1 / idf
            else:
                idf = 1
            for title_term in title_terms:
                if question_term == title_term:
                    score += idf * 2
            for snippet_term in snippet_terms:
                if question_term == snippet_term:
                    score += idf
        score *= self.term_weight
        logging.debug('term 评分结束')
        evidence1.add_score(score)

    def skip_score(self, question1, evidence1):
        logging.debug('evidence skip二元评分开始')
        question_terms = question1.get_words()
        patterns = []
        for i in range(len(question_terms) - 1):
            pattern = question_terms[i] + '.' + question_terms[i + 1]
            patterns.append(pattern)
        score = 0
        for pattern in patterns:
            count = self.count_skip_bigram(evidence1.get_title() + evidence1.get_snippet(), pattern)
            if count > 0:
                score += count * 2
        score *= self.bigram_weight
        logging.debug('evidence skip二元评分:' + str(score))
        return score

    @staticmethod
    def count_bigram(text, pattern):
        count = 0
        index = -1
        while True:
            index = text.find(pattern, index + 1)
            if index > -1:
                count += 1
            else:
                break
        return count

    @staticmethod
    def count_skip_bigram(text, pattern):
        return len(re.findall(pattern, text))

    def score(self, question1, evidence1):
        idf_dict = question1.init_idf()
        self.bigram_score(question1, evidence1)
        self.term_score(question1, evidence1,idf_dict)
        self.skip_score(question1, evidence1)

if __name__ == '__main__':
    a = EvidenceScore()
    b = EvidenceScore()
