from question_type_analysis import question_type_transformer
from question_type_analysis import pattern_match_strategy
from question_type_analysis.pattern_match_result_selector import PatternMatchResultSelector
from question_type_analysis import question_type_pattern_file
from question_type_analysis.question_pattern import QuestionPattern
from question_type_analysis.pattern_match_result import PatternMatchResult
from question_type_analysis.pattern_match_result_item import PatternMatchResultItem
from model.question import Question
from parser.word_parser import WordParser
import os
import re


class PatternBasedMultiLevelQuestionClassifier:
    path = '../files/'
    question_pattern_cache = {}
    question_type_pattern_cache = {}
    question_type_pattern_files = []

    def __init__(self, pattern_match_strategy1, pattern_match_result_selector1):
        self.pattern_match_strategy = pattern_match_strategy1
        self.pattern_match_result_selector = pattern_match_result_selector1
        file_path = os.path.dirname(__file__).replace('question_type_analysis', 'files') + '/questionTypePattern'
        for item in sorted(os.listdir(file_path)):
            attr = item.split('_')
            file = question_type_pattern_file.QuestionTypePatternFile()
            file.set_file(item)
            if 'true' in attr[1]:
                multi_match = True
            else:
                multi_match = False
            file.set_multi_match(multi_match)
            PatternBasedMultiLevelQuestionClassifier.question_type_pattern_files.append(file)

    def classify(self, question_str):
        q = Question()
        q.set_question(question_str)
        pattern_match_strategy1 = self.get_pattern_match_strategy()
        question_patterns = self.extract_pattern_from_question(question_str, pattern_match_strategy1)
        if len(question_patterns) == 0:
            print('extract failed')
            return question_str
        pattern_match_result = PatternMatchResult()
        for qtpfile in PatternBasedMultiLevelQuestionClassifier.question_type_pattern_files:
            question_type_pattern_file1 = '/questionTypePatterns' + qtpfile.get_file()
            print(qtpfile.get_file())
            question_type_pattern1 = self.extract_pattern_from_question(question_type_pattern_file1)
            if question_type_pattern_file1 is not None:
                pattern_match_result_items = self.get_pattern_match_result_items(question_patterns,question_type_pattern1)
                if len(pattern_match_result_items) == 0:
                    print('在问题类型模式中未找到匹配项')
                else:
                    pattern_match_result.add_pattern_match_result(qtpfile,pattern_match_result_items)
        pattern_match_result_items = pattern_match_result.get_all_pattern_match_result()
        if len(pattern_match_result_items) == 0:
            print('无匹配')
            return question_str
        if len(pattern_match_result_items) > 1:
            i = 1
            for item in pattern_match_result_items:
                print('xuhao'+i)
                print('\twen'+item.get_origin())
                print('\tmoshi' + item.get_pattern())
                print('\tfenlei'+item.get_type())
                i += 1
        for file in pattern_match_result.get_questiontypepatternfiles_compacttoloose():
            i = 1
            for item in pattern_match_result.get_pattern_match_result(file):
                print('xuhao'+i)
                print('\twen'+item.get_origin())
                print('\tmoshi' + item.get_pattern())
                print('\tfenlei'+item.get_type())
                i += 1
        return self.get_pattern_match_result_selector().select(question_str, pattern_match_result)



    def get_pattern_match_strategy(self):
        return self.pattern_match_strategy

    def set_pattern_match_strategy(self, pattern_match_strategy1):
        self.pattern_match_strategy = pattern_match_strategy1

    def get_pattern_match_result_selector(self):
        return self.pattern_match_result_selector

    def set_pattern_match_result_selector(self, pattern_match_result_selector1):
        self.pattern_match_result_selector = pattern_match_result_selector1

    @staticmethod
    def extract_pattern_from_question(question1, pattern_match_strategy1):
        question_patterns = []
        question1 = question1.strip()
        if pattern_match_strategy1.enable_question_pattern(QuestionPattern.Question):
            question_patterns.append(question1)
        if pattern_match_strategy1.enable_question_pattern(QuestionPattern.TermWithNatures) or \
                pattern_match_strategy1.enable_question_pattern(QuestionPattern.Natures):
            term_with_nature = PatternBasedMultiLevelQuestionClassifier.question_pattern_cache.get(
                question1 + 'termWithNatures')
            nature = PatternBasedMultiLevelQuestionClassifier.question_pattern_cache.get(question1 + 'nature')
            if term_with_nature is None or nature is None:
                words = WordParser(question1).parse()
                term_with_nature_str = ''
                nature_str = ''
                i = 0
                for word in words:
                    term_with_nature_str += word[0] + '/' + word[1] + ' '
                    if i > 0:
                        nature_str += '/'
                    i += 1
                    nature_str += word[1]
                PatternBasedMultiLevelQuestionClassifier.question_pattern_cache[
                    question1 + 'term_with_nature'] = term_with_nature_str
                PatternBasedMultiLevelQuestionClassifier.question_pattern_cache[question1 + 'nature'] = nature_str
                question_patterns.append(term_with_nature_str)
                question_patterns.append(nature_str)
        return question_patterns

    def extract_question_type_pattern(self, question_type_pattern_file1):
        value = self.question_pattern_cache[question_type_pattern_file1]
        if value is not None:
            return value
        types = []
        patterns = []
        with open(question_type_pattern_file1, 'r') as f:
            lines = f.readlines()
            for line in lines:
                types.append(line.split(' ')[0])
                patterns.append(line.split(' ')[1])
        question_type_pattern = QuestionTypePattern()
        question_type_pattern.set_patterns(patterns)
        question_type_pattern.set_types(types)
        self.question_type_pattern_cache[question_type_pattern_file1] = question_type_pattern
        return question_type_pattern

    # 获取模式匹配项
    @staticmethod
    def get_pattern_match_result_items(question_patterns, question_type_pattern):
        if question_patterns is None or len(question_patterns) == 0:
            return None
        if question_type_pattern is None or len(question_type_pattern.get_patterns()) == 0:
            return None
        pattern_match_result_items = []
        patterns = []
        types = []
        p_length = len(patterns)
        for i in range(p_length):
            pattern = patterns[i]
            for question_pattern in question_patterns:
                m = re.match(pattern,question_pattern)
                if m:
                    item = PatternMatchResultItem()
                    item.set_origin(question_pattern)
                    item.set_pattern(pattern)
                    item.set_type(types[i])
                    pattern_match_result_items.append(item)
        return pattern_match_result_items


class QuestionTypePattern:
    def __init__(self):
        self.types = []
        self.patterns = []

    def get_types(self):
        return self.types

    def set_types(self, types):
        self.types = types

    def get_patterns(self):
        return self.patterns

    def set_patterns(self, patterns):
        self.patterns = patterns


if __name__ == '__main__':
    pattern_match_strategy = pattern_match_strategy.PatternMatchStrategy()
    pattern_match_strategy.add_question_pattern(QuestionPattern.Question)
    pattern_match_strategy.add_question_pattern(QuestionPattern.TermWithNatures)
    pattern_match_strategy.add_question_pattern(QuestionPattern.Natures)
    pattern_match_strategy.add_question_type_pattern_files('QuestionTypePatternLevel1_true.txt')
    pattern_match_result_selector = PatternMatchResultSelector()
    question_classifier = PatternBasedMultiLevelQuestionClassifier(pattern_match_strategy,
                                                                   pattern_match_result_selector)
    a = question_classifier.extract_pattern_from_question('头疼怎么办', pattern_match_strategy)
    print(a)


