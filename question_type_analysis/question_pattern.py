from enum import Enum,unique

@unique
class QuestionPattern(Enum):
    Question = 0
    TermWithNatures = 1
    Natures = 2
    MainPartPattern = 3
    MainPartNaturePattern = 4
