from .question_type_transformer import QuestionTypeTransformer
from model.question import QuestionType
import logging
"""
模式匹配结果选择器
"""


class PatternMatchResultSelector:
    @staticmethod
    def select(question1, pattern_match_result):
        all_pattern_match_result_items = pattern_match_result.get_all_pattern_match_result()
        if all_pattern_match_result_items is None or len(all_pattern_match_result_items) == 0:
            logging.info('所有问题类型模式匹配结果为空')
            return None
        for file in pattern_match_result.get_questiontypepatternfiles_compacttoloose():
            pattern_match_result_items = pattern_match_result.get_pattern_match_result(file)
            if pattern_match_result_items is None:
                continue
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
            entry_s = sorted(type_dict.items(), key=lambda d: d[1], reverse=True)
            if len(entry_s) > 1:
                for entry in entry_s:
                    question1.add_candidate_question_type(entry[0])
                selected_type = entry_s[0][0]
                question1.set_question_type(selected_type)
                if selected_type in question1.get_candidate_question_types():
                    question1.remove_candidate_question_type(selected_type)
                return question1
            else:
                selected_type = entry_s[0][0]
                question1.set_question_type(selected_type)
                return question1
        question1.set_question_type(QuestionType.Solution)
        return question1
