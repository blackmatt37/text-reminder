import tornado.ioloop
import tornado.web
from twilio.rest import TwilioRestClient
import twilio.twiml
import couchdb
import wolframalpha
import datetime
from urllib import urlopen
import json
import unidecode

appid = '8K6X8G-EJTYLE4A5X'
geo_api = '41dcda96a31342769ddb337521599595'
wwo_key = '3w7q9es8u5ewpkg8vu488maq'

def getTime(timeString):
	client = wolframalpha.Client(appid)
	res = client.query(timeString)
	return int(res.pods[1].text.split(" ")[0])

def geocode(zipCode):
    response = urlopen("https://geoservices.tamu.edu/Services/Geocode/WebService/GeocoderWebServiceHttpNonParsed_V04_01.aspx?apiKey=" + geo_api + "&zip=" + zipCode + "&version=4.01").read().split(",")
    return float(response[3]), float(response[4])


def timeZone(zipCode):
	j = urlopen("http://api.worldweatheronline.com/free/v1/tz.ashx?q=" + zipCode + "&format=json&key=" + wwo_key)
	return str(int(float(unidecode.unidecode(json.load(j)['data']['time_zone'][0]['utcOffset']))))

class TextRequestHandler(tornado.web.RequestHandler):
	def get(self):
		server = couchdb.client.Server()
		db = server['texter']
		message = str(self.get_argument("Body"))
		number = str(self.get_argument("From"))
		zipcode = str(self.get_argument("FromZip"))
		print("GET REQUEST " + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " number: " + number  " zip: " + zipcode + " message: " + message)
		sys.stdout.flush()
		zone = timeZone(zipcode)
		entry = {}
		entry['number'] = number
		split = message.split("... ")
		time = getTime("convert " + split[0] + "UTC" + zone + " to unix time")
		entry['time'] = time
		entry['message'] = split[1]
		entry['done'] = "false"
		db[str(time)] = entry
		resp = twilio.twiml.Response()
		formated = str(datetime.datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S'))
		resp.sms("Text scheduled at " + formated)
		self.write(str(resp))
	def post(self):
		self.write("hello")


handlers = [(r"/", TextRequestHandler)]

app = tornado.web.Application(handlers)

if __name__ == "__main__":
	app.listen(80)
	tornado.ioloop.IOLoop.instance().start()
