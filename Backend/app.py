from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    text = data["text"]

    words = text.lower().split()
    unique_words = len(set(words))

    response = {
    "word_count": len(words),
    "unique_words": unique_words,
    "preview": text[:100]
}


    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
