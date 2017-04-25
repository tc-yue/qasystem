import jieba.posseg
import requests
from parser.LTML import LTML

arg = {'api_key':'T8r3Z4d4PkDpzysjWVLG4GPmguFTthFSKeapPlhk', 'text': '头疼全身无力怎么办', 'pattern': 'dp', 'format': 'json','xml_input':'true'}


class WordParser:
    def __init__(self, sentence):
        self.sentence = sentence

    def parse(self):
        word_list = []
        for item in jieba.posseg.lcut(self.sentence):
            word_list.append(tuple(item))
        return word_list

    def get_dependencies(self,wordslist):
        print(wordslist)
        ltml=LTML()
        ltml.build_from_words([("这", "r"),("是", "v")])
        xml = ltml.tostring()
        arg['text'] = xml
        return requests.post(url='http://api.ltp-cloud.com/analysis/', data=arg).json()


if __name__ == '__main__':
    b = WordParser('头疼怎么办').parse()

    print(b)

