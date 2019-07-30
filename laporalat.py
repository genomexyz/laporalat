#!/usr/bin/python3

import logging
import csv
import datetime
import mysql.connector
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

#setting
ICAOfile = 'ICAO.csv'
serverdb = 'localhost'
userdb = 'root'
passdb = 'reyditya'
dbname = 'alat'

#Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

#load all ICAO
allICAO = []
ICAOopen = open(ICAOfile)
ICAOlist = csv.reader(ICAOopen)
for ICAO in ICAOlist:
	allICAO.append(ICAO)

def checkavability(wilayah, waktu):
	cnt = 0
	mydb = mysql.connector.connect(host=serverdb, user=userdb, passwd=passdb, database=dbname)
	mycursor = mydb.cursor()
	querry = "SELECT * FROM arsipalat WHERE wilayah="+"'"+wilayah+"' AND waktu="+"'"+waktu+"'"
	mycursor.execute(querry)

	myresult = mycursor.fetchall()

	for x in myresult:
		print(x)
		cnt += 1
		result = x
	
	if cnt == 0:
		return 'none'
	else:
		return result

def inserttodb(waktu, wilayah, awosanemometer, awosbarometer, awostermometer, awosceilometer, awosvisibility, radar, llwas, lidarva):
	mydb = mysql.connector.connect(host=serverdb, user=userdb, passwd=passdb, database=dbname)
	mycursor = mydb.cursor()
	querry = "INSERT INTO arsipalat (wilayah, waktu, awosanemometer, awosbarometer, awostermometer, awosceilometer, awosvisibility, radar, llwas, lidarva) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
	val = (wilayah, waktu, awosanemometer, awosbarometer, awostermometer, awosceilometer, awosvisibility, radar, llwas, lidarva)
	mycursor.execute(querry, val)
	mydb.commit()

def updatetodb(fetcheddb):
	wilayah = fetcheddb[1]
	awosanemometer = fetcheddb[3]
	awosbarometer = fetcheddb[4]
	awostermometer = fetcheddb[5]
	awosceilometer = fetcheddb[6]
	awosvisibility = fetcheddb[7]
	radar = fetcheddb[8]
	llwas = fetcheddb[9]
	lidarva = fetcheddb[10]
	ids = fetcheddb[0]
	mydb = mysql.connector.connect(host=serverdb, user=userdb, passwd=passdb, database=dbname)
	mycursor = mydb.cursor()
	querry = "UPDATE arsipalat SET wilayah=%s, awosanemometer=%s, awosbarometer=%s, awostermometer=%s, awosceilometer=%s, awosvisibility=%s, radar=%s, llwas=%s, lidarva=%s WHERE id=%s"
	val = (wilayah, awosanemometer, awosbarometer, awostermometer, awosceilometer, awosvisibility, radar, llwas, lidarva, ids)
	mycursor.execute(querry, val)
	mydb.commit()
	
#	print(wilayah, awosanemometer, awosbarometer, awostermometer, awosceilometer, awosvisibility, radar, llwas, lidarva, ids)
	print("UPDATE arsipalat SET wilayah=%s, awosanemometer=%s, awosbarometer=%s, awostermometer=%s, awosceilometer=%s, awosvisibility=%s, radar=%s, llwas=%s, lidarva=%s WHERE id=%s" %(wilayah, awosanemometer, awosbarometer, awostermometer, awosceilometer, awosvisibility, radar, llwas, lidarva, ids))

def koreksistr(string):
	stringbaru = string
	while '  ' in stringbaru:
		stringbaru = stringbaru.replace('  ', ' ')
	while '\n\n' in stringbaru:
		stringbaru = stringbaru.replace('\n\n', '\n')
	stringbaru = stringbaru.lower()
	return stringbaru

