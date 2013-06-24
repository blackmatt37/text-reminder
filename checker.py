import couchdb
from time import time, sleep
from twilio.rest import TwilioRestClient
from time import gmtime, strftime
import sys


account_sid = 'AC954b92ab3aa3fe23cee06ae56b384019'
auth_token = 'b037fe51ee05147c69c806d78b3d9e95'
advance = 2

def sendMessage(message, number):
	client = TwilioRestClient(account_sid, auth_token)
	message = client.sms.messages.create(to=number, from_="7039400998", body=message)



while True:
	server = couchdb.client.Server("http://23.21.135.161:5984/")
	db = server['texter']
	foreward = int(time()) + 60*advance
	map_fun = '''function(doc) {
		if(doc.time < ''' + str(foreward) + ''' && doc.done == "false") {
			emit(doc.number, doc.message);
		}
	}'''
	results = db.query(map_fun).rows
	while int(time()) < foreward:
		second = []
		for row in results:
			#print int(time())
			if int(row.id) < time():
				doc = db[row.id]
				doc['done'] = 'true'
				db[row.id] = doc
				sendMessage(row.value, row.key)
				print("MESS SENT   " + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " number: " + row.key  + "            message: " + row.value)
				sys.stdout.flush()
			else:
				second.append(row)
		results = second
		sleep(1)
	if foreward > int(time()):
		sleep(foreward-int(time()))
		
