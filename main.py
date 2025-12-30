from flask import Flask, request, jsonify, render_template
from generator import generate_idea
from flask_cors import CORS
from db import get_cached_idea, set_cached_idea
# ------------------------------
# Google Authentication Setup
# ------------------------------
import os
from dotenv import load_dotenv
from google.oauth2 import id_token
from google.auth.transport import requests

# Load environment variables
load_dotenv()

# Google OAuth Client ID
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")

if not GOOGLE_CLIENT_ID:
    raise ValueError("GOOGLE_CLIENT_ID not found in .env")


def verify_google_token(auth_header):
    """
    Verifies Google ID token sent from frontend.
    Returns user info if valid, else None.
    """
    if not auth_header:
        return None

    try:
        token = auth_header.split(" ")[1]  # Bearer <token>

        idinfo = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            GOOGLE_CLIENT_ID
        )

        return {
            "email": idinfo.get("email"),
            "name": idinfo.get("name"),
            "picture": idinfo.get("picture")
        }

    except Exception as e:
        print("Google Token Verification Failed:", e)
        return None



#Flask Server Setup

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.post("/generate")
def create_idea():
    auth_header = request.headers.get("Authorization")
    user = verify_google_token(auth_header)

    if not user:
        return jsonify({"error": "Google login required"}), 401

    try:
            data = request.get_json()
            topic = data.get("topic")

            if not topic:
                return jsonify({"error": "Topic is required"}), 400

            normalized_topic=topic.lower().replace(" ","")
            # Check cache first
            cached_idea = get_cached_idea(normalized_topic)
            if cached_idea:
                return jsonify({"idea": cached_idea})

            # Generate new idea if not cached
            idea = generate_idea(normalized_topic)
            set_cached_idea(normalized_topic, idea)
            return jsonify({"idea": idea})
    except Exception as e:
            print(f"Error generating idea: {str(e)}")
            return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
        app.run(host="0.0.0.0", port=8000, debug=True)
