from node import Node
from multi_node import MultiNode, NodeToMultiNode, simplify 
from pattern import PatternNode
import os

class WordNet:
	class Questions:

		class Parse:
			@staticmethod
			def Questions (text):
				from nltk.tokenize import sent_tokenize
				return sent_tokenize(text)

			@staticmethod
			def QuestionTree (sentence):
				from nltk.parse import stanford

				parser = stanford.StanfordParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
				for line in parser.raw_parse_sents((sentence, "")):
					return line

		class Match:
			
			@staticmethod
			def Properties (prop1, prop2):
				if len(prop2) == 0:
					return 1
				return sum([float(prop in prop1) for prop in prop2]) / len(prop2)

			@staticmethod
			def Node (node, pattern):
				pattern_from = pattern
				pattern_action = pattern.all_actions()[0]['action']
				pattern_to = pattern.all_actions()[0]['obj']

				percentage = 0
				percentage += WordNet.Questions.Match.Properties(node.all_properties(), pattern_from.all_properties()) 
				percentage += sum(
						[
							float(
								(
								 WordNet.Questions.Match.Properties(pair['obj'].all_properties(), pattern_to.all_properties()) 
								 + 
								 float(pattern_action == pair['action'])
								) / 2
							) for pair in node.actions
						]
				)
				return percentage
				

			@staticmethod
			def Pattern (tree, pattern):
				return sorted(tree.all_nodes (), key=lambda node: WordNet.Questions.Match.Node(node, pattern))[0]
				
		
		class Analyze:

			@staticmethod
			def Tree (trees):
				#print ()
				for tree in trees:
					if tree.label () == 'ROOT':
						for part in list(tree):
							if part.label () == 'SBARQ':
								for part1 in list(part):
									if part1.label () == 'SQ':
										return WordNet.Questions.Analyze.SentenceTree (part1)
					elif tree.label () == 'SBARQ':
						for part in list(tree):
							if part.label () == 'SQ':
								return WordNet.Questions.Analyze.SentenceTree (part)

			@staticmethod
			def SentenceTree (tree, node = None):
				print (tree.label ())
				print ("ST " + ' '.join ([' '.join(part.leaves ()) for part in list(tree)]))
				VBZ = ''
				node1, action, node2 = MultiNode ([Node()]), '', MultiNode ([PatternNode ()])

				for part in list(tree):
					if part.label () == 'NP':
						node1 = WordNet.Questions.Analyze.NP (part)
						#print (str(node1))
					elif part.label () == '.' or part.label () == ',':
						continue
					elif part.label ()[:2] == 'VB':
						VBZ = ''.join (part.leaves ())
					elif part.label () == 'VP':
						(action, node2) = WordNet.Questions.Analyze.VP (part)
						print ('action: ' + str(action))

				action = VBZ + ' ' + action
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
								node.nodes[-1] = WordNet.Questions.Analyze.SentenceTree (i, node.nodes[-1])
								#print ("After SBAR: " + str(node))
					elif part.label () == '.' or part.label () == ',':
						continue
					elif part.label () == 'DT':
						continue
					elif part.label () == 'CC': # TODO: understand positive or negative is meaning of the CC word
						node.addNode (Node ())	
					elif part.label () == 'PP':
						node.nodes[-1] = WordNet.Questions.Analyze.PP (part, node.nodes[-1])
					elif part.label () == 'NP': # POS and node before SBAR
						if any (x.label () == 'POS' for x in list(part)):
							#print ("extend " + ''.join (part.leaves ()))
							node.nodes[-1].extendProperty (''.join (part.leaves ()))
						else: 
							#print ("extend " + str(part))
							node.nodes[-1] = WordNet.Questions.Analyze.NP (part, node.nodes[-1])
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
						node.extendAction(action, WordNet.Questions.Analyze.NP (i))

				return node

			@staticmethod
			def VP (tree):
				print ("VP:" + str(tree))
				action, node = "", MultiNode ([PatternNode ()])
				
				for part in list(tree):
					if part.label () == 'VP':
						children = {}
						for i in list(part):
							#print ("key: " + ''.join(i.leaves ()))
							children [''.join(i.leaves ())] = i
						if 'VP' in children:	
							action = action + list(children.keys ())[0]
						else:
							(suffix, node.nodes[-1]) = WordNet.Questions.Analyze.VP (part)
							action += ' ' + suffix
					elif part.label () == 'NP':
						node.nodes [-1] = (WordNet.Questions.Analyze.NP (part, node.nodes[-1]))
					elif part.label () == 'PP':
						node.nodes [-1] = (WordNet.Questions.Analyze.PP (part, node.nodes[-1]))
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


