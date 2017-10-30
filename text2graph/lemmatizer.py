class lemmatizer:
	@staticmethod
	def to_verb (word):
		from nltk.stem.wordnet import WordNetLemmatizer
		from nltk.parse import stanford

		parser = stanford.StanfordParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")

		word = ' '.join ([x if x != 'do' and x != 'does' else '' for x in word.split(' ')])

		for line in parser.raw_parse_sents((word, "")):
			node = line
			while True:
				broken = False
				for x in list (node):
					if x.label() == 'VP' or x.label() == 'ROOT' or x.label() == 'FRAG':
						node = x
						broken = True
						break
				if not broken:
					break
			ans = node.leaves ()
			ans[0] = WordNetLemmatizer().lemmatize(ans[0], 'v')
			print('LEMMA:', word, ' '.join(ans))
			return ' '.join(ans)
