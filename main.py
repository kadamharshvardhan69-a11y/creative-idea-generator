from flask import Flask, request, jsonify, render_template
from generator import generate_idea
from flask_cors import CORS

app = Flask(__name__, template_folder="templates", static_folder="static")

# Enable CORS for ALL routes and ALL origins
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/")
def home():
    return render_template("index.html")

@app.post("/generate")
def create_idea():
    data = request.get_json()

    # Prevent empty input from breaking the backend
    topic = data.get("topic", "").strip()
    if not topic:
        return jsonify({"error": "Topic cannot be empty"}), 400

    # Generate idea
    idea = generate_idea(topic)
    return jsonify({"idea": idea})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
