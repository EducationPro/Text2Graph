import unittest

import wordnet as wn

class WordNet_Should(unittest.TestCase):
	def setUp(self):
		#wn.WordNet.environment ()

	def test_WordNet_Should_GenerateGraph_WhenInputIsASimpleSenetence(self):
		node = wn.WordNet.Analyze.Tree(wn.WordNet.Parse.SentenceTree('The red fox is fox.'))
		#print ()
		#print (' | '.join (node.properties))
		self.assertEqual('red' in node.properties, True)
		self.assertEqual('fox' in node.properties, True)
		self.assertEqual(any ('is' == d["action"] for d in node.actions), True)

	def test_WordNet_Should_GenerateGraph_WhenInputIsASimpleSenetence_WithSBAR(self):
		node = wn.WordNet.Analyze.Tree(wn.WordNet.Parse.SentenceTree('The red fox, which is a fox, killed a human.'))
		#print ()
		#print (' | '.join (node.properties))
		self.assertEqual('red' in node.properties, True)
		self.assertEqual('fox' in node.properties, True)
		self.assertEqual(any ('killed' == d["action"] and d["obj"].properties == ['human'] for d in node.actions), True)

	def test_WordNet_Should_GenerateGraph_WhenInputIsASimpleSenetence_WithPOS(self):
		node = wn.WordNet.Analyze.Tree(wn.WordNet.Parse.SentenceTree('John\'s jacket is black.'))
		#print ()
		#print (' | '.join (node.properties))
		self.assertEqual('John\'s' in node.properties, True)
		self.assertEqual('jacket' in node.properties, True)
		self.assertEqual(any ('is' == d["action"] and d["obj"].properties == ['black'] for d in node.actions), True)

	def test_WordNet_Should_GenerateGraph_WhenInputIsASimpleSenetence_WithPOSandSBAR(self):
		node = wn.WordNet.Analyze.Tree(wn.WordNet.Parse.SentenceTree('John\'s jacket, which was black, is cool.'))
		#print ()
		#print (' | '.join (node.properties))
		self.assertEqual('John\'s' in node.properties, True)
		self.assertEqual('jacket' in node.properties, True)
		self.assertEqual(any ('was' == d["action"] and d["obj"].properties == ['black'] for d in node.actions), True)
		self.assertEqual(any ('is' == d["action"] and d["obj"].properties == ['cool'] for d in node.actions), True)

if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(WordNetShould)
	unittest.TextTestRunner(verbosity=2).run(suite)
