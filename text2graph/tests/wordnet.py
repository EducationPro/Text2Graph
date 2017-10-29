import unittest

import wordnet as wn

class WordNet_Should(unittest.TestCase):
	def setUp(self):
		wn.WordNet.environment ()
		pass

	def test_WordNet_Should_GenerateGraph_WhenInputIsASimpleSenetence(self):
		node = wn.WordNet.Analyze.Tree(wn.WordNet.Parse.SentenceTree('The red fox is fox.')).nodes[0]
		#print ()
		#print (' | '.join (node.properties))
		self.assertEqual('red' in node.properties, True)
		self.assertEqual('fox' in node.properties, True)
		self.assertEqual(any ('is' == d["action"] for d in node.actions), True)

	def test_WordNet_Should_GenerateGraph_WhenInputIsASimpleSenetence_WithSBAR(self):
		node = wn.WordNet.Analyze.Tree(wn.WordNet.Parse.SentenceTree('The red fox, which is a fox, killed a human.')).nodes[0]
		#print ()
		#print (' | '.join (node.properties))
		self.assertEqual('red' in node.properties, True)
		self.assertEqual('fox' in node.properties, True)
		self.assertEqual(any ('killed' == d["action"] and d["obj"].nodes[0].properties == ['human'] for d in node.actions), True)

	def test_WordNet_Should_GenerateGraph_WhenInputIsASimpleSenetence_WithPOS(self):
		node = wn.WordNet.Analyze.Tree(wn.WordNet.Parse.SentenceTree('John\'s jacket is black.')).nodes[0]
		#print ()
		#print (' | '.join (node.properties))
		self.assertEqual('John\'s' in node.properties, True)
		self.assertEqual('jacket' in node.properties, True)
		self.assertEqual(any ('is' == d["action"] and d["obj"].properties == ['black'] for d in node.actions), True)

	def test_WordNet_Should_GenerateGraph_WhenInputIsASimpleSenetence_WithPOSandSBAR(self):
		node = wn.WordNet.Analyze.Tree(wn.WordNet.Parse.SentenceTree('John\'s jacket, which was black, is cool.')).nodes[0]
		#print ()
		#print (' | '.join (node.properties))
		self.assertEqual('John\'s' in node.properties, True)
		self.assertEqual('jacket' in node.properties, True)
		self.assertEqual(any ('was' == d["action"] and d["obj"].properties == ['black'] for d in node.actions), True)
		self.assertEqual(any ('is' == d["action"] and d["obj"].properties == ['cool'] for d in node.actions), True)

	def test_WordNet_Should_GenerateGraph_WhenInputIsAComplexSentence_WithComplexSubject(self):
		node = wn.WordNet.Analyze.Tree(wn.WordNet.Parse.SentenceTree('Alex and John are clever'))
		node1 = node.nodes [0]
		node2 = node.nodes [1]
		self.assertEqual('Alex' in node1.properties, True)
		self.assertEqual(any ('are' == d["action"] and d['obj'].properties == ['clever'] for d in node1.actions), True)
		self.assertEqual('John' in node2.properties, True)
		self.assertEqual(any ('are' == d["action"] and d['obj'].properties == ['clever'] for d in node2.actions), True)

	def test_WordNet_Should_GenerateGraph_WhenInputIsAComplexSentence_WithComplexSubject_NP(self):
		node = wn.WordNet.Analyze.Tree(wn.WordNet.Parse.SentenceTree('Alex and John are humans and programmers'))
		node1 = node.nodes [0]
		node2 = node.nodes [1]
		self.assertEqual('Alex' in node1.properties, True)
		self.assertEqual(any ('are' == d["action"] and d['obj'].nodes[0].properties == ['humans'] for d in node1.actions), True)
		self.assertEqual(any ('are' == d["action"] and d['obj'].nodes[1].properties == ['programmers'] for d in node1.actions), True)
		self.assertEqual('John' in node2.properties, True)
		self.assertEqual(any ('are' == d["action"] and d['obj'].nodes[0].properties == ['humans'] for d in node2.actions), True)
		self.assertEqual(any ('are' == d["action"] and d['obj'].nodes[1].properties == ['programmers'] for d in node2.actions), True)

if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(WordNetShould)
	unittest.TextTestRunner(verbosity=2).run(suite)
