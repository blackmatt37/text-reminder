import tornado.ioloop
import tornado.web
from twilio.rest import TwilioRestClient
import twilio.twiml

class TextRequestHandler(tornado.web.RequestHandler):
	def get(self):
		message = str(self.get_argument("Body"))
		resp = twilio.twiml.Response()
		resp.sms(message)
		self.write(str(resp))
	def post(self):
		self.write("hello")


handlers = [(r"/", TextRequestHandler)]

app = tornado.web.Application(handlers)

if __name__ == "__main__":
    app.listen(80)
    tornado.ioloop.IOLoop.instance().start()