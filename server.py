import tornado.ioloop
import tornado.web
import twilio.twiml
import couchdb
import wolframalpha
import datetime
from urllib import urlopen
import json
import unidecode
from time import gmtime, strftime
import sys

# Wolfram Alpha API: http://products.wolframalpha.com/api/
- appid   = 'INSERT API KEY'
# Texam A&M Geocoding API: http://geoservices.tamu.edu/Services/Geocode/WebService/GeocoderWebService.aspx
- geo_api = 'INSERT API KEY'
# World Weather Online Time Zone API: http://developer.worldweatheronline.com/
- wwo_key = 'INSERT API KEY'


def getTime(timeString, zone):
	"""Returns the unix timestamp for free formed date and time"""
	client = wolframalpha.Client(appid)
	res = client.query("convert " + timeString + " UTC" + zone + " to unix time")
	return int(res.pods[1].text.split(" ")[0])

def geocode(zipCode):
	"""Returns the longitude and latitude given a zipcode"""
	response = urlopen("https://geoservices.tamu.edu/Services/Geocode/WebService/GeocoderWebServiceHttpNonParsed_V04_01.aspx?apiKey=" + geo_api + "&zip=" + zipCode + "&version=4.01").read().split(",")
	return float(response[3]), float(response[4])


def timeZone(zipCode):
	"""Returns a UTC time zone given a zipcode"""
	j = urlopen("http://api.worldweatheronline.com/free/v1/tz.ashx?q=" + zipCode + "&format=json&key=" + wwo_key)
	return str(int(float(unidecode.unidecode(json.load(j)['data']['time_zone'][0]['utcOffset']))))

class TextRequestHandler(tornado.web.RequestHandler):
	def get(self):
		# Connect to the local couchdb server. Running at http://localhost/:5984
		server = couchdb.client.Server()
		db = server['texter']

		# Retrive the fields from the twilio request
		message = str(self.get_argument("Body"))
		number = str(self.get_argument("From"))
		zipcode = str(self.get_argument("FromZip"))

		# Get the timezone and split the message from the date/time 
		zone = timeZone(zipcode)
		split = message.split("... ")
		# Gets the unix time stamp
		time = getTime(split[0], zone)

		# Writes the text message to the couchdb database
		entry = {}
		entry['number'] = number
		entry['time'] = time
		entry['message'] = split[1]
		entry['done'] = "false"
		db[str(time)] = entry

		# Logs the message
		print("GET REQUEST " + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " number: " + number + " zip: " + zipcode + " message: " + message)
		sys.stdout.flush()

		# Responds to the messages with a notice that the event is saved
		resp = twilio.twiml.Response()
		formated = str(datetime.datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S'))
		resp.sms("Text scheduled at " + formated)
		self.write(str(resp))

handlers = [(r"/", TextRequestHandler)]

app = tornado.web.Application(handlers)

if __name__ == "__main__":
	app.listen(80)
	tornado.ioloop.IOLoop.instance().start()