def extractinfo(fragment):
	wilayah = 'unknown'
	for i in range(len(allICAO)):
		if allICAO[i][0].lower() in fragment[0]:
			wilayah = allICAO[i][0]
			break

	awosanemometer = 'unknown'
	for i in range(len(fragment)):
		if '(awos) anemometer' in fragment[i] or '(awos)anemometer' in fragment[i]:
			awosanemometer = fragment[i][fragment[i].find(':')+1:].strip()
			if not (awosanemometer == 'on' or awosanemometer == 'off' or awosanemometer == 'none'):
				awosanemometer = 'unknown'
			break
	
	awosbarometer = 'unknown'
	for i in range(len(fragment)):
		if '(awos) barometer' in fragment[i] or '(awos)barometer' in fragment[i]:
			awosbarometer = fragment[i][fragment[i].find(':')+1:].strip()
			if not (awosbarometer == 'on' or awosbarometer == 'off' or awosbarometer == 'none'):
				awosbarometer = 'unknown'
			break
	
	awostermometer = 'unknown'
	for i in range(len(fragment)):
		if '(awos) termometer' in fragment[i] or '(awos)termometer' in fragment[i]:
			awostermometer = fragment[i][fragment[i].find(':')+1:].strip()
			if not (awostermometer == 'on' or awostermometer == 'off' or awostermometer == 'none'):
				awostermometer = 'unknown'
			break

	awosceilometer = 'unknown'
	for i in range(len(fragment)):
		if '(awos) ceilometer' in fragment[i] or '(awos)ceilometer' in fragment[i]:
			awosceilometer = fragment[i][fragment[i].find(':')+1:].strip()
			if not (awosceilometer == 'on' or awosceilometer == 'off' or awosceilometer == 'none'):
				awosceilometer = 'unknown'
			break
	
	awosvisibility = 'unknown'
	for i in range(len(fragment)):
		if '(awos) visibility' in fragment[i] or '(awos)visibility' in fragment[i]:
			awosvisibility = fragment[i][fragment[i].find(':')+1:].strip()
			if not (awosvisibility == 'on' or awosvisibility == 'off' or awosvisibility == 'none'):
				awosvisibility = 'unknown'
			break
	
	radar = 'unknown'
	for i in range(len(fragment)):
		if 'radar cuaca' in fragment[i]:
			radar = fragment[i][fragment[i].find(':')+1:].strip()
			if not (radar == 'on' or radar == 'off' or radar == 'none'):
				radar = 'unknown'
			break
	
	llwas = 'unknown'
	for i in range(len(fragment)):
		if 'llwas' in fragment[i]:
			llwas = fragment[i][fragment[i].find(':')+1:].strip()
			if not (llwas == 'on' or llwas == 'off' or llwas == 'none'):
				llwas = 'unknown'
			break
	
	lidarva = 'unknown'
	for i in range(len(fragment)):
		if 'lidar va' in fragment[i]:
			lidarva = fragment[i][fragment[i].find(':')+1:].strip()
			if not (lidarva == 'on' or lidarva == 'off' or lidarva == 'none'):
				lidarva = 'unknown'
			break

	return wilayah, awosanemometer, awosbarometer, awostermometer, awosceilometer, awosvisibility, radar, llwas, lidarva

def help(update, context):
	"""Send a message when the command /help is issued."""
	update.message.reply_text('daftar perintah khusus:\n\
	/status : daftar kode ICAO yang sudah melapor hari ini\n\
	/allicao : daftar kode ICAO yang peralatannya ingin dan bisa dilaporkan\n\n\
	Harap melakukan pelaporan peralatan kondisi alat setiap hari. Untuk format pelaporan sebagai berikut dibawah ini tanpa tanda kutip.\n\
	"/lapor <kode ICAO>\n\
	(AWOS) Anemometer: <on/off/none>\n\
	(AWOS) Barometer: <on/off/none>\n\
	(AWOS) Termometer: <on/off/none>\n\
	(AWOS) Ceilometer: <on/off/none>\n\
	(AWOS) Visibility: <on/off/none>\n\
	RADAR cuaca: <on/off/none>\n\
	LLWAS: <on/off/none>\n\
	LIDAR VA: <on/off/none>"\n\n\
	on jika alatnya hidup, off jika alatnya mati atau tidak bekerja dan none jika alat tersebut tidak ada. Contoh pelaporannya\
	 adalah sebagai berikut:')
	update.message.reply_text("/lapor WIII\n\
	(AWOS) Anemometer: on\n\
	(AWOS) Barometer: on\n\
	(AWOS) Termometer: on\n\
	(AWOS) Ceilometer: on\n\
	(AWOS) Visibility: on\n\
	RADAR cuaca: on\n\
	LLWAS: on\n\
	LIDAR VA: none")
	update.message.reply_text("Silahkan dijadikan template contoh pelaporan tersebut untuk mempermudah user sekalian.")

