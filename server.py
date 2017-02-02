import os
import tornado.ioloop
import tornado.web
import tornado.options

# import word2vec

## gensim ##
import os
import re
import gensim, logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class MySentences(object):
	def __init__(self, dirname):
		self.dirname = dirname

	def __iter__(self):
		for fname in os.listdir(self.dirname):
			for line in open(os.path.join(self.dirname, fname)):
				yield re.sub(r'[^\w]', ' ', line).split()

sentences = MySentences('text')
model = gensim.models.Word2Vec(sentences, min_count=1, size=40, batch_words=100)
word_list = model.wv.index2word

def modeling():
	return word_list

def similarity_query(in1, in2, out1):
	out2 = model.most_similar(positive=[out1, in2], negative=[in1], topn=1)[0][0]
	return out2
## gensim end ##

## tornado
tornado.options.define("port", default=8888, help="jizz")

class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("index.html", corpora = word_list, message = '')

	def post(self):
		output = ''
		error  = ''

		t1 = self.get_argument('text1', '')
		t2 = self.get_argument('text2', '')
		t3 = self.get_argument('text3', '')

		if(t1 in word_list and t2 in word_list and t3 in word_list):
			output = similarity_query(t1, t2, t3)
			print(output)
			self.render("index.html", corpora = word_list, message = output)
		else:
			error = "please choose words from CORPORA LIST"
			self.render("index.html", corpora = word_list, message = error)



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
