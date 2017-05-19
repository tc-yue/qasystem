from .question_type_transformer import QuestionTypeTransformer
from model.question import QuestionType
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
                    filename='../qa.log',
                    filemode='w')
"""
模式匹配结果选择器
"""


class PatternMatchResultSelector:
    @staticmethod
    def select(question1, pattern_match_result):
        logging.info('模式匹配结果选择')
        all_pattern_match_result_items = pattern_match_result.get_all_pattern_match_result()
        if all_pattern_match_result_items is None or len(all_pattern_match_result_items) == 0:
            logging.info('所有问题类型模式匹配结果为空')
            return None
        for file in pattern_match_result.get_questiontypepatternfiles_compacttoloose():
            pattern_match_result_items = pattern_match_result.get_pattern_match_result(file)
            if pattern_match_result_items is None or len(pattern_match_result_items) == 0:
                continue
            # 问题类型-匹配次数
            type_dict = {}
            for pattern_match_result_item in pattern_match_result_items:
                type1 = pattern_match_result_item.get_type()
                key = QuestionTypeTransformer.transform(type1)
                value = type_dict.get(key)
                if value is None:
                    value = 1
                else:
                    value += 1
                type_dict[key] = value
            # 对类型的匹配次数排序 entry_s 问题类型-次数
            entry_s = sorted(type_dict.items(), key=lambda d: d[1], reverse=True)
            if len(entry_s) > 1:
                logging.info('\t类型\t选中数目')
                for entry in entry_s:
                    logging.info('\t'+entry[0]+'\t'+entry[1])
                    question1.add_candidate_question_type(entry[0])
                logging.info('对于多个匹配结果，选择匹配类型最多的')
                selected_type = entry_s[0][0]
                question1.set_question_type(selected_type)
                # 候选类型中不包括主类型
                if selected_type in question1.get_candidate_question_types():
                    question1.remove_candidate_question_type(selected_type)
                return question1
            else:
                logging.info('只有一个匹配结果，匹配成功')
                selected_type = entry_s[0][0]
                question1.set_question_type(selected_type)
                return question1
        logging.info('匹配未成功，不能识别问题类型，不能识别的类型统一指定为Solution')
        question1.set_question_type(QuestionType.Solution)
        return question1
