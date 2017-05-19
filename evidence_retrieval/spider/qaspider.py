import requests
import re
import time


# 以http://club.xywy.com/keshi/1.html 为源头
def spider2(date, size):
    for id1 in range(size):
        url1 = 'http://club.xywy.com/keshi/2017-%s/%d.html' % (date,id1)
        r = requests.get(url=url1)
        html = r.content.decode('gbk', errors='ignore')
        sub_url = re.findall(r'http://club.xywy.com/static/\d+?/\d+?.htm',html)
        for i in sub_url:
            try:
                shtml = requests.get(url=i).content.decode('gbk', errors='ignore')
                question = re.findall(r'<div class="graydeep User_quecol pt10 mt10" id="qdetailc">\s*?(\S*?)\t*?</div>',shtml)
                answer = re.findall(r'<div class="pt15 f14 graydeep  pl20 pr20">(.*?)</div>',shtml)
                data = '\n'.join(question+answer)
                write_data = re.sub(r'(<b>.*?</b>)|(br/)|(<h5>.*?</h5>)','',data)
                if write_data:
                    with open('../qa_data/'+date+'/'+i[-22:-4].replace('/','_')+'.txt','w')as f:
                        f.write(write_data)
            except Exception as e:
                    print(e)
        print(id1)
        time.sleep(0.2)


if __name__ == '__main__':
    spider2('05-13', 710)
