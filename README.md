Text Reminder
=============

Remind Yourself via Text Message. This is a service I built to help remind me of things to do. You can text it a date, time, and message, and it will send you back the message that date and time.

How it Works:
---

Text Reminder is written in python and running on an aws instance. It uses couchdb to store the message, and twilio to handle the sms messages. You can test out the app by sending the message to `703-940-0998`. To format the message, place the date and time before three periods and a space. Then write the message.

`"dateString"... "message"`
### Date Examples

+ `Today at 6 pm`
+ `Tomorrow at 9:30 pm`
+ `Wednesday a 10 am`
+ `7/13/13 at 4:20 pm`

Including a date without at time will default to midnight

### Complete Example

+ `Today at 6:30 pm... Take out the trash`
+ `Monday at 9 pm... Turn in english paper`
+ `8/24/13... Feed neighbor's cat`

Dependencies
---
+ [Tornado Web Framework](http://www.tornadoweb.org/en/stable/)
+ [CouchDB Server](http://couchdb.apache.org/)
+ [CouchDB for Python](https://pypi.python.org/pypi/CouchDB/0.9)
+ [Wolfram Alpha for Python](https://pypi.python.org/pypi/wolframalpha/1.0.2)
+ [Python Unidecode](https://pypi.python.org/pypi/Unidecode/0.04.13)
+ [Twilio for Python](https://pypi.python.org/pypi/twilio/3.5.1)

API'S
---
+ [Wolfram Alpha API](http://products.wolframalpha.com/api/)
+ [Texas A&M Geocoding API](http://geoservices.tamu.edu/Services/Geocode/WebService/GeocoderWebService.aspx)
+ [World Weather Online Time Zone API](http://developer.worldweatheronline.com/)
+ [Twilio API](https://www.twilio.com/)

Installation
---
Start out by installing the python dependencies by running `./depend` to install the python dependencies. If that doesn't work, you can install them manually. Next, install a couchdb server running localy on the server. Next, register an account on twilio, and by a phone number. Be sure to point the number to your server in the setup. Next, get api keys for all of the apis listed above. Run `sh start.sh` to start the server.