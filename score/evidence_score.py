import re
import logging
from score.sentence_similarity import SentenceSimilarity
from model.question import Question
from model.evidence import Evidence
"""
组合证据评分组件对证据评分：
二元模型bigram 构造出问题的所有正则表达式 在证据中进行匹配
跳跃二元模型评分组件 利用跳跃二元模型构造出问题的所有正则表达式 在证据中进行匹配，匹配1次得2分
对证据进行评分 不管语法关系或词序，直接对问题和证据的词进行匹配 对于问题中的词，
在title中出现一次记2/idf分对于问题中的词，在snippet中出现一次记1/idf分
"""


class EvidenceScore:
    def __init__(self, weight_list=(1, 1, 1)):
        # 初始化评分权重，evidence list
        self.term_weight = weight_list[0]
        self.bigram_weight = weight_list[1]
        self.skip_weight = weight_list[2]
        self.similarity_weight = 0.5

    def set_score_weight(self, weight_list):
        self.term_weight = weight_list[0]
        self.bigram_weight = weight_list[1]
        self.skip_weight = weight_list[2]

    def bigram_score(self, question1, evidence1):
        """

        :param question1: Question
        :param evidence1: Evidence
        """
        logging.debug('evidence二元评分开始')
        question_terms = question1.get_words()
        # 利用二元模型构造出问题的所有二元表达式
        patterns = []
        for i in range(len(question_terms)-1):
            pattern = question_terms[i] + question_terms[i + 1]
            patterns.append(pattern)
        score = 0
        # 在证据中寻找模式，命中1个加2分
        for pattern in patterns:
            # 计算二元表达式在证据中出现的次数，出现1次加2分
            count = self.count_bigram(evidence1.get_title() + evidence1.get_snippet(), pattern)
            if count > 0:
                logging.debug("模式: " + pattern + " 在文本中出现 " + str(count) + "次")
                score += count * 2
        score *= self.bigram_weight
        logging.debug('evidence 二元评分:' + str(score))
        evidence1.add_score(score)
        logging.debug('Evidence 二元模型评分结束')

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
            idf = idf_dict.get(question_term)
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
        logging.debug('Evidence TermMatch评分:' + str(score))
        evidence1.add_score(score)
        logging.debug("Evidence TermMatch评分结束")

    def skip_score(self, question1, evidence1):
        logging.debug('evidence skip二元评分开始')
        question_terms = question1.get_words()
        patterns = []
        # 利用跳跃二元模型构造出问题的所有跳跃二元表达式
        for i in range(len(question_terms) - 1):
            pattern = question_terms[i] + '.' + question_terms[i + 1]
            patterns.append(pattern)
        score = 0
        # 在evidence中寻找模式，命中1个加2分
        for pattern in patterns:
            # 计算跳跃二元表达式在证据中出现的次数，出现1次加2分
            count = self.count_skip_bigram(evidence1.get_title() + evidence1.get_snippet(), pattern)
            if count > 0:
                logging.debug("模式: " + pattern + " 在文本中出现 " + str(count) + "次")
                score += count * 2
        score *= self.bigram_weight
        logging.debug('evidence skip二元评分:' + str(score))
        evidence1.add_score(score)
        logging.debug("Evidence 跳跃二元模型评分结束")

    def similarity_score(self,question1,evidence1):
        logging.debug('问句相似度评分开始')
        question_b = Question()
        question_b.set_question(evidence1.get_title())
        a = SentenceSimilarity()
        a.combination_sim(question1, question_b)
        score = a.get_score() * self.similarity_weight
        logging.debug('相似度评分：' + str(score))
        evidence1.add_score(score)

    # 在text中包含pattern数目
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
        idf_dict = question1.get_idf()
        print(idf_dict)
        self.term_score(question1, evidence1,idf_dict)
        self.bigram_score(question1, evidence1)
        self.skip_score(question1, evidence1)
        self.similarity_score(question1,evidence1)

if __name__ == '__main__':
    a = EvidenceScore()
    question = Question()
    question.set_question('早上到现在一直是腹泻怎么办')
    evidence = Evidence()
    evidence.set_snippet('早上起来就一直腹泻，还出血了，怎么办')
    evidence.set_title('建议你去医院治疗，腹泻这种情况还是要牙医治疗')
    evidence2 = Evidence()
    evidence2.set_snippet('早上起来就一直腹泻，还出血了，吃什么药')
    evidence2.set_title('建议你去医院治疗，腹泻这种情况还是要牙医治疗')
    question.add_evidences([evidence, evidence2])
    a.score(question,evidence)
    a.score(question,evidence2)
    print(evidence.get_score())
    print(evidence2.get_score())
