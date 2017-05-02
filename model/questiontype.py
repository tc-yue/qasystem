from enum import Enum,unique
"""
问题类型
"""


@unique
class QuestionType(Enum):
    Null = 'unknown'
    Medicine = 'medicine'
    Price = 'price'
    Hospital = 'hospital'
    Doctor = 'doctor'
    Solution = 'solution'
    Description = 'description'

    def __init__(self, des):
        self.des = des

    def get_des(self):
        return self.des

    def get_pos(self):
        pos = 'unknown'
        if QuestionType.Doctor == self:
            pos = 'nr'
        elif QuestionType.Medicine == self:
            pos = 'nz'
        elif QuestionType.Price == self:
            pos = 'm'
        elif QuestionType.Hospital == self:
            pos = 'nt'
        elif QuestionType.Solution == self:
            pos = 'n'
        return pos

if __name__ == '__main__':
    type1 = QuestionType.Doctor
    print(type1)
    print(type1.get_pos())
    a = QuestionType(QuestionType.Doctor)
    print(a.get_des())

