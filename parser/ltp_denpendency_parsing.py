import requests


class LtpDependencyParsing:
    arg = {
        'api_key': 'T8r3Z4d4PkDpzysjWVLG4GPmguFTthFSKeapPlhk',
        'text': '',
        'pattern': 'dp',
        'format': 'json'
    }

    def __init__(self, sentence):
        self.sentence = sentence

    def get_dp_json(self):
        self.arg['text'] = self.sentence
        return requests.post(url='http://api.ltp-cloud.com/analysis/', data=self.arg).json()

    def get_dp_plain(self):
        self.arg['text'] = self.sentence
        self.arg['format'] = 'plain'
        return requests.post(url='http://api.ltp-cloud.com/analysis/', data=self.arg).content.decode()
if __name__ == '__main__':
    print(LtpDependencyParsing('头疼吃什么药好得快').get_dp_plain())
