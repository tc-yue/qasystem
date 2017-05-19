from parser.word_parser import WordParser
from model.questiontype import QuestionType
from model.candidate_answer import CandidateAnswer
from selector.candidate_answer_select import CandidateAnswerSelect
"""
问题有多个证据
证据用于提取候选答案
"""


class Question:
    def __init__(self):
        self.__question = ''
        self.__question_type = QuestionType.Solution
        # 候选问题类型可能有多个
        self.__candidate_question_types = set()
        self.__evidences = []
        self.__expect_answer = ''
        self.__disease = []
        self.__idf_dic = {}

    def set_question(self, question):
        self.__question = question
        # 问题设置疾病症状关键词
        word_pos_list = WordParser.parse(self.__question)
        self.__disease = [i[0] for i in word_pos_list if i[1] == 'nobjectdisease']

    def get_disease(self):
        return self.__disease

    def get_question(self):
        return self.__question

    # 对问题分词获取分词结果
    def get_words(self):
        return WordParser.lcut(self.__question)

    def set_question_type(self, question_type):
        self.__question_type = question_type

    def get_question_type(self):
        return self.__question_type

    def add_candidate_question_type(self, question_type):
        self.__candidate_question_types.add(question_type)

    def remove_candidate_question_type(self, question_type):
        self.__candidate_question_types.remove(question_type)

    def get_candidate_question_types(self):
        return self.__candidate_question_types

    def get_text(self):
        text = ''
        for evidence in self.__evidences:
            text += evidence.get_title() + evidence.get_snippet()
        return text

    def get_evidences(self):
        return self.__evidences

    def add_evidences(self, evidences):
        self.__evidences.extend(evidences)
        self.init_idf()

    def add_evidence(self, evidence):
        self.__evidences.append(evidence)

    def remove_evidence(self, evidence):
        self.__evidences.remove(evidence)

    # 获取证据每个词的idf
    def init_idf(self):
        for evidence in self.__evidences:
            word_set = set(WordParser.lcut(evidence.get_title() + evidence.get_snippet()))
            for item in word_set:
                doc = self.__idf_dic.get(item)
                if doc is None:
                    doc = 1
                else:
                    doc += 1
                self.__idf_dic[item] = doc
        for i in self.__idf_dic.keys():
            self.__idf_dic[i] = 1 / self.__idf_dic[i]

    def get_idf(self):
        return self.__idf_dic

    def get_hot(self):
        question_words = self.get_words()
        hot_dict = {}
        words = WordParser.lcut(self.get_text())
        for word in set(words):
            hot_dict[word] = words.count(word)
        question_dict = {}
        for question_word in question_words:
            count = hot_dict.get(question_word)
            if count is not None and len(question_word) > 1:
                question_dict[question_word] = count
        question_list = [(v[1], v[0]) for v in question_dict.items()]
        return sorted(question_list, reverse=True)[0][1]

    def get_expect_answer(self):
        return self.__expect_answer

    def set_expect_answer(self, expect_answer):
        self.__expect_answer = expect_answer

    # 获取所有候选答案
    def get_all_candidate_answer(self):
        dict1 = {}
        for evidence in self.__evidences:
            for candidate_answer in evidence.get_candidate_answer_collection().get_all_candidate_answer():
                score = dict1.get(candidate_answer.get_answer())
                # 候选答案的分值用于计算最终候选答案分值
                candidate_answer_final_score = candidate_answer.get_score() + evidence.get_score()
                if score is None:
                    score = candidate_answer_final_score
                else:
                    score += candidate_answer_final_score
                dict1[candidate_answer.get_answer()] = score
        candidate_answers = []
        for entry in dict1.items():
            answer = entry[0]
            score = entry[1]
            if answer is not None and score is not None and score > 0:
                if score < 100000:
                    candidate_answer = CandidateAnswer()
                    candidate_answer.set_answer(answer)
                    candidate_answer.set_score(score)
                    candidate_answers.append(candidate_answer)
        candidate_answers = sorted(candidate_answers, key=lambda ans: ans.get_score(), reverse=True)
        if candidate_answers is not None:
            candidate_answers = CandidateAnswerSelect.candidate_answer_filter(self.get_question(), candidate_answers)
        if len(candidate_answers) > 0:
            base_score = candidate_answers[0].get_score()
            for candidate_answer in candidate_answers:
                score = candidate_answer.get_score()/base_score
                candidate_answer.set_score(score)
        return candidate_answers

    # 获取topN候选答案
    def get_topn_candidate_answer(self, topn):
        topn_candidate_answers = []
        all_candidate_answers = self.get_all_candidate_answer()
        if topn > len(all_candidate_answers):
            topn = len(all_candidate_answers)
        for i in range(len(topn)):
            topn_candidate_answers.append(all_candidate_answers[i])
        return topn_candidate_answers
if __name__ == '__main__':
    q = Question()
    q.set_question('头疼怎么办')
    q.set_question_type(QuestionType.Doctor)
    print(q.get_question_type())
