#-*- coding: utf-8-*-
import os
import re
import urllib
import urllib2
from bs4 import BeautifulSoup
import time
import datetime
import codecs


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

	with codecs.open(str(month)+str(day)+"_학식"+".txt", "w", encoding="utf-8") as f:
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
		with codecs.open(str(month)+str(day)+"_"+str(cnt)+".txt", "w", encoding="utf-8") as j:
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
			with codecs.open(str(month)+str(day)+"_"+str(cnt)+".txt", "a+", encoding="utf-8") as j:
				j.write(temp_2+"\r\n")
			temp += temp_2
			temp += "\r\n"

		temp+= "\r\n\n"
		cnt += 1



	#codec 이용해서 파일을 쓸수 있다. 개행은 \r\n
	#전체 건물 별 식단 저장.
	with codecs.open(str(month)+str(day)+"_학식"+".txt", "a+", encoding="utf-8") as f:
		f.write(temp+"\r\n")

	#	print cleanhtml(b)

	print temp
	print


def hyumin1(month,day):
	with codecs.open(str(month)+str(day)+"_학식"+".txt", "a+", encoding="utf-8") as f:
		f.write(u"제 1 효민 생활관\r\n")
		f.write("==========================================\r\n")

	with codecs.open(str(month)+str(day)+"_효민1"+".txt", "w", encoding="utf-8") as f:
		f.write(u"제 1 효민 생활관\r\n")
#		f.write("==========================================\r\n")
	print "\n+++++++++++++++++제 1 효민 생활관++++++++++++++++++++"


	###############제1 효민 생활관 파싱
	url2 = 'http://dorm.deu.ac.kr/Program/ReadFood.aspx?BuildCd=1&menu=46'
	html2 = get_source(url2,url2)
	soup2 = BeautifulSoup(html2)
	result2 = str(soup2)

	#a = soup2.find_all('td',{'width':'140'})
	a = soup2.find_all('tr')
	#a = soup2.find_all('table',{'border':'1'})
	#a = soup2.find_all('font',{'face':'Arial'})

	cnt = 0
	eatTime = 0
	result_text = ""
	tex = ""
	d = datetime.date.today()
	d= d.weekday()
	d += 2
	k=0
	#한글 파싱 // \xa0 인식불가 제거
	# b= 기숙사 식단 파싱

	for i in a:
		cnt += 1
		i = i.find_all('td')
		for b in i:
			b = b.text
			b = b.replace(u'\xa0', '')
			b = b.replace('            ','')
			b = b.replace('\r','')

			if cnt ==1:
				#print k, b[0:3]
				#조식 중식 석식 문자열 체크
				if k ==1 : mor = b[0:3]
				if k ==2 : aft = b[0:3]
				if k ==3 : eve = b[0:3]
				k+=1

			if eatTime%4 == 0:
				b = b.replace('\n','')
				result_text += b
				result_text += '\n'
				pass


			elif eatTime%4 == 1:
				b = b.replace('\n','  ')
				b = b.replace('  ',' ')
				if cnt == d:
					print '===아침==='
					with codecs.open(str(month)+str(day)+"_학식"+".txt", "a+", encoding="utf-8") as f:
						f.write(mor+"\r\n")
					with codecs.open(str(month)+str(day)+"_효민1"+".txt", "a+", encoding="utf-8") as j:
						j.write(mor+"\r\n")
				result_text += b
				result_text += '\n'

			elif eatTime%4 == 2:
				if cnt == d:
					print '===점심==='
					with codecs.open(str(month)+str(day)+"_학식"+".txt", "a+", encoding="utf-8") as f:
						f.write(aft+"\r\n")
					with codecs.open(str(month)+str(day)+"_효민1"+".txt", "a+", encoding="utf-8") as j:
						j.write(aft+"\r\n")
				b = b.replace('\n',' ')
				result_text += b
				result_text += '\n'

			elif eatTime%4 == 3:
				if cnt == d:
					print '===저녁==='
					with codecs.open(str(month)+str(day)+"_학식"+".txt", "a+", encoding="utf-8") as f:
						f.write(eve+"\r\n")
					with codecs.open(str(month)+str(day)+"_효민1"+".txt", "a+", encoding="utf-8") as j:
						j.write(eve+"\r\n")
				b = b.replace('\n',' ')
				result_text += b
				result_text += '\n\n\n'


			if cnt == d:
				print b
				with codecs.open(str(month)+str(day)+"_학식"+".txt", "a+", encoding="utf-8") as f:
					f.write(b+"\r\n\r\n")
				with codecs.open(str(month)+str(day)+"_효민1"+".txt", "a+", encoding="utf-8") as j:
					j.write(b+"\r\n")
				print

			eatTime+=1
	with codecs.open(str(month)+str(day)+"_학식"+".txt", "a+", encoding="utf-8") as f:
		f.write("\r\n\r\n")
	#print mor, aft, eve
	print "\n\n\n"


