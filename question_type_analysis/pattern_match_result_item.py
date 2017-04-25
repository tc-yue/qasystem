# 模式匹配结果项
class PatternMatchResultItem:
    def __init__(self):
        self.type1 = ''
        self.origin = ''
        self.pattern = ''

    def get_type(self):
        return self.type1

    def set_type(self, type1):
        self.type1 = type1

    def get_origin(self):
        return self.origin

    def set_origin(self, origin):
        self.origin = origin

    def get_pattern(self):
        return self.pattern

    def set_pattern(self, pattern):
        self.pattern = pattern



