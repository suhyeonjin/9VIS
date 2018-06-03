#-*- coding: utf-8-*-
import os
import re
import urllib
import urllib2
from bs4 import BeautifulSoup
import time
import datetime
import codecs


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


todayDate = str(datetime.datetime.now()).split(' ')[0]

##Referrer check + add
def get_source(url,referer):
	req = urllib2.Request(url)
	req.add_header("Referer",referer)
	response = urllib2.urlopen(req)
	the_page = response.read()
	return the_page

def cleanhtml(raw_html):
	 cleanr =re.compile('<.*?>')
	 cleantext = re.sub(cleanr,'', raw_html)
	 return cleantext

def haksik(month,day):
	d = datetime.date.today()
	day_num = d.weekday()
	yoeil = {0:u'월',1:u'화',2:u'수',3:u'목',4:u'금',5:u'토',6:u'일'}
	print yoeil[day_num]
	#yoeil = str(yoeil[day_num])

	with codecs.open(str(todayDate)+"_학식"+".txt", "w", encoding="utf-8") as f:
		f.write(str(d.year)+'_'+month+'_'+day+' ('+yoeil[day_num]+")\r\n")
		f.write("==========================================\r\n\r\n")


	#url = 'http://m.deu.ac.kr/facility/mobile/page/30070706.jsp?total_date=20151201&yy=2015'
	url = 'http://m.deu.ac.kr/facility/mobile/page/30070706.jsp?total_date=2015'+month +day
	html = get_source(url,url)
	soup = BeautifulSoup(html)
	result = str(soup)
	#regexp = re.compile(r'[가-?]')
	#imgs = regexp.findall(result)
	#print soup.replaceAll("<(/)?([a-zA-Z]*)(\\s[a-zA-Z]*=[^>]*)?(\\s)*(/)?>")


	#html 태그 제거 파싱
	#print cleanhtml(str(soup)).decode('utf-8')
	#cleantext = cleanhtml(str(soup)).decode('utf-8')
	#print type(cleantext)

	#menu
	elements = soup.findAll('div', {'class':'menu'})
	#location
	elements2 = soup.findAll('h1')

	result1 = ""
	result2 = ""

	#regexp = re.compile(r'[가-?]+')
	regexp = re.compile(r'[\u3131-\u3163\uac00-\ud7a3]+')


	#식당 위치
	#for i in elements2:
	#	print str(i).decode('utf-8')+"\n"
	#	result1 += str(i).decode('utf-8')

	#메뉴
	#for j in elements:
	#	print str(j).decode('utf-8')+"\n"
	#	result2 += str(j).decode('utf-8')

	location_len = len(elements2) #4
	menu_len = len(elements)

	total = ""
	print "\n+++++++++++++++동의대학교 건물별 학식++++++++++++++++++\n"
	temp =""
	temp_1 = ""
	temp_2 = ""
	cnt = 1

	for i in range(0,location_len):
	#	print str(elements2[i]).decode('utf-8')
		a = str(elements2[i]).decode('utf-8')
	#	print cleanhtml(a)
		temp_1 = cleanhtml(a)
	#	print "[+]",temp_1
	#  건물 별로 따로 파일 생성/저장 작업 >> temp_1 은 건물 명
		with codecs.open(str(todayDate)+"_"+str(cnt)+".txt", "w", encoding="utf-8") as j:
			j.write(temp_1+"\r\n")
		temp += temp_1
		temp += "\r\n"
	#	print str(elements[i]).decode('utf-8')
		b = str(elements[i]).decode('utf-8')
		b = b.split('<br><br>')

		for i in b:
	#		print "+++",cleanhtml(i)
			temp_2 = cleanhtml(i)
			print "[+]",temp_2
			#  건물 별로 따로 파일 생성/저장 작업 >> temp_2 는 식단표
			with codecs.open(str(todayDate)+"_"+str(cnt)+".txt", "a+", encoding="utf-8") as j:
				j.write(temp_2+"\r\n")
			temp += temp_2
			temp += "\r\n"

		temp+= "\r\n\n"
		cnt += 1



	#codec 이용해서 파일을 쓸수 있다. 개행은 \r\n
	#전체 건물 별 식단 저장.
	with codecs.open(str(todayDate)+"_학식"+".txt", "a+", encoding="utf-8") as f:
		f.write(temp+"\r\n")

	#	print cleanhtml(b)

	print temp
	print

#기숙사 통합 식단.
def hyumin1(month,day):
	with codecs.open(str(todayDate)+"_학식"+".txt", "a+", encoding="utf-8") as f:
		f.write(u"기숙사 통합\r\n")
		f.write("==========================================\r\n")

	print "\n+++++++++++++++++제 1 효민 생활관++++++++++++++++++++"




	#url 변경 : https://dorm.deu.ac.kr/hyomin/food/getWMLastNext.kmc?sch_date=2018-06-03
	url2 = 'https://dorm.deu.ac.kr/hyomin/food/getWMLastNext.kmc?sch_date=2018-06-03'

	#header setting
	options = webdriver.ChromeOptions()
	options.add_argument('headless')
	options.add_argument('window-size=1920x1080')
	options.add_argument("disable-gpu")
	options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
	options.add_argument("lang=ko_KR")

	#chrome driver load
	driver = webdriver.Chrome('./chromedriver', chrome_options=options)
	driver.get('about:blank')
	driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5];},});")



	day = str(time.localtime().tm_wday+1)

	driver.get('https://dorm.deu.ac.kr/hyomin/food/getWMLastNext.kmc?sch_date='+todayDate)
	#today Click -> javascript onclick
	driver.find_element_by_xpath("//a[@id='tabDay"+day+"']").send_keys(Keys.ENTER)


	#morning
	mor = driver.find_element_by_xpath("//td[@id='fo_menu_mor1']").text

	#lunch
	lun = driver.find_element_by_xpath("//td[@id='fo_menu_lun1']").text

	#evening
	eve = driver.find_element_by_xpath("//td[@id='fo_menu_eve1']").text
	print "조식 : ",mor
	print "중식 : ",lun
	print "석식 : ",eve

	driver.quit()
	with codecs.open(str(todayDate)+"_학식"+".txt", "a+", encoding="utf-8") as f:
		f.write(mor+"\r\n")
		f.write(lun+"\r\n")
		f.write(eve+"\r\n")
		f.write("\r\n\r\n")
	#print mor, aft, eve
	with codecs.open(str(todayDate)+"_기숙사"+".txt", "w", encoding="utf-8") as f:
		f.write(mor+"\r\n")
		f.write(lun+"\r\n")
		f.write(eve+"\r\n")
		f.write("\r\n\r\n")
	print "\n\n\n"


if __name__ == "__main__":
	d = datetime.date.today()
	month = str(d.month)
	if d.day<10: day = '0'+str(d.day)
	else:
		day = str(d.day)

	haksik(month,day)
	hyumin1(month,day)

