#-*- coding: utf-8-*-
import os, re, urllib, time, datetime, codecs, json
from bs4 import BeautifulSoup

##Referrer check + add
def get_source(url,referer):
    req = urllib.request.Request(url)
    req.add_header("Referer",referer)
    response = urllib.request.urlopen(req)
    the_page = response.read()
    return the_page

def cleanhtml(raw_html):
     cleanr =re.compile('<.*?>')
     cleantext = re.sub(cleanr,'', raw_html)
     return cleantext

def getNotice():
    url = 'http://deu.ac.kr/jsp/module/board/list01.do?menu_no=1001050101&conf_no=23&board_no=&category_no=N'


    html = get_source(url,url)
    soup = BeautifulSoup(html,"lxml")
    result = str(soup)

    resultDic = {}
    dic = {}
    tmp = []
    #menu
    elements = soup.findAll('a',href=True)
    cnt = 1
    for i in elements[3:-14]:
        dic[cnt] = (cleanhtml(str(i)))
        cnt += 1

    resultDic['Notice'] = {"공지":dic}
    print (resultDic)


    print (resultDic)
    with codecs.open('dataNotice.json', 'w',encoding="utf-8") as outfile:
        json.dump(resultDic, outfile)


if __name__ == "__main__":
    getNotice()
