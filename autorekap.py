#!/usr/bin/python3

import logging
import csv
import datetime
import mysql.connector

#setting
ICAOfile = 'ICAO.csv'
mapdb = '/var/www/html/laporalat/mapdb.csv'
serverdb = 'localhost'
userdb = 'root'
passdb = 'YOUR PASS'
dbname = 'alat'

def checkavability(waktu):
	cnt = 0
	mydb = mysql.connector.connect(host=serverdb, user=userdb, passwd=passdb, database=dbname)
	mycursor = mydb.cursor()
	querry = "SELECT * FROM arsipalat WHERE waktu="+"'"+waktu+"'"
	mycursor.execute(querry)

	myresult = mycursor.fetchall()

	result = []
	for x in myresult:
		cnt += 1
		result.append(x)

	return result


#define time
waktu = datetime.datetime.utcnow()
waktustr = waktu.strftime('%Y%m%d')
print(waktustr)

#load all ICAO
allICAO = []
ICAOopen = open(ICAOfile)
ICAOlist = csv.reader(ICAOopen)
for ICAO in ICAOlist:
	allICAO.append(ICAO)


#load alldata db in time
alldataintime = checkavability(waktustr)
print(alldataintime)

#save all data in file
openmapdb = open(mapdb, 'w')
for i in range(len(allICAO)):
	tidakadadata = True
	for j in range(len(alldataintime)):
		if allICAO[i][0] == alldataintime[j][1]:
			openmapdb.write(allICAO[i][0]+','+allICAO[i][1]+','+allICAO[i][2]+','+
			alldataintime[j][3]+','+alldataintime[j][4]+','+alldataintime[j][5]+','+alldataintime[j][6]+','+
			alldataintime[j][7]+','+alldataintime[j][8]+','+alldataintime[j][9]+','+alldataintime[j][10]+'\n')
			tidakadadata = False
			break
	if tidakadadata:
		openmapdb.write(allICAO[i][0]+','+allICAO[i][1]+','+allICAO[i][2]+','+
		'belum lapor'+','+'belum lapor'+','+'belum lapor'+','+'belum lapor'+','+
		'belum lapor'+','+'belum lapor'+','+'belum lapor'+','+'belum lapor'+'\n')
