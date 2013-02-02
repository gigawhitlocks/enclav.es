# vim: set ts=4 sw=4 noet

import tornado.auth
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from jinja2 import Environment, FileSystemLoader
from tornado.options import define, options

env = Environment(loader=FileSystemLoader('templates')) #load ./templates/
template = env.get_template('landingpage.html')

define("port", default=1337, help="run on the given port", type=int)

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
				(r"/", MainHandler),
		]
		tornado.web.Application.__init__(self, handlers)

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("hello world!")
		#self.write(template.render())

def main():
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
	main()
