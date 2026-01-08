from flask import Flask, request, jsonify
from flask_cors import CORS
import nltk
from nltk.corpus import stopwords
import re
from collections import Counter

app = Flask(__name__)
CORS(app)

stop_words = set(stopwords.words("english"))

def extract_interests(text):
    text = text.lower()
    text = re.sub(r"[^a-z\s]", "", text)

    words = text.split()
    meaningful = [w for w in words if w not in stop_words and len(w) > 3]

    counts = Counter(meaningful)
    total = sum(counts.values())

    interests = []
    for word, freq in counts.most_common(5):
        interests.append({
            "topic": word,
            "score": round(freq / total, 2)
        })

    return interests

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    text = data["text"]

    interests = extract_interests(text)

    return jsonify({
        "top_interests": interests
    })

if __name__ == "__main__":
    app.run(debug=True)
