from nltk.stem.wordnet import WordNetLemmatizer as lemmatize
from nltk.corpus import wordnet as wn

class TagWord:

	def __init__(self):
		pass	

	def is_noun(tag):
		return tag in ['NN', 'NNS', 'NNP', 'NNPS']

	def is_verb(tag):
		return tag in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']

	def is_adverb(tag):
		return tag in ['RB', 'RBR', 'RBS']

	def is_adjective(tag):
		return tag in ['JJ', 'JJR', 'JJS']

	def get_tag(word):
		tag = '' 
		if is_adjective(tag):
			return 'ADJ'
		elif is_noun(tag):
			return 'NOUN'
		elif is_adverb(tag):
			return 'ADV'
		elif is_verb(tag):
			return 'VERB'
		return None
