import os
import re
import logging
from model.question import Question
from parser.word_parser import WordParser
from parser.ltp_denpendency_parsing import LtpDependencyParsing
from question_type_analysis.question_pattern import QuestionPattern
from question_type_analysis.pattern_match_result import PatternMatchResult
from question_type_analysis.pattern_match_strategy import PatternMatchStrategy
from question_type_analysis.pattern_match_result_item import PatternMatchResultItem
from question_type_analysis.question_type_pattern_file import QuestionTypePatternFile
from question_type_analysis.pattern_match_result_selector import PatternMatchResultSelector
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
                    filename='../qa.log',
                    filemode='w')
"""
模式匹配判断类型
5种方式 和问题，词和词性，词性，主干词和词性，主干词性 匹配
"""


class PatternBasedMultiLevelQuestionClassifier:

    def __init__(self, pattern_match_strategy1, pattern_match_result_selector1):
        self.__question_pattern_cache = {}
        self.__question_type_pattern_cache = {}
        self.__question_type_pattern_files = []
        self.__pattern_match_strategy = pattern_match_strategy1
        self.__pattern_match_result_selector = pattern_match_result_selector1
        file_path = os.path.abspath(os.path.dirname(__file__)+os.path.sep+os.pardir) + '/files/questionTypePattern'
        for item in sorted(os.listdir(file_path)):
            logging.info('\t模式文件'+item)
            attr = item.split('_')
            file = QuestionTypePatternFile()
            file.set_file(item)
            if 'true' in attr[1]:
                multi_match = True
            else:
                multi_match = False
            file.set_multi_match(multi_match)
            self.__question_type_pattern_files.append(file)

    def classify(self, q):
        question_str = q.get_question()
        pattern_match_strategy1 = self.get_pattern_match_strategy()
        question_patterns = self.extract_pattern_from_question(question_str, pattern_match_strategy1)
        if len(question_patterns) == 0:
            print('extract failed')
            return q
        pattern_match_result = PatternMatchResult()
        for qtpfile in self.__question_type_pattern_files:
            question_type_pattern_file1 = qtpfile.get_file()
            print(qtpfile.get_file())
            question_type_pattern1 = self.extract_question_type_pattern(question_type_pattern_file1)
            if question_type_pattern1 is not None:
                pattern_match_result_items = self.get_pattern_match_result_items(question_patterns, question_type_pattern1)
                if len(pattern_match_result_items) == 0:
                    print('在问题类型模式中未找到匹配项')
                else:
                    pattern_match_result.add_pattern_match_result(qtpfile,pattern_match_result_items)
        pattern_match_result_items = pattern_match_result.get_all_pattern_match_result()
        if len(pattern_match_result_items) == 0:
            print('无匹配')
            return q
        if len(pattern_match_result_items) > 1:
            i = 1
            for item in pattern_match_result_items:
                print('序号'+str(i))
                print('\t问题'+item.get_origin())
                print('\t模式' + item.get_pattern())
                print('\t分类'+item.get_type())
                i += 1
        for file in pattern_match_result.get_questiontypepatternfiles_compacttoloose():
            print(file.get_file()+'是否允许多匹配')
            i = 1
            for item in pattern_match_result.get_pattern_match_result(file):
                print('序号'+str(i))
                print('\t问题'+item.get_origin())
                print('\t模式' + item.get_pattern())
                print('\t分类'+item.get_type())
                i += 1
        return PatternMatchResultSelector.select(q, pattern_match_result)

    def get_pattern_match_strategy(self):
        return self.__pattern_match_strategy

    def set_pattern_match_strategy(self, pattern_match_strategy1):
        self.__pattern_match_strategy = pattern_match_strategy1

    def get_pattern_match_result_selector(self):
        return self.__pattern_match_result_selector

    def set_pattern_match_result_selector(self, pattern_match_result_selector1):
        self.__pattern_match_result_selector = pattern_match_result_selector1

    # 抽取问题的模式
    def extract_pattern_from_question(self, question1, pattern_match_strategy1):
        question_patterns = []
        question1 = question1.strip()
        if pattern_match_strategy1.enable_question_pattern(QuestionPattern.Question):
            question_patterns.append(question1)
        if pattern_match_strategy1.enable_question_pattern(QuestionPattern.TermWithNatures) or \
                pattern_match_strategy1.enable_question_pattern(QuestionPattern.Natures):
            term_with_nature = self.__question_pattern_cache.get(
                question1 + 'term_with_natures')
            nature = self.__question_pattern_cache.get(question1 + 'nature')
            if term_with_nature is None or nature is None:
                words = WordParser.parse(question1)
                term_with_nature_str = ''
                nature_str = ''
                i = 0
                for word in words:
                    term_with_nature_str += word[0] + '/' + word[1] + ' '
                    if i > 0:
                        nature_str += '/'
                    i += 1
                    nature_str += word[1]
                self.__question_pattern_cache[question1 + 'term_with_nature'] = term_with_nature_str
                self.__question_pattern_cache[question1 + 'nature'] = nature_str
                question_patterns.append(term_with_nature_str)
                question_patterns.append(nature_str)
        response = LtpDependencyParsing.get_dp_json(question1)
        try:
            dp_data = response.json()
            question1 = LtpDependencyParsing.get_main_part(dp_data)
            if pattern_match_strategy1.enable_question_pattern(QuestionPattern.MainPartNaturePattern) or \
                    pattern_match_strategy1.enable_question_pattern(QuestionPattern.MainPartPattern):
                mpnp = self.__question_pattern_cache.get(question1 + 'mainpnp')
                mpp = self.__question_pattern_cache.get(question1 + 'mainpp')
                if mpnp is None or mpp is None:
                    words = WordParser.parse(question1)
                    mpp_str = ''
                    mpnp_str = ''
                    i = 0
                    for word in words:
                        mpp_str += word[0] + '/' + word[1] + ' '
                        if i > 0:
                            mpnp_str += '/'
                        i += 1
                        mpnp_str += word[1]
                    self.__question_pattern_cache[question1 + 'mainpnp'] = mpnp_str
                    self.__question_pattern_cache[question1 + 'mainpp'] = mpp_str
                    question_patterns.append(mpnp_str)
                    question_patterns.append(mpp_str)
        except Exception as e:
            logging.error('main_part failed')
            logging.error(e)
        print(question_patterns)
        return question_patterns

    def extract_question_type_pattern(self, question_type_pattern_file1):
        value = self.__question_pattern_cache.get(question_type_pattern_file1)
        if value is not None:
            return value
        types = []
        patterns = []
        with open(os.path.abspath(os.path.dirname(__file__)+os.path.sep+os.pardir)+'/files/questionTypePattern/'+question_type_pattern_file1, 'r') as f:
            lines = f.readlines()
            try:
                for line in lines:
                    types.append(line.split(' ')[0])
                    patterns.append(line.split(' ')[1].replace('\n', ''))
            except Exception as e:
                logging.error(e)
        question_type_pattern = QuestionTypePattern()
        question_type_pattern.set_patterns(patterns)
        question_type_pattern.set_types(types)
        self.__question_type_pattern_cache[question_type_pattern_file1] = question_type_pattern
        return question_type_pattern

    # 获取模式匹配项
    @staticmethod
    def get_pattern_match_result_items(question_patterns, question_type_pattern):
        if question_patterns is None or len(question_patterns) == 0:
            return None
        if question_type_pattern is None or len(question_type_pattern.get_patterns()) == 0:
            return None
        pattern_match_result_items = []
        patterns = question_type_pattern.get_patterns()
        types = question_type_pattern.get_types()
        p_length = len(patterns)
        for i in range(p_length):
            pattern = patterns[i]
            for question_pattern in question_patterns:
                m = re.search(pattern, question_pattern)
                if m:
                    item = PatternMatchResultItem()
                    item.set_origin(question_pattern)
                    item.set_pattern(pattern)
                    item.set_type(types[i])
                    pattern_match_result_items.append(item)
        return pattern_match_result_items

