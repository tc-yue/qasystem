"""
问题类型模式文件
"""


class QuestionTypePatternFile:
    def __init__(self):
        self.__multi_match = True
        self.__file = ''

    def get_file(self):
        return self.__file

    def set_file(self, file):
        self.__file = file

    def is_multi_match(self):
        return self.__multi_match

    def set_multi_match(self, multi_match):
        self.__multi_match = multi_match
