from flask import Flask
from flask import request, jsonify, abort
from wordnet import WordNet as wn

app = Flask(__name__)
wn.environment ()

@app.route('/api/v1.0/text/map/', methods=['GET'])
def responseMap():
	if not request.args or not request.args.get('text'):
		abort(400)
	text = request.args.get ('text')
	sentences = wn.Parse.Sentences (text)
	print (sentences [0])
	Map = wn.Analyze.Tree (wn.Parse.SentenceTree (sentences [0]))
	for x in sentences [1:]:
		Map = wn.Analyze.CombineTrees (Map, wn.Analyze.Tree (wn.Parse.SentenceTree (x)))

	return jsonify(Map.getAsObject ())

if __name__ == '__main__':
    app.run(debug=True)
