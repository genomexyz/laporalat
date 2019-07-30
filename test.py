#!/usr/bin/python3

import mysql.connector

#setting
serverdb = 'localhost'
userdb = 'root'
passdb = 'reyditya'
dbname = 'alat'

def checkavability(wilayah, waktu):
	cnt = 0
	mydb = mysql.connector.connect(host=serverdb, user=userdb, passwd=passdb, database=dbname)
	mycursor = mydb.cursor()
	querry = "SELECT * FROM arsipalat WHERE wilayah="+"'"+wilayah+"' AND waktu="+"'"+waktu+"'"
	print(querry)
	mycursor.execute(querry)

	myresult = mycursor.fetchall()

	for x in myresult:
		cnt += 1
	
	if cnt == 0:
		return 'none'
	else:
		return myresult

mydb = mysql.connector.connect(host="localhost", user="root", passwd="reyditya")

print(mydb)

print(checkavability('WIII', '20190112'))
