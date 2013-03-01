# vim: set ts=4 sw=4 noet

import tornado.auth
import tornado.autoreload
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import redis

from tornado.options import define, options
from jinja2 import Environment, FileSystemLoader
from session import *
import hashlib
from random import random

from bulbs.neo4jserver import Graph
from users import User

#load ./templates/
env = Environment(loader=FileSystemLoader('templates')) 

#define port for the server to run on
define("port", default=1337, help="run on the given port", type=int) 

#handles routes
class Application(tornado.web.Application):
	def __init__(self):
		settings = {
			'cookie_secret': hashlib.sha512(str(random())).hexdigest()
		}
		self.redis = redis.StrictRedis()
		self.session_store = RedisSessionStore(self.redis)

		handlers = [
				(r"/", LandingPageHandler),
				(r"/sign-up", InviteHandler)
		]
		tornado.web.Application.__init__(self, handlers,**settings)


class LandingPageHandler(tornado.web.RequestHandler):
		
	# handles GET requests sent to /
	def get(self):
		if(self.get_current_user() == None):
			## we aren't logged in; load the landing page:
			landingpage_template = env.get_template('landingpage.html')
			self.write(landingpage_template.render())
		else:
			## a user is logged in
			self.set_header("Content-Type","text/plain")
			self.write("The current user is "+self.get_current_user())

	def get_current_user(self):
		return self.session['user'] if self.session and 'user' in self.session else None
 
	@property
	def session(self):
		sessionid = self.get_secure_cookie('sid')
		return Session(self.application.session_store, sessionid)

	# handles POST requests sent to /
	def post(self):
		if (self.get_current_user() == None):
			# Sets up the graph db
			graph = Graph()
			graph.add_proxy("users",User)
			self.set_header("Content-Type", "text/html")
			user = graph.users.index.get_unique(name=self.get_argument("username")) 
			if ( user == None ):
				self.write("No such user exists\n")
			else :
				self.write("The userid of "+user.name+" is "+user.userid+"<br />")
				
			self.write("The username you entered was " + self.get_argument("username") + "<br />")
			self.write("The password you entered was " + self.get_argument("password") + "<br />")
			## instead of raising an error, we should authenticate here
			## with the information passed via POST

		## else we're already logged in		
			## in this case we're probably handling a POST from a different form
			## and we can deal with that as needed	

class InviteHandler(tornado.web.RequestHandler):
	def post(self):
		self.set_header("Content-Type","text/plain")
		self.write("The invitation code you entered was "+self.get_argument("invitecode"))

def main():
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()

#start everything up
if __name__ == "__main__":
 	#watch for changes and reload the server
	tornado.autoreload.watch('templates/landingpage.html')
	tornado.autoreload.start()

	main()
