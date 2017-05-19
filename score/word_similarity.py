import sqlite3
import math
import os
"""
论文：基于同义词词林的词语相似度计算方法
github：TongYiCiCILin
"""


class WordSimilarity:
    # 常数参数
    def __init__(self):
        self.__a = 0.65
        self.__b = 0.8
        self.__c = 0.9
        self.__d = 0.96
        self.__e = 0.5
        self.__f = 0.1

    # 获取词的编码
    @staticmethod
    def get_encode(word1, word2):
        conn = sqlite3.connect(os.path.abspath(os.path.dirname(__file__)+os.path.sep+os.pardir)+'/files/cilin/cilin.db')
        cursor = conn.cursor()
        cursor.execute("select * from CILIN where word = ?", (word1,))
        results1 = cursor.fetchall()
        cursor.execute("select * from CILIN where word = ?", (word2,))
        results2 = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()
        return [i[1] for i in results1], [i[1] for i in results2]

    # 相似度计算
    def get_similarity(self, word1, word2):
        encode1, encode2 = self.get_encode(word1, word2)
        # 如果词没有编码 ，则相似度为0
        if len(encode1) == 0 or len(encode2) == 0:
            return 0
        max_value = 0
        pi = math.pi
        for e1 in encode1:
            for e2 in encode2:
                common_str = self.get_common_str(e1, e2)
                length = len(common_str)
                k = self.get_k(e1,e2)
                n = self.get_n(common_str)
                res = 0
                # 如果有一个以'@'结尾，那么表示自我封闭，肯定不再一棵树上，直接返回f
                if e1[-1] == '@' or e2[-1] == '@' or 0 ==length:
                    if self.__f > max_value:
                        max_value = self.__f
                    continue
                if length == 1:
                    res = self.__a * math.cos(n*pi/180)*((n-k+1)/n)
                elif length == 2:
                    res = self.__b * math.cos(n*pi/180)*((n-k+1)/n)
                elif length == 4:
                    res = self.__c * math.cos(n*pi/180)*((n-k+1)/n)
                elif length == 5:
                    res = self.__d * math.cos(n*pi/180)*((n-k+1)/n)
                else:
                    if e1[-1] == '=' and e2[-1] == '=':
                        res = 1
                    elif e1[-1] == '#' and e2[-1] == '#':
                        res = self.__e
                if res > max_value:
                    max_value = res

        return max_value

    # 获取编码公共子串
    @staticmethod
    def get_common_str(encode1, encode2):
        sb = ''
        for i in range(8):
            if encode1[i] == encode2[i]:
                sb += encode1[i]
            else:
                break
        if len(sb) == 3 or len(sb)==6:
            sb = sb[:-1]
        return sb

    # 计算所在分支层分支数目
    @staticmethod
    def get_n(encode_head):
        conn = sqlite3.connect(os.path.abspath(os.path.dirname(__file__)+os.path.sep+os.pardir)+'/files/cilin/cilin.db')
        cursor = conn.cursor()
        length = len(encode_head)
        cursor.execute("select * from CILIN where labels like ?", [encode_head+'%'])
        results = cursor.fetchall()
        if length == 1:
            count = len(set(([i[1][0:2] for i in results])))
        elif length == 2:
            count = len(set(([i[1][0:4] for i in results])))
        elif length == 4:
            count = len(set(([i[1][0:5] for i in results])))
        elif length == 5:
            count = len(set(([i[1][0:7] for i in results])))
        else:
            count = 0
        cursor.close()
        conn.commit()
        conn.close()
        return count

    """两个编码对应的分支间的距离"""
    @staticmethod
    def get_k(encode1, encode2):
        temp1 = encode1[0]
        temp2 = encode2[0]
        if temp1 == temp2:
            temp1 = encode1[1]
            temp2 = encode2[1]
        else:
            return abs(ord(temp1)-ord(temp2))
        if temp1 == temp2:
            temp1 = encode1[2:4]
            temp2 = encode2[2:4]
        else:
            return abs(ord(temp1)-ord(temp2))
        if temp1 == temp2:
            temp1 = encode1[4]
            temp2 = encode2[4]
        else:
            return abs(int(temp1)-int(temp2))
        if temp1 == temp2:
            temp1 = encode1[5:7]
            temp2 = encode2[5:7]
        else:
            return abs(ord(temp1)-ord(temp2))
        return abs(int(temp1)-int(temp2))


if __name__ == '__main__':
    print(WordSimilarity().get_similarity('骄傲', '仔细'))






















