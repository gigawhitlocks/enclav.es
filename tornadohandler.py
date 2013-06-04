
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
from users import User, check_password, Invitee

import smtplib
from email.parser import Parser

import uuid


class ClusterHandler(tornado.web.RequestHandler):

	env = Environment(loader=FileSystemLoader('templates')) 

	"""
	Checks to see if a user is logged.
	"""
	def is_logged_in(self):
		return self.get_secure_cookie("username") != None
	
	"""
	Call at the beginning of a Handler to redirect non-users to 
	the site's homepage.
	"""
	def require_login(self):
		if (not self.is_logged_in()):
			self.redirect("/")

"""
LandingPageHandler handles all requests sent to the root of the domain.
This means displaying a login page when no user is logged in and the home page
for logged in users.

It also handles POST requests sent to the root, which is where logins are handled.
"""
class LandingPageHandler(ClusterHandler):

	"""
	Handles requests to the root of the site when visiting normally
	(GET requests)
	"""
	def get(self):
		if(not self.is_logged_in()):
			landingpage_template = self.env.get_template('landingpage.html')
			self.write(landingpage_template.render())
		else:
			self.set_header("Content-Type","text/html")
			header_template =	self.write(self.env.get_template('content.html').render())

	"""
	Session stores a cookie with the userID in the browser for persistent sessions.
	The redis bit is half-implemented.
	TODO: determine if server-side sessions are really even necessary
	"""
	def session(self):
		sessionid = self.get_secure_cookie('sid')
		return Session(self.application.session_store, sessionid)

	"""
	# handles POST requests sent to /
	# Generally these are login requests
	"""
	def post(self):
		if ( not self.is_logged_in() ):
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
"""
Destroys existing sessions
Send a GET to /logout to trigger this Handler
"""
class LogoutHandler(ClusterHandler):
	def get(self):
		self.clear_cookie("username")


"""
Handler for sending out invitation emails.
"""
class InviteHandler(ClusterHandler):
	def get(self):
		self.require_login()
		self.write(self.env.get_template("invite.html").render())
	def post(self):
		self.require_login()

		g = Graph()
		g.add_proxy("invitees", Invitee)
		currentinvitee = g.invitees.index.lookup(email=self.get_argument("email")) 

		if ( currentinvitee != None ):
			for current in currentinvitee:
				g.invitees.delete(current.eid)

		currentinvitee = g.invitees.create(email=self.get_argument("email"), token=uuid.uuid4().hex, invited_by=self.get_secure_cookie("username"))

		s = smtplib.SMTP('localhost')
		headers = Parser().parsestr('From: <noreply@cluster.im>\n'
        'To: <'+ self.get_argument("email") +'>\n'
        'Subject: You have been invited to Cluster.im\n'
        '\n'
				'Click here to accept the invitation: http://localhost:8080/sign-up?token='+currentinvitee.token+'\n')

		s.sendmail(headers['from'],[headers['to']],headers.as_string())
		self.redirect("/invite")

"""
The GET method in this Handler is for users who wish to send invites.
POST handles the form on the landing page for new users signing up.
This design is kind of dumb, maybe things should be moved around, IDK.
"""

class SignUpHandler(ClusterHandler):
	def post(self):
		self.set_header("Content-Type","text/plain")
		self.write("The invitation code you entered was "+self.get_argument("invitecode"))

	def get(self):
		graph = Graph()
		graph.add_proxy("invitees", Invitee)
		currentinvitee = graph.invitees.index.lookup(token=self.get_argument("token"))
		if ( currentinvitee == None ) :
			self.redirect("/")
		else:
			## do stuff
			self.write("Success!")

			## to do: also check expiry on token
			## destroy token after use, either way
			## load template for actual user signup form


