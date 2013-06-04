
import tornado.auth
import tornado.autoreload
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
from bulbs.neo4jserver import Graph
from session import *
import redis
import hashlib
from jinja2 import Environment, FileSystemLoader
from users import User, check_password

class ClusterHandler(tornado.web.RequestHandler):
	env = Environment(loader=FileSystemLoader('templates')) 
	def is_logged_in(self):
		return self.get_secure_cookie("username") != None
	

class LandingPageHandler(ClusterHandler):
	# handles GET requests sent to /
	def get(self):
		if(self.get_secure_cookie("username") == None):
			## we aren't logged in; load the landing page:
			landingpage_template = self.env.get_template('landingpage.html')
			self.write(landingpage_template.render())

		else:
			## a user is logged in
			self.set_header("Content-Type","text/html")
			header_template =	self.write(self.env.get_template('content.html').render())
	#		self.write('Thank you for logging in, %s.' %self.get_current_user())

	def session(self):
		sessionid = self.get_secure_cookie('sid')
		return Session(self.application.session_store, sessionid)

	# handles POST requests sent to /
	# Generally these are login requests
	def post(self):
#		header_template = self.env.get_template('content.html')
#		self.write(header_template.render())
		if (not self.is_logged_in()):
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

class LogoutHandler(ClusterHandler):
	def get(self):
		self.clear_cookie("username")

class SendInviteHandler(ClusterHandler):
	def post(self):
		if (not self.is_logged_in()):
			return None

class InviteHandler(ClusterHandler):
	def get(self):
		if (not self.is_logged_in()):
			self.write(self.env.get_template("landingpage.html").render())
		else:
			self.write(self.env.get_template("invite.html").render())

	def post(self):
		self.set_header("Content-Type","text/plain")
		self.write("The invitation code you entered was "+self.get_argument("invitecode"))

