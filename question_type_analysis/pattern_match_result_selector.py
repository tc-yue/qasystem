from .question_type_transformer import QuestionTypeTransformer
from .pattern_match_strategy import PatternMatchStrategy
from .pattern_match_result import  PatternMatchResult
from model.question import Question
from model.question import QuestionType
# 模式匹配结果选择器


class PatternMatchResultSelector:
    @staticmethod
    def select(question1, pattern_match_result):
        all_pattern_match_result_items = pattern_match_result.get_all_pattern_match_result()
        if all_pattern_match_result_items is None or len(all_pattern_match_result_items) == 0:
            return None
        for file in pattern_match_result.get_questiontypepatternfiles_compacttoloose():
            pattern_match_result_items = pattern_match_result.get_pattern_match_result(file)
            if pattern_match_result_items is None:
                continue
            type_dict={}
            for pattern_match_result_item in pattern_match_result_items:
                type1 = pattern_match_result_item.get_type()
                key = QuestionTypeTransformer(type1).transform()
                value = type_dict.get(key)
                if value is None:
                    value = 1
                else:
                    value += 1
                type_dict[key] = value
            entrys = sorted(type_dict.items(),key=lambda d:d[1] ,reverse=True)
            if len(entrys) > 1:
                for entry in entrys:
                    question1.add_candidate_question_type(entry[0])
                selected_type = entrys[0][0]
                question1.set_question_type(selected_type)
                if selected_type in question1.get_candidate_question_types()
                    question1.remove_candidate_question_type(selected_type)
                return question1
            else:
                selected_type = entrys[0][0]
                question1.set_question_type(selected_type)
                return question1
        question1.set_question_type(QuestionType.Solution)
        return question1
