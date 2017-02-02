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