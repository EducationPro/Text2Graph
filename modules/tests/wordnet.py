import unittest

import wordnet as wn

class WordNetShould(unittest.TestCase):
	def setUp(self):
		pass

	def WordNetShould_GenerateGraph_WhenInputIsASimpleSenetence_AlexIsClever(self):
		graph = wn.WordNet().analyze('Alex is clever')
		self.assertEqual(graph, None)
		self.assertEqual(graph.has('Alex', 'clever'), 'is-not')

if __name__ == '__main__':
    unittest.main()
