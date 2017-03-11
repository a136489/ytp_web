import os
import tornado.ioloop
import tornado.web
import tornado.options

import text2house

tornado.options.define("port", default=8887, help="jizz")

class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("index.html", error = "")

	def post(self):
		self_intro = self.get_argument('self-intro')
		print(text2house.text2house(self_intro), "jizzzz")

		result = text2house.text2house(self_intro)
		if (result != 'e' and result != 'jerr'):
			tested = True
			page = result + ".html"
			self.render(page, tested = tested)
		else:
			print(result, "jizzjjjizjz")
			errors = {
				'e': '"Please say something."',
				'jerr': '"I cannot figure out which house you belong in, maybe you should say more things about you."'
			}
			self.render('index.html', error = errors[result])



class Gryffindor(tornado.web.RequestHandler):
	def get(self):
		tested = False
		self.render("gryffindor.html", tested = tested)

class Hufflepuff(tornado.web.RequestHandler):
	def get(self):
		tested = False
		self.render("hufflepuff.html", tested = tested)

class Ravenclaw(tornado.web.RequestHandler):
	def get(self):
		tested = False
		self.render("ravenclaw.html", tested = tested)

class Slytherin(tornado.web.RequestHandler):
	def get(self):
		tested = False 
		self.render("slytherin.html", tested = tested)


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
			(r'/gryffindor', Gryffindor), 
			(r'/hufflepuff', Hufflepuff),
			(r'/ravenclaw', Ravenclaw),
			(r'/slytherin', Slytherin),
		], **settings
	)

	app.listen(tornado.options.options.port)
	tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
	main()
