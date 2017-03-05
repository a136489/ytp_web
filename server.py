import os
import tornado.ioloop
import tornado.web
import tornado.options

# import word2vec

## gensim ##
# import os
# import re
# import gensim, logging

# model = gensim.models.Word2Vec.load('HP')
# word_list = model.wv.index2word

# def modeling():
# 	l = []
# 	for word in word_list:
# 		l.append((word, model[word]))
# 	print(l)
# 	return l

# def similarity_query(in1, in2, out1):
# 	out2 = model.most_similar(positive=[out1, in2], negative=[in1], topn=1)[0][0]
# 	return out2
## gensim end ##

## tornado
tornado.options.define("port", default=8887, help="jizz")

class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		# l = modeling()
		self.render("index.html", message = '')

	def post(self):
		if(t1 in word_list and t2 in word_list and t3 in word_list):
			output = similarity_query(t1, t2, t3)
			print(output)
			self.render("index.html", message = output)
		else:
			error = "please choose words from CORPORA LIST"
			self.render("index.html", message = error)

class Gryffindor(tornado.web.RequestHandler):
	def get(self):
		self.render("gryffindor.html")

class Hufflepuff(tornado.web.RequestHandler):
	def get(self):
		self.render("hufflepuff.html")

class Ravenclaw(tornado.web.RequestHandler):
	def get(self):
		self.render("ravenclaw.html")

class Slytherin(tornado.web.RequestHandler):
	def get(self):
		self.render("slytherin.html")




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
