import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load the environment variables from the .env file into the system environment
load_dotenv()
# Retrieve the Gemini API key from the environment
api_key = os.getenv("GEMINI_API_KEY")

# If the key is missing, raise an error immediately
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

# Configure the Gemini API using the retrieved key
genai.configure(api_key=api_key)

def generate_idea(topic: str) -> str:
    
    # Initialize the generative model
    model = genai.GenerativeModel("models/gemini-2.5-flash") 
    
    # Build the prompt with instructions for style and format

    prompt = f"Generate a creative one sentance idea based on this topic : {topic} should be simple to  understand and should be display either in table format avoid fluff words."
    
    # Send the request to Gemini and get the response
    response = model.generate_content(prompt)
        # Return the clean text output
    return response.text.strip()