def printallICAO(update, context):
	strsend = 'list kode ICAO yang ingin dan bisa dilaporkan:\n'
	for i in range(len(allICAO)):
		strsend += '-'+allICAO[i][0]+'\n'
	update.message.reply_text(strsend)

def recvlaporan(update, context):
	#update.message.reply_text(update.message.from_user.username+' '+update.message.text)
	#print(update.message.text)
	pesan = update.message.text
	pesan = koreksistr(pesan)
	pesanfragmet = pesan.split('\n')
	allinfo = extractinfo(pesanfragmet)
	
	for i in range(len(allinfo)):
		if allinfo[i] == 'unknown':
			update.message.reply_text('Laporan tidak valid, ulangi lagi')
			return 0

	waktu = datetime.datetime.utcnow()
	waktustr = waktu.strftime('%Y%m%d')
	checkAVA = checkavability(allinfo[0], waktustr)
	if checkAVA == 'none':
		inserttodb(waktustr, allinfo[0], allinfo[1], allinfo[2], allinfo[3], allinfo[4], allinfo[5], allinfo[6], allinfo[7], allinfo[8])
		update.message.reply_text('Telah dimasukkan datanya untuk '+allinfo[0])
	else:
		fetchedupdate = (str(checkAVA[0]), allinfo[0], waktustr, allinfo[1], allinfo[2], allinfo[3], allinfo[4], allinfo[5], allinfo[6], allinfo[7], allinfo[8])
		updatetodb(fetchedupdate)
		update.message.reply_text('Telah diperbaharui untuk '+allinfo[0])

	wilayah = allinfo[0]
	awosanemometer = allinfo[1]
	


def error(update, context):
	"""Log Errors caused by Updates."""
	logger.warning('Update "%s" caused error "%s"', update, context.error)

def testinline(update, context):
	print('masuk fungsi')
	print(update.message.text)
	#if update.inline_query is not None and update.inline_query.query:
	update.message.reply_text('balasannya : '+update.inline_query.query)

def main():
	"""Start the bot."""
	# Create the Updater and pass it your bot's token.
	# Make sure to set use_context=True to use the new context based callbacks
	# Post version 12 this will no longer be necessary
	updater = Updater("649890106:AAEUQAY9MiXIiGJHiPRXJlVpZY1e9DSZI-g", use_context=True)

	# Get the dispatcher to register handlers
	dp = updater.dispatcher

	# on different commands - answer in Telegram
	dp.add_handler(CommandHandler("help", help))

	# test inline
	dp.add_handler(CommandHandler("test", testinline))

	#list all ICAO
	dp.add_handler(CommandHandler("allicao", printallICAO))

	#receive laporan
	dp.add_handler(CommandHandler("lapor", recvlaporan))

	# log all errors
	dp.add_error_handler(error)

	# Start the Bot
	print('bot start')
	updater.start_polling()

	# Run the bot until you press Ctrl-C or the process receives SIGINT,
	# SIGTERM or SIGABRT. This should be used most of the time, since
	# start_polling() is non-blocking and will stop the bot gracefully.
	updater.idle()


if __name__ == '__main__':
	main()
