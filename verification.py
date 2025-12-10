from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    print("API Key loaded:", api_key[:5] + "*****")
else:
    print("GEMINI_API_KEY is NOT loading — check .env file location and variable name.")
