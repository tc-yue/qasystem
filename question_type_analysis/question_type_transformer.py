from model.questiontype import QuestionType


class QuestionTypeTransformer:
    def __init__(self, question_type):
        self.question_type = question_type

    def transform(self):
        if 'Medicine' in self.question_type:
            return QuestionType.Medicine_name
        elif 'Price' in self.question_type:
            return QuestionType.Price
        elif 'Hospital' in self.question_type:
            return QuestionType.Hospital
        elif 'Doctor' in self.question_type:
            return QuestionType.Doctor
        elif 'Solution' in self.question_type:
            return QuestionType.Solution

        else:
            return QuestionType.Solution


if __name__ == '__main__':
    # q = Questiontype.Person_name
    print(QuestionTypeTransformer('Person->Multi5').transform())
