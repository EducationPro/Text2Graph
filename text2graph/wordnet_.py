from node import Node

class WordNet:
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
				elif part.label () == 'VP':
					(action, node2) = WordNet.Analyze.VP (part)

			#print ("SentenceTree (start node: {3}): {0} -{1}-> {2}".format (node1, action, str(node2), node))
			if node != None:
				node1.extendNode (node)
			node1.extendAction (action, node2)
			#print ("End ST")

			return node1

		@staticmethod
		def NP (tree):
			#print ("NP: " + str(tree))
			ans = []
			node = Node ()
			ind = 0
			for part in list(tree):
				if part.label () == 'NP':
					node = WordNet.Analyze.NP (part) 
				elif part.label () == 'SBAR': 	
					for i in list(part):
						if i.label () == 'S':
							#print ("SBAR: " + str(node))
							node = WordNet.Analyze.SentenceTree (i, node)
							#print ("After SBAR: " + str(node))
				elif part.label () == 'DT':
				  continue
				elif part.label () == 'CC': # TODO: understand positive or negative is meaning of the CC word
					#if ind > 0:
					#	ans.append (node)
					#	node = Node ()
					continue
				elif part.label () == 'PP':
					node = WordNet.Analyze.PP (part, node)
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
					node = WordNet.Analyze.NP (part)
				elif part.label () == 'PP':
					node = WordNet.Analyze.PP (part, node)
				else:
					action = action + ''.join(part.leaves ())


			#print ("({0}, {1})".format (action, node))
			#print ("End VP")
			return (action, node)

