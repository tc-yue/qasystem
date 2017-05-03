from model.questiontype import QuestionType
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
                    filename='../qa.log',
                    filemode='w')


# Question type string to type enum
class QuestionTypeTransformer:

    @staticmethod
    def transform(question_type):
        logging.debug('问题类型转换' + str(question_type))
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
            logging.error('问题类型转换失败，默认solution' + str(question_type))
            return QuestionType.Solution


if __name__ == '__main__':
    # q = Questiontype.Person_name
    print(QuestionTypeTransformer.transform('Doctor->Multi5'))
