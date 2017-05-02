"""
候选答案
每一个候选答案都包含答案名称以及分值
"""


class CandidateAnswer:
    def __init__(self):
        self.__answer = ''
        self.__score = 1.0

    def get_answer(self):
        return self.__answer

    def set_answer(self, answer):
        self.__answer = answer

    def get_score(self):
        return self.__score

    def set_score(self, score):
        self.__score = score

    def add_score(self, score):
        self.__score += score

    #     CandidateAnswer 某个实例o
    def compare_to(self, o):
        if 0 is not None and isinstance(o, CandidateAnswer):
            if self.__score < o.__score:
                return -1
            elif self.__score > o.__score:
                return 1
            else:
                return 0

if __name__ == '__main__':
    a = CandidateAnswer()
    a.set_score(10)
    b = CandidateAnswer()
    b.set_score(5)
    print(a.compare_to(b))
