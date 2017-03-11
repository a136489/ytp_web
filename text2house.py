import gensim, logging
import numpy
from stop_words import get_stop_words
import re
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

stop_words = get_stop_words('en')

model = gensim.models.Word2Vec.load('model')
h_mix = {
		'g': ['brave', 'courageous', 'daring','clever','intelligent','fire','lion','red','gold','reckless','bravery', 'chivalry', 'courage','cleverness','leadership','hero','heroic','adventurous'],
		's': ['cunning', 'ambitious', 'determined', 'clever','snake','water','antagonist','green','silver','ambition', 'determination', 'cleverness'],
		'h': ['dedicated', 'patient', 'tolerant', 'loyal','humble','friendly','decent','earth','badger','yellow','black','dedication', 'patience', 'kindness', 'tolerance', 'loyalty'],
		'r': ['intelligent' ,'wise' ,'creative', 'original', 'individual','arrogant','eagle','air','blue','brown','bronze','black','intelligence', 'wit', 'wisdom', 'creativity']
}
h = h_mix

def judge(points,mode):
	result='g'
	summ=0.0
	for house in points:
		summ+=points[house]
	if mode==3:
		for house in points:
			if points[house] <= points[result]:
				result = house
				resultnum=points[house]
	elif mode==2:
		for house in points:
			if points[house] > points[result]:
				result = house
				resultnum=points[house]
	if summ==0:
		return 'jerr'#judge err
	else:
		return result

def dist1(word, house):
	mean = 0.0
	n=0
	for attr in h[house]:
		mean += numpy.linalg.norm(model[attr] - model[word])
		n=n+1
	mean /= len(h[house])
	return mean
def dist2(word,house):
	minn = 1000
	try:
			tmp=model[word]
	except:
		# print(word)
		return 1000
	for attr in h[house]:
		minn = min(minn,numpy.linalg.norm(model[attr] - tmp))
	return minn
#split valid word
def text_pre_process(text):
	words = re.sub(r'[^\w]', ' ', str(text)).lower().split()
	tmp = []
	for word in words:
		if word not in stop_words:
			tmp.append(word)
	valid_words = tmp[:]
	# print(valid_words)
	return valid_words
# Algorithm 1 total and mean
def A1(wrods):
	# print('Algorithm1')
	total = { 'g': 0.0, 's': 0.0, 'h': 0.0, 'r': 0.0 }
	for word in words:
		try:
			for house in h:
				total[house] += dist1(word, house)
		except:
			continue

	result1 = 'g'
	for house in total:
		if total[house] < total[result1]:
			result1 = house
	# print()
	# print(total)
	# print('result1:', result1)
	return result1



# Algorithm 2 
def A2(words):
	Min_thr=10
	# print('Algorithm2')
	valid_words = { 'g': [], 's': [], 'h': [], 'r': [] }
	score = { 'g': 0, 's': 0, 'h': 0, 'r': 0 }
	for word in words:
		try:
			if word == 'harry':
				continue
			flag = False
			for house in h:
				if flag == False:
					flag = True
					min_house = house
					min_dist = dist1(word, house)
				else:
					tmp_dist = dist1(word, house)
					if tmp_dist < min_dist:
						min_house = house
						min_dist = tmp_dist
			if min_dist < 5:
				score[min_house] += 1
				valid_words[min_house].append((word, min_dist))
		except:
			continue
	# print('validwords',valid_words)

	result2=judge(score,2)
	# print()
	# print(score)
	# print('result2:', result2)
	# print('Min_thr:',Min_thr)
	return result2
	
#Algorithm3
def A3(words):
	nstdthr = 0.17
	# print('Algorithm3')
	distance = { 'g': 0, 's': 0, 'h': 0, 'r': 0 }
	for word in words:
		try:
			tmpd=[]
			tmpdis={ 'g': 0, 's': 0, 'h': 0, 'r': 0 }
			mean=0
			for house in h:
				minn = dist2(word,house)
				tmpd.append(minn)
				# print(word,house,minn)
				tmpdis[house]=minn
				mean+=minn
			mean/=4
			nstd=numpy.std(tmpd)
			if mean<7 and nstd >nstdthr:
				# print(word,':::')
				# print(tmpdis)
				# print(nstd,'aaaaa')
				for house in h:
					distance[house]+=tmpdis[house]
		except:
			print('uhhhhh jizzzing in A3:',word)		
	result3=judge(distance,3)
	# print()
	# print(distance)
	# print('result3:', result3)
	# print('nstdthr:',nstdthr)
	# print('valid_num:',len(words))
	return result3
def text2house(text):
	if text=='':
		return 'e'#empty
	valid_words=text_pre_process(text)
	house=A3(valid_words)
	if house=='jerr':
		print('your house is remained undecided,maybe your age is under 30')
		return house
	else:
		houses = {
			'g': 'gryffindor',
			'h': 'hufflepuff',
			'r': 'ravenclaw',
			's': 'slytherin'
		}
		return houses[house]

# file=open('intro_texts/Hermione Granger','r')
# a=text2house(file.read())
# print(a)



