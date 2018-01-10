#-*- coding:utf-8 -*-
import urllib2
import random
import pymysql as mariadb
from bs4 import BeautifulSoup
url=[ 'http://www.fifa.com/worldcup/archive/koreajapan2002/matches/index.html',
	  'http://www.fifa.com/worldcup/archive/germany2006/matches/index.html',
	  'http://www.fifa.com/worldcup/archive/southafrica2010/matches/index.html',
	  'http://www.fifa.com/worldcup/archive/brazil2014/matches/index.html' ]

my_headers=["Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36", 
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36", 
"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0" 
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) version/7.0.3 Safari/537.75.14", 
"Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)"] 

def main():
	dataset=[]
	for i in range(4):	
		content = get_content(url[i],my_headers)
		dataset.extend(exetraction(content))
	# print dataset[0]
	#connect and insert into Mariadb
	# for i in range(7):
	# 	print dataset[0][i] #272 matches in these 4 tourments
	for i in range(len(dataset)):
		insert(dataset[i])

def get_content(url,headers): 
  randdom_header=random.choice(headers)  
  req=urllib2.Request(url) 
  req.add_header("User-Agent",randdom_header) 
  req.add_header("Host","www.fifa.com") 
  req.add_header("Referer","http://www.fifa.com/") 
  req.add_header("GET",url)  
  content=urllib2.urlopen(req).read() 
  return content 

def exetraction(content):
	output=[]
	h_score=[]
	a_score=[]
	year=[]
	soup = BeautifulSoup(content,'html.parser')
	home=soup.find_all("","t home")
	away=soup.find_all("","t away")
	score = soup.find_all("","s-scoreText")
	date = soup.find_all("","mu-i-date")
	stage = soup.find_all("","mu-i-group")
	# first arg is tag name(ex:h1,h2) second is class 
	# http://bit.ly/2CVcW3e 
	
	for i in range(len(home)):
		home[i]=home[i]['data-team-id']
		away[i]=away[i]['data-team-id']
		score[i] = score[i].text.strip()
		h_score.append(score[i][0])
		a_score.append(score[i][-1])
		date[i]=date[i].text.strip()
		year.append(date[i].split()[-1])
		stage[i]=stage[i].text.strip()
		
		date[i]=normalizaionDate(date[i].split()[0],date[i].split()[1],date[i].split()[2])
	output=zip(home,away,h_score,a_score,year,date,stage)
	return output

def normalizaionDate(d,m,y):
	output=''
	# python doesn't have 'switch' 
	if m=='May':
		output=y+'-05-'+d
	elif m=='Jun':
		output=y+'-06-'+d
	else:
		output=y+'-07-'+d
	return output

# Then connect to sql and then insert data
# http://flowsnow.net/2017/04/14/Python-pymysql/
def conn():
	try:
	    db = mariadb.connect(host='ip',user='aaa',password='aaa',database='fifa')
	    
	except Exception as e:
	    print('Connection Failed!\nError Code is %s;\nError Content is %s;' % (e.args[0],e.args[1]))
	return db

def insert(data):
	db = mariadb.connect(host='ip',user='aaa',password='aaa',database='fifa')
	cursor = db.cursor()
	d=['','','','','','','']
	for i in range(7):
		d[i]=data[i].encode('utf-8')
	# print d
	sql = "INSERT INTO `matches`(`home`,`away`,`h_score`,`a_score`,`year`,`date`,`stage`)VALUES("+d[0]+','+d[1]+','+d[2]+','+d[3]+','+d[4]+",'"+d[5]+"','"+d[6]+"')"
	try:
   		cursor.execute(sql)
   		db.commit()
   		print("finifshed")
	except Exception as e:
   		db.rollback()
   		print('Connection Failed!\nError Code is %s;\nError Content is %s;' % (e.args[0],e.args[1]))

   	db.close()

if __name__ == "__main__":
    main()