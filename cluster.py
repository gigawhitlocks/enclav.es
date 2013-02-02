# vim: set ts=4 sw=4 noet

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('landingpage.html')

from tornado.options import define, options

define("port", default=1337, help="run on the given port", type=int)

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.write(template.render())

def main():
	application = tornado.web.Application([
		(r"/", MainHandler),
	])
	http_server = tornado.httpserver.HTTPServer(application)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
	main()
