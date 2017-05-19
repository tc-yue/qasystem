"""
合工大 问句相似度研究算法实现
"""
from model.questiontype import QuestionType
from score.word_similarity import WordSimilarity


class SentenceSimilarity:
    def __init__(self):
        # 初始化评分权重
        self.__scores = 0.0
        self.__syntax_scores = 0.0
        self.__class_weight = 0.2
        self.__key_weight = 0.3
        self.__syntax_weight = 0.2
        self.__semantic_weight = 0.5
        self.__order_weight = 0.1
        self.__len_weight = 0.1
        self.__word_weight = 0.7
        self.__dis_weight = 0.1

    def set_score_weight(self, weight_list):
        self.__syntax_scores = weight_list[0]
        self.__order_weight = 0.1
        self.__len_weight = 0.1
        self.__word_weight = 0.7
        self.__dis_weight = 0.1

    def get_score(self):
        return self.__scores

    # param 问题的分词list 词形相似度，用两个问句中含有共同词的个数来衡量
    def word_sim(self, question1, question2):
        intersection_words = [w for w in question1 if w in question2]
        same_count = 0
        for i in intersection_words:
            a = question1.count(i)
            b = question2.count(i)
            if a >= b:
                same_count += b
            else:
                same_count += a
        score = 2*same_count/(len(question1)+len(question2))
        self.__syntax_scores += self.__word_weight * score

    # 词序相似度
    def order_sim(self, question1, question2):
        intersection_words = [w for w in question1 if w in question2
                              and question1.count(w) == 1 and question2.count(w)]
        if len(intersection_words) <= 1:
            score = 0
        else:
            pfirst = sorted([question1.index(i) for i in intersection_words])
            psecond = [question2.index(question1[i]) for i in pfirst]
            count = 0
            for i in range(len(psecond)-1):
                if psecond[i] < psecond[i+1]:
                    count += 1
            score = 1 - count/(len(intersection_words)-1)
        self.__syntax_scores += self.__order_weight * score

    # 句子长度相似度
    def len_sim(self, question1, question2):
        score = 1 - abs((len(question1)-len(question2))/(len(question1)+len(question2)))
        self.__syntax_scores += self.__order_weight*score

    # 语义方法
    def semantic_sim(self, question1, question2):
        n = len(question1)
        m = len(question2)
        score1 = 0.0
        for i in range(n):
        # question1中每个词与2中每个词最相似
            score1 += max(WordSimilarity().get_similarity(question1[i], question2[j]) for j in range(m))
        score1 /= (2*n)
        score2 = 0.0
        for j in range(m):
            score2 += max(WordSimilarity().get_similarity(question1[i], question2[j]) for i in range(n))
        score2 /= (2*n)
        self.__scores += self.__semantic_weight * (score1+score2)

    # 问题类型
    def class_sim(self, question_type1, question_type2):
        if question_type1 == question_type2:
            score = 1
        elif question_type1 is QuestionType.Solution or question_type2 is QuestionType.Solution:
            score = 0.5
        else:
            score = 0
        self.__scores += self.__class_weight * score

    # 关键词
    def key_sim(self,question_a,question_b):
        keya = question_a.get_disease()
        keyb = question_b.get_disease()
        score = 0
        for i in keya:
            if i in keyb:
                score += 1
        if len(keya) > 0:
            self.__scores += self.__key_weight * score / len(keya)

    def combination_sim(self,question_a, question_b):
        """

        :param question_a: 问题类
        :param question_b:
        :param question_type1: 问题类型
        :param question_type2:
        :return:
        """
        question1 = question_a.get_words()
        question2 = question_b.get_words()
        # self.class_sim(question_type1,question_type2)
        self.key_sim(question_a, question_b)
        self.semantic_sim(question1,question2)
        self.word_sim(question1,question2)
        self.len_sim(question1,question2)
        self.order_sim(question1,question2)
        self.__scores += self.__syntax_scores * self.__syntax_weight

if __name__ == '__main__':
    a = SentenceSimilarity()
    # a.combination_sim(['牙疼','怎么','治疗'],['怎么','治疗','牙痛'],QuestionType.Solution,QuestionType.Description)
    print(a.get_score())
