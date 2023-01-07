import requests
import re
import csv

#LiTV

allinfo =[]
#第一層
rankpage_url = 'https://www.litv.tv/vod/movie/list.do?category_id=124&page=1'
rankpage = requests.get(rankpage_url)
#print(rankpage.text)

obj1 = r'<a class="content_item" title="(?P<name>.*?)" href="(?P<urls>.*?)">'
iter1 = re.finditer(obj1, rankpage.text)
domainurl = 'https://www.litv.tv'

with open('move_info.csv', 'w',newline='', encoding='UTF-8') as m:
    write = csv.writer(m)

    for i in iter1:
        #print(i.group('name'))
        eachurl = domainurl + i.group('urls')
        #print(eachurl)

    #第二層
        moviepage = requests.get(eachurl)
        #print(moviepage.text)
    
        obj2 = r'<h1 class="vod_title">(?P<name>.*?)</h1>.*?"secondary_mark">(?P<Eng_name>.*?)</h2>.*?年份.*?">(?P<year>.*?)</a>'
        iter2 = re.finditer(obj2, moviepage.text, re.S)
    
        for j in iter2:
            infolist = [j.group('name'), j.group('Eng_name'), j.group('year')]
            write.writerow(infolist)
