from flask import Flask
from flask import request, jsonify, abort
from wordnet import WordNet as wn
from questions import WordNet as wnq

app = Flask(__name__)
wn.environment ()

@app.route('/api/v1.0/text/map/')
def responseMap():
	if not request.args or not request.args.get('text'):
		abort(400)
	text = request.args.get ('text')
	sentences = wn.Parse.Sentences (text)
	Map = wn.Analyze.Tree (wn.Parse.SentenceTree (sentences [0]))
	for x in sentences [1:]:
		Map = wn.Analyze.CombineTrees (Map, wn.Analyze.Tree (wn.Parse.SentenceTree (x)))

	print(jsonify(Map.getAsObject ()))
	return jsonify(Map.getAsObject ())

@app.route('/api/v1.1/text/answer/')
def responseAnswer():
	if not request.args or not request.args.get('question') or not request.args.get('text'):
		abort(400)
	text = request.args.get ('text')
	sentences = wn.Parse.Sentences (text)
	Map = wn.Analyze.Tree (wn.Parse.SentenceTree (sentences [0]))
	for x in sentences [1:]:
		Map = wn.Analyze.CombineTrees (Map, wn.Analyze.Tree (wn.Parse.SentenceTree (x)))

	response = wnq.Questions.Match.Pattern(
		Map,
		wnq.Questions.Analyze.Tree (wnq.Questions.Parse.QuestionTree (request.args.get('question')))
	)

	print(jsonify(response.getAsObject ()))
	return jsonify(response.getAsObject ())

if __name__ == '__main__':
    app.run(debug=True)
