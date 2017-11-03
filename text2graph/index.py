from flask import Flask, render_template
from flask import request, jsonify, abort
from wordnet import WordNet as wn
from questions import WordNet as wnq

app = Flask(__name__, template_folder='.')
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
    resp = jsonify(Map.getAsObject ())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

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
    resp = jsonify(response.getAsObject ())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/jquery-3.2.1.min.js')
def sendAJAX():
    return render_template('jquery-3.1.1.js')

@app.route('/index.js')
def sendINDEX():
    return render_template('index.js')

@app.route('/find.html')
def sendFind():
    return render_template('find.html')

@app.route('/graph.html')
def sendGraph():
    return render_template('graph.html')

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=8001)
