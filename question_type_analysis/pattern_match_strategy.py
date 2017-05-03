from question_type_analysis import question_pattern


class PatternMatchStrategy:
    def __init__(self):
        self.__question_type_pattern_files = []
        self.__question_patterns = []

    def add_question_type_pattern_files(self, question_type_file):
        self.__question_type_pattern_files.append(question_type_file)

    def add_question_pattern(self, question_onepattern):
        self.__question_patterns.append(question_onepattern)

    def enable_question_type_pattern_file(self, question_type_pattern_file):
        if question_type_pattern_file in self.__question_type_pattern_files:
            return True
        else:
            return False

    def enable_question_pattern(self, question_onepattern):
        if question_onepattern in self.__question_patterns:
            return True
        else:
            return False

    def get_strategy_des(self):
        string = ''
        for question_type_pattern_file in self.__question_type_pattern_files:
            string = string+question_type_pattern_file+':'
        for question_onepattern in self.__question_patterns:
            string = string+str(question_onepattern)+':'
        return string
if __name__ == '__main__':
    pattern_match_strategy = PatternMatchStrategy()
    pattern_match_strategy.add_question_pattern(question_pattern.QuestionPattern.Question)
    pattern_match_strategy.add_question_pattern(question_pattern.QuestionPattern.TermWithNatures)
    pattern_match_strategy.add_question_pattern(question_pattern.QuestionPattern.Natures)
    pattern_match_strategy.add_question_type_pattern_files('QuestionTypePatternsLevel1_true.txt')
    pattern_match_strategy.add_question_type_pattern_files('QuestionTypePatternsLevel2_true.txt')
    pattern_match_strategy.add_question_type_pattern_files('QuestionTypePatternsLevel3_true.txt')
    print(pattern_match_strategy.get_strategy_des())

