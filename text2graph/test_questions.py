import questions as wn
import wordnet as wns

#wn.WordNet.Questions.Analyze.Tree (wn.WordNet.Questions.Parse.QuestionTree ("What is Google?")).printStr ()
#wn.WordNet.Questions.Analyze.Tree (wn.WordNet.Questions.Parse.QuestionTree ("How much does it cost?")).printStr ()
#wn.WordNet.Questions.Analyze.Tree (wn.WordNet.Questions.Parse.QuestionTree ("What has Google done since 1950 while John Smith was director?")).printStr ()

wn.WordNet.Questions.Match.Pattern(
	wns.WordNet.Analyze.Tree(wns.WordNet.Parse.SentenceTree("Google is a company.")),
	wn.WordNet.Questions.Analyze.Tree (wn.WordNet.Questions.Parse.QuestionTree ("What is Google?"))
).printStr()
