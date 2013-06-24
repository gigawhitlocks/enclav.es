# vim: set ts=4 sw=4 expandtab

import tornado.auth
import tornado.autoreload
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
from handlers import EnclaveHandler, PostHandler,\
        LandingPageHandler, UserHandler, ForgotPassHandler,\
        SettingsHandler, NewPostHandler, NewEnclaveHandler,\
        SignUpHandler, InviteHandler, LogoutHandler

from websockets import PostSocket, ChatSocket

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

        #######################################################
        #THIS IS WHERE ROUTES ARE DEFINED.
        #May want to move these elsewhere at some point,
        #but for now let's just highlight them with this comment.
        #######################################################
        handlers = [

            # static file routes
            (r"/css/(.*)", tornado.web.StaticFileHandler, {'path': 'static/css'}),
            (r"/images/(.*)", tornado.web.StaticFileHandler, {'path': 'static/images'}),
            (r"/js/(.*)", tornado.web.StaticFileHandler, {'path': 'static/js'}),
            (r"/html/(.*)", tornado.web.StaticFileHandler, {'path': 'static/html'}),

            # special routes
            (r"/", LandingPageHandler),
            (r"/forgot_password", ForgotPassHandler),
            (r"/sign-up", SignUpHandler), #maybe this should be sign_up? I like underscores..
            (r"/logout", LogoutHandler),
            (r"/invite", InviteHandler),
            (r"/settings", SettingsHandler),
            (r"/create_enclave", NewEnclaveHandler),
            (r"/new_post", NewPostHandler),

            # websocket routes
            (r"/\~.+/postws", PostSocket),
            (r"/\~.+/chatws", ChatSocket),

            # generated routes
            (r"/\~.+/new_post", NewPostHandler), # any URI starting with ~ will load an enclave
            (r"/\~.+", EnclaveHandler), # any URI starting with ~ will load an enclave
            (r"/p/.+", PostHandler), # any URI starting with /p/ will load an individual post
            (r"/u/.+", UserHandler) # any URI such that /[user]  will load an identity's profile page

        ]
        #######################################################
        #Also with this comment
        #######################################################



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



