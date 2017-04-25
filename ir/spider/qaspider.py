import requests
import re
import time
agent = 'Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0'
headers = {
    "Host": "static.css.xywy.com",
    "Referer": "http://club.xywy.com/list_294_answer_1.htm",
    'User-Agent': agent
}
for id in range(1,201):
    url1='http://club.xywy.com/list_532_answer_'+str(id)+'.htm'
    r=requests.get(url=url1)
    try:
        html=r.content.decode('gbk')
        suburl=re.findall(r'http://club.xywy.com/static/\d+?/\d+?.htm',html)
        for i in suburl:
            shtml=requests.get(url=i).content.decode('gbk')
            question=re.findall(r'<div class="graydeep User_quecol pt10 mt10" id="qdetailc">\s*?(\S*?)\t*?</div>',shtml)
            answer=re.findall(r'<div class="pt15 f14 graydeep  pl20 pr20">(.*?)</div>',shtml)
            data='\n'.join(question+answer)
            with open('qa_bone/'+i[-22:-4].replace('/','_')+'.txt','w')as f:
                f.write(re.sub(r'(<b>.*?</b>)|(br/)|(<h5>.*?</h5>)','',data))
                print(id)
    except Exception as e:
        print(e)
    
 
    time.sleep(0.5)
