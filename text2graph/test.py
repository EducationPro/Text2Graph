import wordnet as wn

wn.WordNet.environment ()

#tree1 = wn.WordNet.Analyze.Tree(wn.WordNet.Parse.SentenceTree('Google is an American multinational technology company that specializes in Internet-related services and products.'))
#tree2 = wn.WordNet.Analyze.Tree(wn.WordNet.Parse.SentenceTree('Google was founded in 1998 by Larry Page and Sergey Brin while they were PhD students at Stanford University in California.'))
#tree3 = wn.WordNet.Analyze.CombineTrees(tree1, tree2)
#tree3.printStr ()
#print ('------------------------------------------------------------')
tree1 = wn.WordNet.Analyze.Tree(wn.WordNet.Parse.SentenceTree('Google is an American multinational technology company that specializes in Internet-related services and products.'))
tree2 = wn.WordNet.Analyze.Tree(wn.WordNet.Parse.SentenceTree('Google is an American multinational technology company that specializes in Internet-related services and products.'))
tree3 = wn.WordNet.Analyze.CombineTrees(tree1, tree2)
tree3.printStr ()
