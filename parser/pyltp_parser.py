from pyltp import Segmentor, Postagger, Parser

class PyLtpParser:

    def __init__(self, sentence):
        self.sentence = sentence

    def get_seg(self):
        segmentor = Segmentor()
        segmentor.load('ltpmodel/cws.model')
        words = segmentor.segment('你怎么了')
        print('\t'.join(words))
        segmentor.release()


    def get_pos(self):
        postagger = Postagger()
        postagger.load('ltpmodel/pos.model')
        postags = postagger.postag(['你','怎么','看'])
        print('\t'.join(postags))
        postagger.release()

    def get_dp(self):
        parser = Parser()
        parser.load('ltpmodel/parser.model')
        words = ['你','怎么','看']
        postags = ['r','r','v']
        arcs = parser.parse(words,postags)
        print('\t'.join("%d:%s" % (arc.head, arc.relation) for arc in arcs))
        parser.release()


if __name__ == '__main__':
    print(PyLtpParser('头疼全身无力怎么办').get_seg())
    PyLtpParser('头疼全身无力怎么办').get_pos()
    PyLtpParser('头疼全身无力怎么办').get_dp()
