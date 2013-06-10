
import tornado.auth
import tornado.autoreload
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

from bulbs.neo4jserver import Graph
import redis


import hashlib
from jinja2 import Environment, FileSystemLoader
from users import *
from posts import *
import smtplib
from email.parser import Parser

import uuid


class EnclavesHandler(tornado.web.RequestHandler):
	graph = Graph()
	graph.add_proxy("invitees", Invitee)
	graph.add_proxy("invited", Invited)
	graph.add_proxy("Is", Is)
	graph.add_proxy("users",User)
	graph.add_proxy("identities",Identity)


	graph.add_proxy("link_posts",LinkPost)

	graph.scripts.update("traversals.groovy")
	env = Environment(loader=FileSystemLoader('templates')) 

	"""
	Checks to see if a user is logged in.
	"""
	def is_logged_in(self):
		return self.get_secure_cookie("userid") != None


	"""
	Use for throwing a 403 when a user does something that is not permitted
	"""
	def forbidden(self):
		self.clear()
		self.set_status(403)
		self.finish("<html><body><h3>403 That is not permitted</h1></body></html>")

	"""
	Use as a decorator around functions that require the user be logged in
	"""
	@staticmethod
	def require_login(function):
		def new_function(self):
			if (not self.is_logged_in()):
				self.forbidden()
			function(self)
		return new_function
"""
LandingPageHandler handles all requests sent to the root of the domain.
This means displaying a login page when no user is logged in and the home page
for logged in users.

It also handles POST requests sent to the root, which is where logins are handled.
"""
class LandingPageHandler(EnclavesHandler):

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
			header_template =	self.write(self.env.get_template('content.html').render(posts=self.graph.link_posts.get_all()))

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
			# open database and look up input username
			self.set_header("Content-Type", "text/html")
			user = self.graph.users.index.get_unique(userid=self.get_argument("username")) 
			if ( user == None ):
				self.write("Username or password was incorrect.\n")
			else :

				# check that password is correct
				if check_password(self.get_argument("password"),user.password):
					# save the session cookie
					self.set_secure_cookie("userid", user.userid)
					self.redirect("/")
				else:
					self.write("Username or password was incorrect.\n")
"""
Destroys existing sessions
Send a GET to /logout to trigger this Handler
"""
class LogoutHandler(EnclavesHandler):
	def get(self):
		self.clear_cookie("userid")
		self.redirect("/")

"""
Handler for sending out invitation emails.
"""
class InviteHandler(EnclavesHandler):
	"""
		This loads the invitation creation dialog, for existing users to send invitations
	"""
	@EnclavesHandler.require_login	
	def get(self):
		self.write(self.env.get_template("invite.html").render())
	"""
	This actually sends out the email when the existing user clicks 'send'
	"""
	@EnclavesHandler.require_login	
	def post(self):

		currentinvitee = self.graph.invitees.index.lookup(email=self.get_argument("email")) 
		# check to see if this email has already been invited. If it has, remove all of its previos occurrences
		if ( currentinvitee is not None ):
			for current in currentinvitee:
				self.graph.invitees.delete(current.eid)


		#creates an Invitee object with the given email and a generated uuid
		currentinvitee = self.graph.invitees.create(
											email=self.get_argument("email"), 
											token=uuid.uuid4().hex) #TODO: Does this need to be more secure?

		currentuser = self.graph.users.index.lookup(userid=self.get_secure_cookie("userid")).next()
		self.graph.invited.create(currentuser, currentinvitee)

		## build the email and send it. SMTP host is localhost for now.
		s = smtplib.SMTP('localhost')
		headers = Parser().parsestr('From: <noreply@cluster.im>\n'
        'To: <'+ self.get_argument("email") +'>\n'
        'Subject: You have been invited to Cluster.im\n'
        '\n'
				## TODO: Write out a better invite email
				'Click here to accept the invitation: http://localhost:8080/sign-up?token='+currentinvitee.token+'\n')

		s.sendmail(headers['from'],[headers['to']],headers.as_string())
		self.redirect("/invite")

"""
This route handles incoming new users sent from their email to sign-up/?token=[generated token]
"""
class SignUpHandler(EnclavesHandler):

	#This checks to make sure the provided token is valid
	def get(self):
		currentinvitee = self.graph.invitees.index.lookup(token=self.get_argument("token"))
		if ( currentinvitee is None ) :
			self.redirect("/")
		else:
			## If the token is valid load the new user form
			self.set_secure_cookie("token",self.get_argument("token"))
			self.write(self.env.get_template('sign-up.html').render())
			## TODO: also check expiry on token


	#This processes the new user form and creates the new user if the username isn't taken already	
	def post(self):
		
		invitee = self.graph.invitees.index.lookup(token=self.get_secure_cookie("token"))
		if (invitee is None):
			self.forbidden()
		else:
			newuser = self.graph.identities.index.lookup(identity=self.get_argument("userid"))
			if newuser is not None:
				self.write("Handle is taken")
			else:
				newuser = self.graph.users.create(
						userid=self.get_argument("userid"),
						password=generate_storable_password(self.get_argument("password")))
				

				
				get_inviter = self.graph.scripts.get('getInviter')
				inviter = self.graph.gremlin.query(get_inviter, dict(_id=invitee.next().eid)).next()
				self.graph.invited.create(inviter,newuser)

				# creates an Identity with the same name as the initial username
				self.graph.Is.create(newuser,self.graph.identities.create(identity=newuser.userid))
				
				self.clear_cookie("token")
				self.clear_cookie("userid")
				for i in invitee:
					self.graph.invitees.delete(i.eid)

				self.redirect("/")

class NewPostHandler(EnclavesHandler):

	@EnclavesHandler.require_login
	def get(self):
		self.write(self.env.get_template('new_post.html').render())
	
	@EnclavesHandler.require_login
	def post(self):
		newpost = self.graph.link_posts.create(
								title=self.get_argument("title"),
								url=self.get_argument("url"))
			
class SettingsHandler(EnclavesHandler):
	def get(self):
		pass
