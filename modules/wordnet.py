from graph import Graph

from nltk.stem.wordnet import WordNetLemmatizer as lemmatize

import nltk
from word import TagWord

class WordNet:
	def __init__(self):
		self.words = dict()
		self.graph = Graph()
		
	def add_word(self, word):
		if word not in self.words:
			self.words[word] = len(self.words.keys())
		self.graph.add_node(self.words [word])

	def add_edge(self, edge_type, edge, to=None):
		if to == None:
			self.graph.add_edge(self.words[edge[0]]. self.words[edge[1]], weight=edge_type)
		else:
			self.graph.add_edge(self.words[edge]. self.words[to], weight=edge_type)

	def __get_sentences(self, data):
		tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
		print(tokenizer.tokenize(data))

	# TODO: analyzer must work with complex sentences
	def __analyze_sentence(self, sentence):
		new_edges = Graph()
			
		return new_edges

	def analyze(self, text):
		new_edges = Graph()
		
		sentences = self.__get_sentences(text)

		for sentence in sentences:
			new_edges.append(self.__analyze_sentence(sentence))

		return new_edges

	def add_edges(self, edges):
		raise NotImplementedError('WordNet.add_edges method is not implemented yet')


