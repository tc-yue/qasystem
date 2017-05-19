#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import re
import time
agent = 'Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0'
headers = {
    "Host": "baike.baidu.com",
    "Referer": "http://baike.baidu.com/wikitag/taglist?tagId=75954",
    'User-Agent': agent
}
data = {'limit':'24','timeout':'3000','filterTags':'[]','tagId':'75954','fromelemma':'false','contentLength':'40','page':'0'}
for i in range(500,600):
    print(i)
    data['page']=str(i)
    r=requests.post(url='http://baike.baidu.com/wikitag/api/getlemmas',data=data,headers=headers)
    for item in r.json()['lemmaList']:
        suburl=item['lemmaUrl']
        html=requests.get(suburl).content.decode()
        d=re.findall(r'</span>(\S+?)</h2>\s+</div>\s+<div class="para" label-module="para">(\S+?)</div>',html)
        b=re.findall(r'<div class="lemma-summary" label-module="lemmaSummary">\s(\S+?)\s</div>',html)
        c=re.findall(r'<dt class="basicInfo-item name">(\S+?)</dt>\s<dd class="basicInfo-item value">\s(\S+?)\s</dd>',html)
        id=re.findall(r'(\d+?).htm',suburl)[0]
        with open ('medicine_data/'+str(id)+'.txt','w') as f:
            for j in c:
                f.write(j[0]+j[1]+'\n')
            for j in d:
                f.write(j[0]+j[1]+'\n')
            for j in b:
                f.write(j+'\n')

    time.sleep(0.5)



