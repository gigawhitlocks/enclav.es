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
from users import User, check_password

#load ./templates/
env = Environment(loader=FileSystemLoader('templates')) 

#define port for the server to run on
define("port", default=8000, help="run on the given port", type=int) 

#handles routes
class Application(tornado.web.Application):
	def __init__(self):
		settings = {
			'cookie_secret': "GOTTA HAVE MY COOKIE SECRETE",
			#'cookie_secret': hashlib.sha512(str(random())).hexdigest(),
	    "xsrf_cookies": False
		}
		self.redis = redis.StrictRedis()
		self.session_store = RedisSessionStore(self.redis)

		handlers = [
				(r"/", LandingPageHandler),
				(r"/sign-up", InviteHandler),
				(r"/logout", LogoutHandler),
		]

		tornado.web.Application.__init__(self, handlers,**settings)

class LandingPageHandler(tornado.web.RequestHandler):
	def get_current_user(self):
		return self.get_secure_cookie("username")

	# handles GET requests sent to /
	def get(self):
		if(self.get_current_user() == None):
			## we aren't logged in; load the landing page:
			landingpage_template = env.get_template('landingpage.html')
			self.write(landingpage_template.render())

		else:
			## a user is logged in
			self.set_header("Content-Type","text/html")
			header_template = env.get_template('content.html')
			self.write(header_template.render())
	#		self.write('Thank you for logging in, %s.' %self.get_current_user())

	@property
	def session(self):
		sessionid = self.get_secure_cookie('sid')
		return Session(self.application.session_store, sessionid)

	# handles POST requests sent to /
	# Generally these are login requests
	def post(self):
#		header_template = env.get_template('content.html')
#		self.write(header_template.render())
		if (self.get_current_user() == None):
			# Sets up the graph db
			graph = Graph()
			graph.add_proxy("users",User)

			# open database and look up input username
			self.set_header("Content-Type", "text/html")
			user = graph.users.index.get_unique(userid=self.get_argument("username")) 
			if ( user == None ):
				self.write("No such user exists\n")
			else :

				# check that password is correct
				if check_password(self.get_argument("password"),user.password):

					# save the session cookie
					self.set_secure_cookie("username", user.userid)
					self.redirect("/")
				else:
					self.write("Password was incorrect")

class LogoutHandler(tornado.web.RequestHandler):
	def get(self):
		self.clear_cookie("username")

class InviteHandler(tornado.web.RequestHandler):
	def get(self):
		if (self.get_secure_cookie("username") == None):
			self.write(env.get_template("landingpage.html").render())
		else:
			self.write(env.get_template("invite.html").render())

	def post(self):
		# todo
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
