# -*- coding: UTF-8 -*-
import pymysql as mariadb
# http://flowsnow.net/2017/04/14/Python-pymysql/
try:
    db = mariadb.connect(host='ip',user='aaa',password='aaa',database='fifa')
    
except Exception as e:
    print('Connection Failed!\nError Code is %s;\nError Content is %s;' % (e.args[0],e.args[1]))

cursor = db.cursor()
# d=[43812,43817,1,0,2002,'1985-01-04','asdf']
d = ['43946', '43879', '0', '1', '2002', '2002-05-31', "Group A"]
sql = "INSERT INTO `matches`(`home`,`away`,`h_score`,`a_score`,`year`,`date`,`stage`)VALUES("+d[0]+','+d[1]+','+d[2]+','+d[3]+','+d[4]+",'"+d[5]+"','"+d[6]+"')"
# for i in range(7):
# print type(int(d[0]))
print sql

try:
   	cursor.execute(sql)
   	db.commit()
   	print("finifshed")
except Exception as e:
   	db.rollback()
   	# print('Connection Failed!\nError Code is %s;\nError Content is %s;' % (e.args[0],e.args[1]))
   	print (e)

db.close()


# data = cursor.fetchone()
# print data