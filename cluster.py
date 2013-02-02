import tornado.ioloop
import tornado.web

from jinja2 import Environment, PackageLoader
env = Environment(loader=PackageLoader('cluster', 'templates'))
template = env.get_template('landingpage.html')


class MainHandler(tornado.web.RequestHandler):
	    def get(self):
		            self.write(template.render())

application = tornado.web.Application([
	    (r"/", MainHandler),
])

if __name__ == "__main__":
	    application.listen(1337)
	    tornado.ioloop.IOLoop.instance().start()

