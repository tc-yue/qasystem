import jieba
import jieba.posseg


class WordParser:
    jieba.load_userdict('../files/dic/jieba_pos.txt')

    @staticmethod
    def parse(sentence):
        word_list = []
        for item in jieba.posseg.lcut(sentence):
            word_list.append(tuple(item))
        return word_list

    @staticmethod
    def lcut(sentence):
        return jieba.lcut(sentence)

if __name__ == '__main__':
    b = WordParser.parse('请您给介绍几味适合我吃的医生')
    print(b)

