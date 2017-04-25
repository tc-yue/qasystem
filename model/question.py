from parser.word_parser import WordParser
from model.questiontype import QuestionType


class Question:
    def __init__(self):
        self.question = ''
        self.question_type = QuestionType.Solution
        self.candidate_question_types = set()

    def set_question(self, question):
        self.question = question

    @property
    def get_question(self):
        return self.question

    # 对问题分词获取分词结果
    @property
    def get_words(self):
        result = []
        words = WordParser(self.question).parse()
        for word in words:
            result.append(word)
        return result

    def set_question_type(self, question_type):
        self.question_type = question_type

    def get_question_type(self):
        return self.question_type

    def add_candidate_question_type(self, question_type):
        self.candidate_question_types.add(question_type)

    def remove_candidate_question_type(self, question_type):
        self.candidate_question_types.remove(question_type)

    def get_candidate_question_type(self):
        return self.candidate_question_types


if __name__ == '__main__':
    q = Question()
    q.set_question('头疼怎么办')
    q.set_question_type(QuestionType.Person_name)
    print(q.get_question_type())
