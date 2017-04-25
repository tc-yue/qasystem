class QuestionTypePatternFile:
    def __init__(self):
        self.multi_match = True
        self.file = ''

    def get_file(self):
        return self.file

    def set_file(self, file):
        self.file = file

    def is_multi_match(self):
        return self.multi_match

    def set_multi_match(self, multi_match):
        self.multi_match = multi_match

    def hash_code(self):
        pass

    def equals(self, obj):
        pass
