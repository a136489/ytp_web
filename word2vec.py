import os
import re
import gensim, logging
import numpy
from stop_words import get_stop_words
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

stop_words = get_stop_words('en')


class MySentences(object):
	def __init__(self, dirname):
		self.dirname = dirname

	def __iter__(self):
		for fname in os.listdir(self.dirname):
			for line in open(os.path.join(self.dirname, fname)):
				yield re.sub(r'[^\w]', ' ', line).split()



sentences = MySentences('text')
# model = gensim.models.Word2Vec(sentences, min_count=1, size=40, batch_words=100)
model = gensim.models.Word2Vec.load('HP_wikia')
# model.save('a')

word_list = model.wv.index2word

def modeling():
	
	return word_list


def similarity_query(in1, in2, out1):

	out2 = model.most_similar(positive=[out1, in2], negative=[in1], topn=1)[0][0]
	
	return out2

# print(model.most_similar('Hufflepuff', topn=20))

h_noun = {
		'g': ['bravery', 'nerve', 'chivalry', 'courage', 'daring'],
		's': ['cunning', 'ambition', 'determination', 'cleverness'],
		'h': ['dedication', 'patience', 'kindness', 'tolerance', 'loyalty'],
		'r': ['intelligence', 'wit', 'wisdom', 'creativity', 'acceptance']
}

h_adj = {
		'g': ['brave', 'nervous', 'courageous', 'daring'],
		's': ['cunning', 'ambitious', 'determined', 'clever'],
		'h': ['dedicated', 'patient', 'kind', 'tolerant', 'loyal'],
		'r': ['intelligent' ,'wise' ,'creative', 'original', 'individual', 'acceptable']
}

def dis(word):
	mini = 9999
	for house in h:
		mean = 0.0
		for att in h[house]:
			mean += numpy.linalg.norm(model[word] - model[att])
			# print()
		mean /= len(h[house])
		if mean < mini:
			mini = mean
			mini_house = house

	return (mini_house, mini)
	
# h = h_adj
# for i in h:
# 	for ii in h[i]:
# 		print(i, ii, dis(ii))
# 	print()
	
h = h_noun
for i in h:
	for ii in h[i]:
		print(i, ii, dis(ii))
	print()

# print(numpy.linalg.norm(model['loyalty'] - model['dedication']))
# print(numpy.linalg.norm(model['loyalty'] - model['patience']))
# print(numpy.linalg.norm(model['loyalty'] - model['kindness']))
# print(numpy.linalg.norm(model['loyalty'] - model['tolerance']))
# print(numpy.linalg.norm(model['loyalty'] - model['loyalty']))