def hyumin2(month,day):
	with codecs.open(str(month)+str(day)+"_학식"+".txt", "a+", encoding="utf-8") as f:
		f.write(u"제 2 효민 생활관\r\n")
		f.write("===========================================\r\n")

	with codecs.open(str(month)+str(day)+"_효민2"+".txt", "w", encoding="utf-8") as j:
		j.write(u"제 2 효민 생활관\r\n")

	print "\n+++++++++++++++++제 2 효민 생활관++++++++++++++++++++"
	###############제2 효민 생활관 파싱
	url2 = 'http://dorm.deu.ac.kr/Program/ReadFood.aspx?BuildCd=3&menu=46'
	html2 = get_source(url2,url2)
	soup2 = BeautifulSoup(html2)
	result2 = str(soup2)

	#a = soup2.find_all('td',{'width':'140'})
	a = soup2.find_all('tr')
	#a = soup2.find_all('table',{'border':'1'})
	#a = soup2.find_all('font',{'face':'Arial'})


	cnt = 0
	eatTime = 0
	result_text = ""
	tex = ""
	d = datetime.date.today()
	d= d.weekday()
	d += 2
	k=0
	#한글 파싱 // \xa0 인식불가 제거
	# b= 기숙사 식단 파싱

	for i in a:
		cnt += 1
		i = i.find_all('td')
		for b in i:
			b = b.text
			b = b.replace(u'\xa0', '')
			b = b.replace('            ','')
			b = b.replace('\r','')

			if cnt ==1:
				#print k, b[0:3]
				#조식 중식 석식 문자열 체크
				if k ==1 : mor = b[0:3]
				if k ==2 : aft = b[0:3]
				if k ==3 : eve = b[0:3]
				k+=1

			if eatTime%4 == 0:
				b = b.replace('\n','')
				result_text += b
				result_text += '\n'
				pass


			elif eatTime%4 == 1:
				b = b.replace('\n','  ')
				b = b.replace('  ',' ')
				if cnt == d:
					print '===아침==='
					with codecs.open(str(month)+str(day)+"_학식"+".txt", "a+", encoding="utf-8") as f:
						f.write(mor+"\r\n")

					with codecs.open(str(month)+str(day)+"_효민2"+".txt", "a+", encoding="utf-8") as j:
						j.write(mor+"\r\n")
				result_text += b
				result_text += '\n'

			elif eatTime%4 == 2:
				if cnt == d:
					print '===점심==='
					with codecs.open(str(month)+str(day)+"_학식"+".txt", "a+", encoding="utf-8") as f:
						f.write(aft+"\r\n")

					with codecs.open(str(month)+str(day)+"_효민2"+".txt", "a+", encoding="utf-8") as j:
						j.write(aft+"\r\n")
				b = b.replace('\n',' ')
				result_text += b
				result_text += '\n'

			elif eatTime%4 == 3:
				if cnt == d:
					print '===저녁==='
					with codecs.open(str(month)+str(day)+"_학식"+".txt", "a+", encoding="utf-8") as f:
						f.write(eve+"\r\n")

					with codecs.open(str(month)+str(day)+"_효민2"+".txt", "a+", encoding="utf-8") as j:
						j.write(eve+"\r\n")
				b = b.replace('\n',' ')
				result_text += b
				result_text += '\n\n\n'


			if cnt == d:
				print b
				with codecs.open(str(month)+str(day)+"_학식"+".txt", "a+", encoding="utf-8") as f:
					f.write(b+"\r\n\r\n")

				with codecs.open(str(month)+str(day)+"_효민2"+".txt", "a+", encoding="utf-8") as j:
					j.write(b+"\r\n")
				print

			eatTime+=1
	with codecs.open(str(month)+str(day)+"_학식"+".txt", "a+", encoding="utf-8") as f:
		f.write("\r\n\r\n")
	#print mor, aft, eve
	print "\n\n\n"


