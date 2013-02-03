# vim: set ts=4 sw=4 noet

import tornado.auth
import tornado.autoreload
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from jinja2 import Environment, FileSystemLoader
from tornado.options import define, options

env = Environment(loader=FileSystemLoader('templates')) #load ./templates/
define("port", default=1337, help="run on the given port", type=int)

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
				(r"/", MainHandler),
				(r"/sign-up", InviteHandler),
				(r"/login", LoginHandler)
		]
		tornado.web.Application.__init__(self, handlers)


class MainHandler(tornado.web.RequestHandler):
	def get(self):
		template = env.get_template('landingpage.html')
		self.write(template.render())
		#self.write("hello world!")

class LoginHandler(tornado.web.RequestHandler):
	def post(self):
		if not self.user.is_logged_in():
			raise tornado.web.HTTPError(403)			

class InviteHandler(tornado.web.RequestHandler):
	def post(self):
		self.set_header("Content-Type","text/plain")
		self.write("The invitation code you entered was "+self.get_argument("invitecode"))

def main():
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
 	#watch for changes and reload the server
	tornado.autoreload.watch('templates/landingpage.html')
	tornado.autoreload.start()

	main()
