"""
模式匹配结果项
"""


class PatternMatchResultItem:
    def __init__(self):
        self.__type1 = ''
        self.__origin = ''
        self.__pattern = ''

    def get_type(self):
        return self.__type1

    def set_type(self, type1):
        self.__type1 = type1

    def get_origin(self):
        return self.__origin

    def set_origin(self, origin):
        self.__origin = origin

    def get_pattern(self):
        return self.__pattern

    def set_pattern(self, pattern):
        self.__pattern = pattern



