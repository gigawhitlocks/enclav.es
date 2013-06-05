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
from clusterhandler import * 
#from session import *
import hashlib
from random import random

from bulbs.neo4jserver import Graph
from users import User, check_password

#load ./templates/

#define port for the server to run on
define("port", default=8000, help="run on the given port", type=int) 



class Application(tornado.web.Application):
	def __init__(self):
		settings = {
			'cookie_secret': "GOTTA HAVE MY COOKIE SECRETE",
	    "xsrf_cookies": False
		}

		"""
		#######################################################
		THIS IS WHERE ROUTES ARE DEFINED.
		May want to move these elsewhere at some point,
		but for now let's just highlight them with this comment.
		#######################################################
		"""
		handlers = [
				(r"/", LandingPageHandler),
				(r"/sign-up", SignUpHandler),
				(r"/logout", LogoutHandler),
				(r"/invite", InviteHandler)
		]
		"""
		#######################################################
		Also with this comment
		#######################################################
		"""



		tornado.web.Application.__init__(self, handlers,**settings)

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
