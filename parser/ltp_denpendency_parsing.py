import requests


"""哈工大api调用"""


class LtpDependencyParsing:
    arg = {
        'api_key': 'T8r3Z4d4PkDpzysjWVLG4GPmguFTthFSKeapPlhk',
        'text': '',
        'pattern': 'dp',
        'format': 'json'
    }
    question_dic = ['多少', '哪', '哪儿', '哪个', '哪里', '哪种', '如何', '什么', '谁',
                    '为什么', '怎么', '怎么样', '怎样', '多久',
                    '多会儿', '啥', '多大', '哪家', '哪些']

    @staticmethod
    def get_dp_json(sentence):
        LtpDependencyParsing.arg['text'] = sentence
        request = requests.post(url='http://api.ltp-cloud.com/analysis/', data=LtpDependencyParsing.arg)
        return request

    @staticmethod
    def get_dp_plain(sentence):
        LtpDependencyParsing.arg['text'] = sentence
        LtpDependencyParsing.arg['format'] = 'plain'
        request = requests.post(url='http://api.ltp-cloud.com/analysis/', data=LtpDependencyParsing.arg)
        return request.content.decode()

    @staticmethod
    def get_main_part(dependency_data):
        dp_list = dependency_data[0][0]
        f_list = []
        for item in dp_list:
            if item['relate'] == 'HED':
                f_list.append(item)
            elif item['relate'] == 'SBV' or item['relate'] == 'VOB':
                f_list.append(item)
                f_list.append(dp_list[item['parent']])
        # 疑问词表item['cont'] in proun_dict ,item['pos'] == 'r'
            elif item['cont'] in LtpDependencyParsing.question_dic:
                f_list.append(item)
                f_list.append(dp_list[item['parent']])
        s_list = sorted(list(set([(i['id'], i['cont']) for i in f_list])))
        return ''.join([i[1]for i in s_list])

if __name__ == '__main__':
    print(LtpDependencyParsing.get_dp_json('头疼吃什么药好得快').json())
    response = LtpDependencyParsing.get_dp_json('早上起来后一直头疼，吃什么药好得快')
    print(response)
    dp_data = response.json()
    print(LtpDependencyParsing.get_main_part(dp_data))
