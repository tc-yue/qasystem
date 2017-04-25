# 模式匹配结果项
class PatternMatchResultItem:
    def __init__(self):
        self.stype = ''
        self.origin = ''
        self.pattern = ''

    def get_type(self):
        return self.stype

    def set_type(self, stype):
        self.stype = stype

    def get_origin(self):
        return self.origin

    def set_origin(self, origin):
        self.origin = origin

    def get_pattern(self):
        return self.pattern

    def set_pattern(self, pattern):
        self.pattern = pattern



