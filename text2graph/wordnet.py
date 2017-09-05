from graph import Graph

from nltk.stem.wordnet import WordNetLemmatizer as lemmatize

import nltk
#from word import TagWord

class Word:
	def __init__(self, Word, Type):
		self.word = Word
		self.type = Type
class Connection:
	def __init__(self, Word, Adds):
		self.word = Word
		self.adds = Adds

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
		return (tokenizer.tokenize(data))

	# TODO: analyzer must work with complex sentences
	def analyze_tag_sentence(self, sentence):
		new_edges = Graph()
		
		actioners = []
		action = None

		adjectives = []

		sentence.append(Word('', 'noun'))

		for x in sentence:
			if x.word == 'a' and x.type == 'article':
				continue
			elif x.type == 'article':
				raise BaseException('Undefined behaviour on ' + x.word + ' as ' + x.type)
			elif x.type == 'adj':
				adjectives.append(x.word)
				new_edges.add_node(x.word)	
			elif x.type == 'noun':
				if x.word == '':
					if len(adjectives) == 1:
						actioners.append(new_edges.add_node(adjectives[0]))
						adjectives = []
				else:
					actioners.append(new_edges.add_node(x.word))

					for each in adjectives:
						new_edges.add_edge(Connection('be', []), x.word, each)

					adjectives = []
			elif x.type == 'verb':
				action = Connection(x.word, [])
			else:
				raise BaseException('Undefined behaviour on ' + x.word + ' as ' + x.type)

		new_edges.add_edge(action, actioners[0], actioners[1])

		return new_edges

	def __sentence_to_tag_sentence(self, sentence):
		raise BaseException('Not implemented exception')

	def analyze(self, text):
		new_edges = Graph()
		
		sentences = self.__get_sentences(text)

		for sentence in sentences:
			new_edges.add_edges(self.analyze_tag_sentence(self.__sentence_to_tag_sentence(sentence)))

		return new_edges

	def add_edges(self, graph):
		self.graph.add_edges(graph)
