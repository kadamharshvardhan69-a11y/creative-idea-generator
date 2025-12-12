# Import load_dotenv to load environment variables from a .env file
from dotenv import load_dotenv
# Import os to access system environment variables
import os

# Load variables from the .env file into the environment
load_dotenv()

# Fetch the value of GEMINI_API_KEY stored in the .env file
api_key = os.getenv("GEMINI_API_KEY")

# Check if the key was successfully loaded
if api_key:
      # Print only the first 5 characters for security,
      # replacing the rest with stars
    print("API Key loaded:", api_key[:5] + "*****")
else:
        # If not found, notify that the key didn't load properly
    print("GEMINI_API_KEY is NOT loading — check .env file location and variable name.")
