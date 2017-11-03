from questions import WordNet as wnq
from wordnet import WordNet as wn

#wn.WordNet.Questions.Analyze.Tree (wn.WordNet.Questions.Parse.QuestionTree ("What is Google?")).printStr ()
#wn.WordNet.Questions.Analyze.Tree (wn.WordNet.Questions.Parse.QuestionTree ("How much does it cost?")).printStr ()
#wn.WordNet.Questions.Analyze.Tree (wn.WordNet.Questions.Parse.QuestionTree ("What has Google done since 1950 while John Smith was director?")).printStr ()

#wn.WordNet.Questions.Match.Pattern(
#	wns.WordNet.Analyze.Tree(wns.WordNet.Parse.SentenceTree("Google is a company.")),
#	wn.WordNet.Questions.Analyze.Tree (wn.WordNet.Questions.Parse.QuestionTree ("What is Google?"))
#).printStr()
    
sentences = wn.Parse.Sentences ('A variable is a storage location paired with an identifier.')
Map = wn.Analyze.Tree (wn.Parse.SentenceTree (sentences [0]))
for x in sentences [1:]:
	Map = wn.Analyze.CombineTrees (Map, wn.Analyze.Tree (wn.Parse.SentenceTree (x)))

Map.printStr ()

response = wnq.Questions.Match.Pattern(
	Map,
	wnq.Questions.Analyze.Tree (wnq.Questions.Parse.QuestionTree ('What is variable?'))
).printStr ()

input ()
