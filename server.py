import os
import tornado.ioloop
import tornado.web
import tornado.options

import word2vec

tornado.options.define("port", default=8888, help="jizz")

class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("index.html", message = '')

	def post(self):
		text1 = self.get_argument('text1', '')
		text2 = self.get_argument('text2', '')
		text3 = self.get_argument('text3', '')

		output = word2vec.similarity_query(text1, text2, text3)

		self.render("index.html", message = output)

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
