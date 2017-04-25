from enum import Enum,unique

@unique
class QuestionType(Enum):
    Null = '未知'
    Medicine_name = 'medicine'
    Price = 'price'
    Hospital = 'hospital'
    Doctor = 'doctor'
    Solution = 'solution'

    def __init__(self, des):
        self.des = des

    def get_des(self):
        return self.des

    def get_pos(self):
        pos = 'unknown'
        if QuestionType.Doctor == self:
            pos = 'nr'
        elif QuestionType.Medicine_name == self:
            pos = 'nz'
        elif QuestionType.Price == self:
            pos = 'm'
        elif QuestionType.Hospital == self:
            pos = 'nt'
        elif QuestionType.Solution == self:
            pos = 'n'
        return pos

if __name__ == '__main__':
    type1 = QuestionType.Person_name
    print(type1)
    print(type1.get_pos())
    a = QuestionType(QuestionType.Person_name)
    print(a.get_des())

