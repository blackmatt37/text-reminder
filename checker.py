import couchdb
import time
from twilio.rest import TwilioRestClient



server = couchdb.client.Server("http://23.21.135.161:5984/")
db = server['texter']