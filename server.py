import tornado.ioloop
import tornado.web
from twilio.rest import TwilioRestClient
import twilio.twiml




handlers = [(r"/", TextRequestHandler)]

app = tornado.web.Application(handlers)

if __name__ == "__main__":
    app.listen(80)
    tornado.ioloop.IOLoop.instance().start()