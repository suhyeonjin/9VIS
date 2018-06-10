#-*- coding: utf-8-*-
import os, re, urllib, urllib2, time, datetime, codecs, json
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db



todayDate = str(datetime.datetime.now()).split(' ')[0]
personalMenu =''
nationalConor = []
informationConor = []
sudukConor = []
domitoryList = []

def makeJson():
	#[코너1] 돈까스카레소스덮밥 미소국[코너2] 콩나물쫄면 미소국[코너3] 차슈덮밥 콩나물국[코너4] 라면 라면밥
	with codecs.open(str(todayDate)+"_1"+".txt", "r", encoding="utf-8") as f:
		tmp = f.read()
		sudukL = tmp.split('\n')[1].replace('[','\n').strip().split('\n')

	for i in sudukL:
		sudukConor.append(i.split(']')[1].strip())

	#print sudukConor

	#sudukConor.append(tmp.split('\n')[1].replace('[','\n').strip().split('\n')[0].split(']')[1].strip())

	#print tmp.split('\n')[1].replace('[','\n').strip().split('\n')[1].split(']')[1].strip()
	#print tmp.split('\n')[1].replace('[','\n').strip().split('\n')[2].split(']')[1].strip()
	#print tmp.split('\n')[1].replace('[','\n').strip().split('\n')[3].split(']')[1].strip()

	with codecs.open(str(todayDate)+"_2"+".txt", "r", encoding="utf-8") as f:
		tmp = f.read()
		jungboL = tmp.split('\n')[1].replace('[','\n').strip().split('\n')

	for i in jungboL:
		i = i.replace(';','').replace('&','').replace('amp',' ')
		informationConor.append(i.split(']')[1].strip())




	with codecs.open(str(todayDate)+"_3"+".txt", "r", encoding="utf-8") as f:
		tmp = f.read()
		nationalL = tmp.split('\n')[1].replace('[','\n').strip().split('\n')

	for i in nationalL:
		i = i.replace(';','').replace('&','').replace('amp',' ')
		nationalConor.append(i.split(']')[1].strip())



	menuDic = {
	"structure" : {
	    "교직원" : {
	      "점심" : {
	        "코너1" : "확인할 수 없습니다"
	      }
	    },
	    "국제관" : {
	      "점심" : {
	        "코너1" : nationalConor[0],
	        "코너2" : nationalConor[1],
	        "코너3" : nationalConor[2]
	      }
	    },
	    "기숙사" : {
	      "아침" : {
	        "메뉴" : domitoryList[0]
	      },
	      "저녁" : {
	        "메뉴" : domitoryList[2]
	      },
	      "점심" : {
	        "메뉴" : domitoryList[1]
	      }
	    },
	    "수덕전" : {
	      "점심" : {
	        "코너1" : sudukConor[0],
	        "코너2" : sudukConor[1],
	        "코너3" : sudukConor[2],
	        "코너4" : sudukConor[3],
	      }
	    },
	    "정보공학관" : {
	      "점심" : {
	        "코너1" : informationConor[0],
	        "코너2" : informationConor[1],
	        "코너3" : informationConor[2]
	      }
	    }
	  }
	}

	with codecs.open('data.json', 'w',encoding="utf-8") as outfile:
		json.dump(menuDic, outfile)


	#firebase Auto uploading
	'''
	# Fetch the service account key JSON file contents
	cred = credentials.Certificate('../../../newagent-38ccc-firebase-adminsdk-degz8-56e307064b.json')
	# Initialize the app with a service account, granting admin privileges
	firebase_admin.initialize_app(cred, {
	    'databaseURL': 'https://newagent-38ccc.firebaseio.com/'
	})

	# Save data
	ref = db.reference('/')
	ref.set(menuDic)
	'''

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


	with codecs.open(str(todayDate)+"_sikdan"+".txt", "w", encoding="utf-8") as f:
		f.write(str(d.year)+'_'+month+'_'+day+' ('+yoeil[day_num]+")\r\n")
		f.write("==========================================\r\n\r\n")



	#      'http://m.deu.ac.kr/facility/mobile/page/30070706.jsp?total_date='+str(todayDate.replace('-',''))
	#url = 'http://m.deu.ac.kr/facility/mobile/page/30070706.jsp?total_date=20151201&yy=2015'
	url = 'http://m.deu.ac.kr/facility/mobile/page/30070706.jsp?total_date='+str(todayDate.replace('-',''))
	url = "http://m.deu.ac.kr/facility/mobile/page/30070706.jsp?total_date=20180612&yy=2018&mm=06&dd=12"
	#print url

	html = get_source(url,url)
	soup = BeautifulSoup(html,"lxml")
	result = str(soup)

	#menu
	elements = soup.findAll('div', {'class':'menu'})
	#location
	elements2 = soup.findAll('h1')

	result1 = ""
	result2 = ""

	#regexp = re.compile(r'[가-?]+')
	regexp = re.compile(r'[\u3131-\u3163\uac00-\ud7a3]+')


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
	#   건물 별로 따로 파일 생성/저장 작업 >> temp_1 은 건물 명
		with codecs.open(str(todayDate)+"_"+str(cnt)+".txt", "w", encoding="utf-8") as j:
			j.write(temp_1+"\r\n")
		temp += temp_1
		temp += "\r\n"
	#	print str(elements[i]).decode('utf-8')
		b = str(elements[i]).decode('utf-8')
		b = b.split('<br><br>')

		for i in b:
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
	with codecs.open(str(todayDate)+"_sikdan"+".txt", "a+", encoding="utf-8") as f:
		f.write(temp+"\r\n")

	#	print cleanhtml(b)

	print temp
	#print

#기숙사 통합 식단.
def hyumin1(month,day):
	global domitoryList
	with codecs.open(str(todayDate)+"_sikdan"+".txt", "a+", encoding="utf-8") as f:
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
	mor = driver.find_element_by_xpath("//td[@id='fo_menu_mor"+day+"']").text

	#lunch
	lun = driver.find_element_by_xpath("//td[@id='fo_menu_lun"+day+"']").text

	#evening
	eve = driver.find_element_by_xpath("//td[@id='fo_menu_eve"+day+"']").text
	print "조식 : ",mor
	print "중식 : ",lun
	print "석식 : ",eve
	domitoryList.append(mor)
	domitoryList.append(lun)
	domitoryList.append(eve)

	driver.quit()
	with codecs.open(str(todayDate)+"_sikdan"+".txt", "a+", encoding="utf-8") as f:
		f.write(mor+"\r\n")
		f.write(lun+"\r\n")
		f.write(eve+"\r\n")
		f.write("\r\n\r\n")
	#print mor, aft, eve
	with codecs.open(str(todayDate)+"_domitory"+".txt", "w", encoding="utf-8") as f:
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
	#updateFirebase()
	makeJson()

