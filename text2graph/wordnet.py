from nltk.parse import stanford

from graph import Graph

from nltk.stem.wordnet import WordNetLemmatizer as lemmatize

import nltk
from word import Word

class Word:
	def __init__(self, Word, Type):
		self.word = Word
		self.type = Type

class Connection:
	def __init__(self, Word, Adds):
		self.word = Word
		self.adds = Adds

class WordNet:
	parser = stanford.StanfordParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
	
	@staticmethod
	def environment():
		os.environ["STANFORDTOOLSDIR"] = os.environ["HOME"]
		os.environ["CLASSPATH"] = os.environ["STANFORDTOOLSDIR"] + "/stanford-postagger-full-2015-04-20/stanford-postagger.jar:" + os.environ["STANFORDTOOLSDIR"] + "/stanford-ner-2015-04-20/stanford-ner.jar:" + os.environ["STANFORDTOOLSDIR"] + "/stanford-parser-full-2015-04-20/stanford-parser.jar:" + os.environ["STANFORDTOOLSDIR"] + "/stanford-parser-full-2015-04-20/stanford-parser-3.5.2-models.jar"
		os.environ["STANFORD_MODELS"] = os.environ["STANFORDTOOLSDIR"] + "/stanford-postagger-full-2015-04-20/models:" + os.environ["STANFORDTOOLSDIR"] + "/stanford-ner-2015-04-20/classifiers"

	def __init__(self):
		return None	
	def __get_sentences(self, data):
		return nltk.tokenize.sent_tokenize(data)

	# TODO: analyzer must work with complex sentences
	def analyze_sentence(self, sentence):
		new_edges = Graph()

		sentences = parser.raw_parse_sents((sentence, ""))

		for line in sentences:
			for sentence in line:
				
				return new_edges

	@staticmethod
	def analyze_sentence_parse_tree(tree):
		graph = Graph()
		node1, action, node2 = Node (), Edge (), Node ()
		for part in tree.subtrees():
			if part.label() == "NP": # Noun Phrase
				node1 = parse_NP (part)
			elif part.label () == "VP": # Verb Phrase
				(action, node2) = parse_VP (part)


	def analyze(self, text):
		new_edges = Graph()
		
		sentences = self.__get_sentences(text)

		for sentence in sentences:
			new_edges = merge (new_edges, self.analyze_sentence(self.__sentence_to_tag_sentence(sentence)))

		return new_edges
