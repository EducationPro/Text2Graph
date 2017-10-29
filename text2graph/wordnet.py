from node import Node
from multi_node import MultiNode, NodeToMultiNode, simplify 
import os

class WordNet:
	
	@staticmethod
	def environment():
		os.environ["STANFORDTOOLSDIR"] = os.environ["HOME"]
		os.environ["CLASSPATH"] = os.environ["STANFORDTOOLSDIR"] + "/stanford-postagger-full-2015-04-20/stanford-postagger.jar:" + os.environ["STANFORDTOOLSDIR"] + "/stanford-ner-2015-04-20/stanford-ner.jar:" + os.environ["STANFORDTOOLSDIR"] + "/stanford-parser-full-2015-04-20/stanford-parser.jar:" + os.environ["STANFORDTOOLSDIR"] + "/stanford-parser-full-2015-04-20/stanford-parser-3.5.2-models.jar"
		os.environ["STANFORD_MODELS"] = os.environ["STANFORDTOOLSDIR"] + "/stanford-postagger-full-2015-04-20/models:" + os.environ["STANFORDTOOLSDIR"] + "/stanford-ner-2015-04-20/classifiers"

	class Parse:
		@staticmethod
		def Sentences (text):
			from nltk.tokenize import sent_tokenize
			return sent_tokenize(text)

		@staticmethod
		def SentenceTree (sentence):
			from nltk.parse import stanford

			parser = stanford.StanfordParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
			for line in parser.raw_parse_sents((sentence, "")):
				return line
	
	class Analyze:

		@staticmethod
		def CombineTrees (multi_node, sentence_tree):
			# Object/Subject mentioning:
			if len(multi_node.nodes) > 1:
				if len(sentence_tree.nodes) == 1 and 'They' in sentence_tree.nodes [0].properties:
					extension_node = Node ()
					for x in sentence_tree.nodes [0].properties:
						extension_node.extendProperty (x)
					for x in sentence_tree.nodes [0].actions:
						extension_node.extendProperty (x)
					multi_node.extendNode (extension_node)
					return multi_node
				elif len(sentence_tree.nodes) == 1: # Визираме един от всички
					for NODE in sentence_tree.nodes:
						node = multi_node.findNode (hasProperties = NODE.properties)
						if node != None:
							node[-1].extendNode (NODE)
						else:
							multi_node.addNode (NODE)
				else:
					for x in sentence_tree.nodes:
						multi_node.addNode (x)
			elif len(multi_node.nodes) == 0:
				for x in sentence_tree.nodes:
					multi_node.addNode (x)
			else:
				for NODE in sentence_tree.nodes:
					node = multi_node.findNode (hasProperties = NODE.properties)
					if node != None:
						node[-1].extendNode (NODE)
					else:
						multi_node.addNode (NODE)

			return multi_node
		@staticmethod
		def Tree (trees):
			#print ()
			for tree in trees:
				if tree.label () == 'ROOT':
					for part in list(tree):
						if part.label () == 'S':
							return WordNet.Analyze.SentenceTree (part)
				elif tree.label () == 'S':
					return WordNet.Analyze.SentenceTree (tree)

		@staticmethod
		def SentenceTree (tree, node = None):
			print ("ST" + str(tree))
			node1, action, node2 = MultiNode ([Node()]), {}, MultiNode ([Node()])

			for part in list(tree):
				if part.label () == 'NP':
					node1 = WordNet.Analyze.NP (part)
					#print (str(node1))
				elif part.label () == '.' or part.label () == ',':
					continue
				elif part.label () == 'VP':
					(action, node2) = WordNet.Analyze.VP (part)

			print ("SentenceTree (start node: {3}): {0} -{1}-> {2}".format (node1, action, str(node2), node))
			if node != None:
				node1.extendNode (node)
			node1.extendAction (action, node2)
			print ("End ST")

			return node1

		@staticmethod
		def NP (tree, NODE = None):
			#print ("NP: " + str(tree))
			ans = []
			if NODE == None:
				node = MultiNode ([Node ()])
			else:
				node = MultiNode ([NODE])
			ind = 0
			for part in list(tree):
				if part.label () == 'SBAR':
					for i in list(part):
						if i.label () == 'S':
							#print ("SBAR: " + str(node))
							node.nodes[-1] = WordNet.Analyze.SentenceTree (i, node.nodes[-1])
							#print ("After SBAR: " + str(node))
				elif part.label () == '.' or part.label () == ',':
					continue
				elif part.label () == 'DT':
					continue
				elif part.label () == 'CC': # TODO: understand positive or negative is meaning of the CC word
					node.addNode (Node ())	
				elif part.label () == 'PP':
					node.nodes[-1] = WordNet.Analyze.PP (part, node.nodes[-1])
				elif part.label () == 'NP': # POS and node before SBAR
					if any (x.label () == 'POS' for x in list(part)):
						#print ("extend " + ''.join (part.leaves ()))
						node.nodes[-1].extendProperty (''.join (part.leaves ()))
					else: 
						#print ("extend " + str(part))
						node.nodes[-1] = WordNet.Analyze.NP (part, node.nodes[-1])
				else:
					for prop in part.leaves ():
						#print ("Property: " + prop)
						node.nodes[-1].extendProperty (prop)

				#ind += 1

			#print (tree)
			#print ('NP(s): ' + str(node))
			#print ("End NP")
			#if len(node.nodes) == 2 and NODE == None:
			#	return node.nodes [0]
			#else:
			return node
			return simplify(node)

		@staticmethod
		def PP (tree, node):
			action = {}

			for i in list(tree):
				if i.label () == 'IN':
					action = ''.join(i.leaves ())
				elif i.label () == '.' or i.label () == ',':
					continue
				elif i.label () == 'NP':
					node.extendAction(action, WordNet.Analyze.NP (i))

			return node

		@staticmethod
		def VP (tree):
			#print ("VP:" + str(tree))
			action, node = "", MultiNode ([])
			
			for part in list(tree):
				if part.label () == 'VP':
					children = {}
					for i in list(part):
						#print ("key: " + ''.join(i.leaves ()))
						children [''.join(i.leaves ())] = i
					if 'VP' in children:	
						action = action + list(children.keys ())[0]
					else:
						node.nodes.addNode (Node ())
						(suffix, node.nodes[-1]) = WordNet.Analyze.VP (part)
						action += ' ' + suffix
				elif part.label () == 'NP':
					node.addNode (WordNet.Analyze.NP (part, node.nodes[-1]))
				elif part.label () == 'PP':
					node.addNode (WordNet.Analyze.PP (part, node.nodes[-1]))
				elif part.label ()[0] == 'V':
					action = action + ''.join(part.leaves ())
				elif part.label () == '.' or part.label () == ',':
					continue
				elif part.label () == 'SBAR': # when/while
					continue
				else:
					node.nodes[-1].extendProperty (''.join(part.leaves ()))
					


			#print ("({0}, {1})".format (action, node))
			#print ("End VP")
			return (action, node)

