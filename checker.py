import couchdb
from time import time, sleep, gmtime, strftime
from twilio.rest import TwilioRestClient
import sys

# Twilio API keys: https://www.twilio.com/
-account_sid = 'INSERT API KEY'
-auth_token  = 'INSERT API KEY'

# Checks the couchdb database every this many minutes for an sms to send 
advance = 2

def sendMessage(message, number):
	"""Uses twilio to send an sms with message to number"""
	client = TwilioRestClient(account_sid, auth_token)
	message = client.sms.messages.create(to=number, from_="PHONE NUMBER FROM TWILIO", body=message)

# Connect to the local couchdb server. Running at http://localhost/:5984
server = couchdb.client.Server()
db = server['texter']



while True:
	# Calculates the time in advance
	foreward = int(time()) + 60*advance
	
	# Gets the messages that are ready to be sent
	map_fun = '''function(doc) {
		if(doc.time < ''' + str(foreward) + ''' && doc.done == "false") {
			emit(doc.number, doc.message);
		}
	}'''
	results = db.query(map_fun).rows
	

	while int(time()) < foreward:
		second = []

		# Break the loop if there are no more messages to send in this cycle
		if len(results) == 0:
			break;
		for row in results:

			# If it is time to send one of the retrieved messages
			if int(row.id) < time():
				# Update the db
				doc = db[row.id]
				doc['done'] = 'true'
				db[row.id] = doc

				# Send the message to the correct number
				sendMessage(row.value, row.key)

				# Log that the message was sent
				print("MESS SENT   " + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " number: " + row.key  + "            message: " + row.value)
				sys.stdout.flush()
				
			else:
				second.append(row)
		results = second
		# Sleep another second, and see if there is a message to send the next second
		sleep(1)


	# If there is more time to wait until we check the db again
	if foreward > int(time()):
		# Wait the extra time
		sleep(foreward-int(time()))
		
