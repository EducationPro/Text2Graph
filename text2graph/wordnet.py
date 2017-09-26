from node import Node
import os

class WordNet:
	
	@staticmethod
	def environment():
		os.environ["STANFORDTOOLSDIR"] = os.environ["HOME"]
		os.environ["CLASSPATH"] = os.environ["STANFORDTOOLSDIR"] + "/stanford-postagger-full-2015-04-20/stanford-postagger.jar:" + os.environ["STANFORDTOOLSDIR"] + "/stanford-ner-2015-04-20/stanford-ner.jar:" + os.environ["STANFORDTOOLSDIR"] + "/stanford-parser-full-2015-04-20/stanford-parser.jar:" + os.environ["STANFORDTOOLSDIR"] + "/stanford-parser-full-2015-04-20/stanford-parser-3.5.2-models.jar"
		os.environ["STANFORD_MODELS"] = os.environ["STANFORDTOOLSDIR"] + "/stanford-postagger-full-2015-04-20/models:" + os.environ["STANFORDTOOLSDIR"] + "/stanford-ner-2015-04-20/classifiers"

	class Parse:
		@staticmethod
		def SentenceTree (sentence):
			from nltk.parse import stanford

			parser = stanford.StanfordParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
			for line in parser.raw_parse_sents((sentence, "")):
				return line
	
	class Analyze:

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
			#print ("ST" + str(tree))
			node1, action, node2 = Node (), {}, Node ()

			for part in list(tree):
				if part.label () == 'NP':
					node1 = WordNet.Analyze.NP (part)
					#print (str(node1))
				elif part.label () == '.' or part.label () == ',':
					continue
				elif part.label () == 'VP':
					(action, node2) = WordNet.Analyze.VP (part)

			#print ("SentenceTree (start node: {3}): {0} -{1}-> {2}".format (node1, action, str(node2), node))
			if node != None:
				node1.extendNode (node)
			node1.extendAction (action, node2)
			#print ("End ST")

			return node1

		@staticmethod
		def NP (tree, NODE = None):
			#print ("NP: " + str(tree))
			ans = []
			if NODE == None:
				node = Node ()
			else:
				node = NODE
			ind = 0
			for part in list(tree):
				if part.label () == 'SBAR': 	
					for i in list(part):
						if i.label () == 'S':
							#print ("SBAR: " + str(node))
							node = WordNet.Analyze.SentenceTree (i, node)
							#print ("After SBAR: " + str(node))
				elif part.label () == '.' or part.label () == ',':
					continue
				elif part.label () == 'DT':
				  continue
				elif part.label () == 'CC': # TODO: understand positive or negative is meaning of the CC word
					#if ind > 0:
					#	ans.append (node)
					#	node = Node ()
					continue
				elif part.label () == 'PP':
					node = WordNet.Analyze.PP (part, node)
				elif part.label () == 'NP': # POS and node before SBAR
					if any (x.label () == 'POS' for x in list(part)):
						#print ("extend " + ''.join (part.leaves ()))
						node.extendProperty (''.join (part.leaves ()))
					else: 
						#print ("extend " + str(part))
						node = WordNet.Analyze.NP (part, node)
				else:
					for prop in part.leaves ():
						#print ("Property: " + prop)
						node.extendProperty (prop)

				#ind += 1

			#print (tree)
			#print ('NP(s): ' + str(node))
			#print ("End NP")
			return node

		@staticmethod
		def PP (tree, node):
			action = {}

			for i in list(tree):
				if i.label () == 'IN':
					action = ''.join(i.leaves ())
				elif part.label () == '.' or part.label () == ',':
					continue
				elif i.label () == 'NP':
					node.extendAction(action, WordNet.Analyze.NP (i))

			return node

		@staticmethod
		def VP (tree):
			#print ("VP:" + str(tree))
			action, node = "", Node ()
			
			for part in list(tree):
				if part.label () == 'VP':
					children = {}
					for i in list(part):
						#print ("key: " + ''.join(i.leaves ()))
						children [''.join(i.leaves ())] = i
					if 'VP' in children:	
						action = action + list(children.keys ())[0]
					else:
						(suffix, node) = WordNet.Analyze.VP (part)
						action += suffix
				elif part.label () == 'NP':
					node = WordNet.Analyze.NP (part, node)
				elif part.label () == 'PP':
					node = WordNet.Analyze.PP (part, node)
				elif part.label ()[0] == 'V':
					action = action + ''.join(part.leaves ())
				elif part.label () == '.' or part.label () == ',':
					continue
				else:
					node.extendProperty (''.join(part.leaves ()))
					


			#print ("({0}, {1})".format (action, node))
			#print ("End VP")
			return (action, node)

