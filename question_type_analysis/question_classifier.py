class QuestionClassifier :
    def __init__(self):
        self.pattern_match_strategy = patternmatch_strategy.PatternMatchStrategy()
    def classify(self, question):
        q = Question()
        q.set_question(question)
        return classify(q)

    def get_pattern_match_strategy(self):
        return