"""
问题类型模式
指定问题类型和问题模式的关系
"""


class QuestionTypePattern:
    def __init__(self):
        # 所有问题类型
        self.types = []
        # 所有问题模式
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
    pattern_match_strategy = PatternMatchStrategy()
    pattern_match_strategy.add_question_pattern(QuestionPattern.Question)
    pattern_match_strategy.add_question_pattern(QuestionPattern.TermWithNatures)
    pattern_match_strategy.add_question_pattern(QuestionPattern.Natures)
    pattern_match_strategy.add_question_pattern(QuestionPattern.MainPartPattern)
    pattern_match_strategy.add_question_pattern(QuestionPattern.MainPartNaturePattern)
    pattern_match_strategy.add_question_type_pattern_files('QuestionTypePatternLevel1_true.txt')
    pattern_match_strategy.add_question_type_pattern_files('QuestionTypePatternLevel2_true.txt')
    pattern_match_strategy.add_question_type_pattern_files('QuestionTypePatternLevel3_true.txt')
    pattern_match_result_selector = PatternMatchResultSelector()
    question_classifier = PatternBasedMultiLevelQuestionClassifier(pattern_match_strategy, pattern_match_result_selector)
    # a = question_classifier.extract_pattern_from_question('早上头疼怎么办', pattern_match_strategy)

    while True:
        input_flag = input('继续 a  退出 b\n')
        if input_flag == 'a':
            input_question = input('input question\n')
            question = Question()
            question.set_question(input_question)
            question = question_classifier.classify(question)
            print(question.get_question_type())
        elif input_flag == 'b':
            break




