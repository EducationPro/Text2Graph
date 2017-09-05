import unittest

import wordnet as wn

class WordNetShould(unittest.TestCase):
	def test_WordNetShould_GenerateGraph_WhenInputIsASimpleTagSenetence_AlexIsClever(self):
		graph = wn.WordNet().analyze_tag_sentence([wn.Word('Alex', 'noun'), wn.Word('is', 'verb'), wn.Word('clever', 'adj')])
		self.assertEqual(graph.has('Alex', 'clever').word, 'is')
		self.assertEqual(graph.has('Alex', 'clever').adds, [])

	def test_WordNetShould_GenerateGraph_WhenInputIsASimpleSenetence_AlexIsClever(self):
		graph = wn.WordNet().analyze('Alex is clever')
		self.assertEqual(graph.has('Alex', 'clever').word, 'is')
		self.assertEqual(graph.has('Alex', 'clever').adds, [])

if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(WordNetShould)
	unittest.TextTestRunner(verbosity=2).run(suite)
