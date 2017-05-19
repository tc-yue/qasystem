from enum import Enum,unique
"""
问题类型
"""


@unique
class QuestionType(Enum):
    Null = 'unknown'
    Medicine = 'medicine'
    # 适应症,禁忌,用法,不良反应
    Indications = 'indications'
    # Contraindications = 'contraindications'
    # Dosage = 'dosage'
    # Adversereactions = 'adversereactions'
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
        elif QuestionType.Medicine == self:
            pos = 'nmediciennmae'
        elif QuestionType.Price == self:
            pos = 'm'
        elif QuestionType.Hospital == self:
            pos = 'nt'
        elif QuestionType.Solution == self:
            pos = 'n'
        elif QuestionType.Indications == self:
            pos = 'n'
        return pos

if __name__ == '__main__':
    type1 = QuestionType.Doctor
    print(type1)
    print(type1.get_pos())
    a = QuestionType(QuestionType.Doctor)
    print(a.get_des())

