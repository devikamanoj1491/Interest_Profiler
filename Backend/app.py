from flask import Flask, request, jsonify
from flask_cors import CORS
import nltk
from nltk.corpus import stopwords
import re
from collections import Counter

app = Flask(__name__)
CORS(app)

stop_words = set(stopwords.words("english"))

DOMAIN_KEYWORDS = {
    "Technology": [
        "software", "programming", "coding", "linux", "network",
        "networks", "cybersecurity", "security", "ai", "machine",
        "data", "computer", "systems"
    ],
    "Psychology": [
        "psychology", "behavior", "mind", "mental", "emotion",
        "personality", "cognitive"
    ],
    "Writing": [
        "writing", "story", "stories", "poetry", "essay",
        "blog", "creative"
    ],
    "Business": [
        "business", "startup", "marketing", "finance",
        "economics", "management"
    ]
}

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

def map_to_domains(interests):
    domain_scores = {}

    for item in interests:
        word = item["topic"]
        score = item["score"]

        for domain, keywords in DOMAIN_KEYWORDS.items():
            if word in keywords:
                domain_scores[domain] = domain_scores.get(domain, 0) + score

    return domain_scores

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    text = data["text"]

    interests = extract_interests(text)
    domains = map_to_domains(interests)

    return jsonify({
        "top_keywords": interests,
        "domains": domains
    })


if __name__ == "__main__":
    app.run(debug=True)
