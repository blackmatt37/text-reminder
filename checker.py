import couchdb
from time import time, sleep
from twilio.rest import TwilioRestClient

account_sid = 'AC954b92ab3aa3fe23cee06ae56b384019'
auth_token = 'b037fe51ee05147c69c806d78b3d9e95'

def sendMessage(message, number):
	client = TwilioRestClient(account_sid, auth_token)
	message = client.sms.messages.create(to=number, from_="7039400998", body=message)



while True:
	server = couchdb.client.Server("http://23.21.135.161:5984/")
	db = server['texter']
	map_fun = '''function(doc) {
		if(doc.time < ''' + str(int(time())) + ''' && doc.done == "false") {
			emit(doc.number, doc.message);
		}
	}'''
	results = db.query(map_fun)
	for row in results.rows:
		print int(time())
		doc = db[row.id]
		doc['done'] = 'true'
		db[row.id] = doc
		#sendMessage(row.value, row.key)

	sleep(15)