def hyumin3(month,day):
	with codecs.open(str(month)+str(day)+"_학식"+".txt", "a+", encoding="utf-8") as f:
		f.write(u"효민 여자 생활관\r\n")
		f.write("===========================================\r\n")

	with codecs.open(str(month)+str(day)+"_효민여자"+".txt", "w", encoding="utf-8") as j:
		j.write(u"효민 여자 생활관\r\n")
	print "\n+++++++++++++++++여자 효민 생활관++++++++++++++++++++"
	###############여자 효민 생활관 파싱
	url2 = 'http://dorm.deu.ac.kr/Program/ReadFood.aspx?BuildCd=2&menu=46'
	html2 = get_source(url2,url2)
	soup2 = BeautifulSoup(html2)
	result2 = str(soup2)

	#a = soup2.find_all('td',{'width':'140'})
	a = soup2.find_all('tr')
	#a = soup2.find_all('table',{'border':'1'})
	#a = soup2.find_all('font',{'face':'Arial'})


	cnt = 0
	eatTime = 0
	result_text = ""
	tex = ""
	d = datetime.date.today()
	d= d.weekday()
	d += 2
	k=0
	#한글 파싱 // \xa0 인식불가 제거
	# b= 기숙사 식단 파싱

	for i in a:
		cnt += 1
		i = i.find_all('td')
		for b in i:
			b = b.text
			b = b.replace(u'\xa0', '')
			b = b.replace('            ','')
			b = b.replace('\r','')

			if cnt ==1:
				#print k, b[0:3]
				#조식 중식 석식 문자열 체크
				if k ==1 : mor = b[0:3]
				if k ==2 : aft = b[0:3]
				if k ==3 : eve = b[0:3]
				k+=1

			if eatTime%4 == 0:
				b = b.replace('\n','')
				result_text += b
				result_text += '\n'
				pass


			elif eatTime%4 == 1:
				b = b.replace('\n','  ')
				b = b.replace('  ',' ')
				if cnt == d:
					print '===아침==='
					with codecs.open(str(month)+str(day)+"_학식"+".txt", "a+", encoding="utf-8") as f:
						f.write(mor+"\r\n")

					with codecs.open(str(month)+str(day)+"_효민여자"+".txt", "a+", encoding="utf-8") as j:
						j.write(mor+"\r\n")
				result_text += b
				result_text += '\n'

			elif eatTime%4 == 2:
				if cnt == d:
					print '===점심==='
					with codecs.open(str(month)+str(day)+"_학식"+".txt", "a+", encoding="utf-8") as f:
						f.write(aft+"\r\n")

					with codecs.open(str(month)+str(day)+"_효민여자"+".txt", "a+", encoding="utf-8") as j:
						j.write(aft+"\r\n")
				b = b.replace('\n',' ')
				result_text += b
				result_text += '\n'

			elif eatTime%4 == 3:
				if cnt == d:
					print '===저녁==='
					with codecs.open(str(month)+str(day)+"_학식"+".txt", "a+", encoding="utf-8") as f:
						f.write(eve+"\r\n")

					with codecs.open(str(month)+str(day)+"_효민여자"+".txt", "a+", encoding="utf-8") as j:
						j.write(eve+"\r\n")
				b = b.replace('\n',' ')
				result_text += b
				result_text += '\n\n\n'


			if cnt == d:
				print b
				with codecs.open(str(month)+str(day)+"_학식"+".txt", "a+", encoding="utf-8") as f:
					f.write(b+"\r\n\r\n")

				with codecs.open(str(month)+str(day)+"_효민여자"+".txt", "a+", encoding="utf-8") as j:
					j.write(b+"\r\n")
				print

			eatTime+=1
	with codecs.open(str(month)+str(day)+"_학식"+".txt", "a+", encoding="utf-8") as f:
		f.write("\r\n\r\n")
	#print mor, aft, eve
	print "\n\n\n"




if __name__ == "__main__":
	d = datetime.date.today()
	######get_day
	#dat = raw_input("월, 일을 입력하세요(예시 1201, 1205) : ")
	#month = dat[0:-2]
	#print month
	#day = dat[2:]
	#print day
	month = str(d.month)
	if d.day <10: day = '0'+str(d.day)
	else:
		day = str(d.day)

#	print day, month

	haksik(month,day)
	hyumin1(month,day)
	hyumin2(month,day)
	hyumin3(month,day)
