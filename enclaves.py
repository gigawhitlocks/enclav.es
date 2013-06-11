# vim: set ts=4 sw=4 expandtab

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
from handlers import * 
import hashlib
from random import random

from bulbs.neo4jserver import Graph
from bulbs.model import Node, Relationship
from bulbs.property import String, DateTime, Integer
from users import User, check_password

"""

This file contains a few things:
  -The main method and Application class, along with runtime configs
  -Routing table
  -The Enclave object and related, to stick to the users.py posts.py etc naming scheme

"""



#define port for the server to run on
define("port", default=8000, help="run on the given port", type=int) 



class Application(tornado.web.Application):
  def __init__(self):
    settings = {
      'cookie_secret': "GOTTA HAVE MY COOKIE SECRETE", #todo: read in from elsewhere
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
        (r"/css/(.*)", tornado.web.StaticFileHandler, {'path': 'static/css'}),
        (r"/images/(.*)", tornado.web.StaticFileHandler, {'path': 'static/images'}),
        (r"/js/(.*)", tornado.web.StaticFileHandler, {'path': 'static/js'}),
        (r"/", LandingPageHandler),
        (r"/sign-up", SignUpHandler), #maybe this should be sign_up? I like underscores..
        (r"/logout", LogoutHandler),
        (r"/invite", InviteHandler),
        (r"/settings", SettingsHandler),
        (r"/new_post", NewPostHandler)
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
  tornado.autoreload.start()
  main()



#Enclave object and related are below
class Enclave(Node):
  created = DateTime(default=current_datetime, nullable=False)
  name = String(nullable=False)
  
  #gov_type will define government type for a given Enclave
  #Will hopefully eventually include Monarchy and Democracy at least
  #If not some combinations as well
  gov_type = String(nullable=False, default="monarchy")

  #determines whether or not subscribers can post
  membership_required = Integer(nullable=False, default=0)

  #determines whether posts in the enclave are visible to the wider community
  #when set to 1, membership_required is assumed to be 1
  private = Integer(nullable=False, default=0)
  
