from enum import Enum, unique


@unique
class QuestionPattern(Enum):
    # 直接和问题匹配
    Question = 0
    # 词和词性序列匹配
    TermWithNatures = 1
    # 词性序列匹配
    Natures = 2
    # 主干词和词性匹配
    MainPartPattern = 3
    # 主干词性匹配
    MainPartNaturePattern = 4
