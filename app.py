from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# OpenRouter API endpoint and API key
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")  # Read API key from .env file

def chat_with_bot(user_message):
    """
    Function to send a message to the OpenRouter API and get the bot's response.
    """
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "http://localhost:5000",  # Optional: Replace with your site URL
        "X-Title": "My Chatbot",  # Optional: Replace with your site name
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openai/gpt-3.5-turbo",  # Use a supported model
        "messages": [
            {"role": "user", "content": user_message}
        ]
    }

    print("Sending payload to OpenRouter API:")  # Debugging
    print(payload)  # Debugging

    try:
        response = requests.post(
            url=OPENROUTER_API_URL,
            headers=headers,
            data=json.dumps(payload))  # Use data=json.dumps() instead of json=
        response.raise_for_status()
        bot_response = response.json()['choices'][0]['message']['content']
        return bot_response
    except requests.exceptions.RequestException as e:
        print("Error response from OpenRouter API:")  # Debugging
        if response:
            print(response.json())  # Print the full error response
        return f"Error: {str(e)}"

@app.route('/chat', methods=['POST'])
def chat():
    """
    Flask route to handle POST requests from the frontend.
    """
    user_message = request.json.get('message')

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    bot_response = chat_with_bot(user_message)
    return jsonify({"response": bot_response})

if __name__ == '__main__':
    # Run the Flask server
    app.run(host='0.0.0.0', port=5000)