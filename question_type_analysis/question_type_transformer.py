from model.questiontype import QuestionType


# Question type string to type enum
class QuestionTypeTransformer:

    @staticmethod
    def transform(question_type):
        if 'Medicine' in question_type:
            return QuestionType.Medicine
        elif 'Price' in question_type:
            return QuestionType.Price
        elif 'Hospital' in question_type:
            return QuestionType.Hospital
        elif 'Doctor' in question_type:
            return QuestionType.Doctor
        elif 'Solution' in question_type:
            return QuestionType.Solution

        else:
            return QuestionType.Solution


if __name__ == '__main__':
    # q = Questiontype.Person_name
    print(QuestionTypeTransformer.transform('Doctor->Multi5'))
