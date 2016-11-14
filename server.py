import os
import tornado.ioloop
import tornado.web
import tornado.options

tornado.options.define("port", default=8888, help="jizz")

class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("index.html", message = '')

	def post(self):
		text = self.get_argument('text', '')
		self.render("index.html", message = text)

settings = {
	"static_path": os.path.join(os.path.dirname(__file__), "static"),
	"autoreload" : True,
	"debug"      : True
}

def main():
	tornado.options.parse_command_line()
	app = tornado.web.Application(
		[
			(r'/', IndexHandler),
		], **settings
	)

	app.listen(tornado.options.options.port)
	tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
	main()
