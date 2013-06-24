import tornado.ioloop
import tornado.web
from twilio.rest import TwilioRestClient
import twilio.twiml
import couchdb
import wolframalpha
import datetime

appid = '8K6X8G-EJTYLE4A5X'
def getTime(timeString):
	client = wolframalpha.Client(appid)
	res = client.query(timeString)
	return int(res.pods[1].text.split(" ")[0])

class TextRequestHandler(tornado.web.RequestHandler):
	def get(self):
		server = couchdb.client.Server()
		db = server['texter']
		message = str(self.get_argument("Body"))
		number = str(self.get_argument("From"))
		entry = {}
		entry['number'] = number
		split = message.split("... ")
		time = getTime("convert " + split[0] + " to unix time")
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
