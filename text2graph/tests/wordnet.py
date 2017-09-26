import unittest

import wordnet as wn
import wordnet_ as wn_

#class WordNetShould(unittest.TestCase):
#	def test_WordNetShould_GenerateGraph_WhenInputIsASimpleSenetence_AlexIsClever(self):
#		graph = wn.WordNet().analyze('Alex is clever.')
#		self.assertEqual(graph.has('Alex', 'clever').word, 'is')
#		self.assertEqual(graph.has('Alex', 'clever').adds, [])
#
class WordNet_Should(unittest.TestCase):
	def test_WordNet_Should_GenerateGraph_WhenInputIsASimpleSenetence(self):
		print()
		node = wn_.WordNet.Analyze.Tree(wn_.WordNet.Parse.SentenceTree('The red fox is fox.'))
		print(' '.join(node.properties))
		for act in node.actions:
			print ("'" + act["action"] + "' '" + str(act["obj"]) + "'")
		self.assertEqual('red' in node.properties, True)
		self.assertEqual('fox' in node.properties, True)
		self.assertEqual(any ('is' == d["action"] for d in node.actions), True)
	def test_WordNet_Should_GenerateGraph_WhenInputIsASimpleSenetence_WithSBAR(self):
		print()
		node = wn_.WordNet.Analyze.Tree(wn_.WordNet.Parse.SentenceTree('The red fox, which is a fox, killed a human.'))
		print(' '.join(node.properties))
		self.assertEqual('red' in node.properties, True)
		self.assertEqual('fox' in node.properties, True)
		self.assertEqual(any ('killed' == d["action"] for d in node.actions), True)

if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(WordNetShould)
	unittest.TextTestRunner(verbosity=2).run(suite)
