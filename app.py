# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from openai import OpenAI
# import os
# from dotenv import load_dotenv

# load_dotenv()

# app = Flask(__name__)
# CORS(app)

# client = OpenAI(
#     base_url="https://openrouter.ai/api/v1",
#     api_key=os.getenv("OPENROUTER_API_KEY"),
# )

# def chat_with_bot(user_message):
#     try:
#         completion = client.chat.completions.create(
#             extra_headers={
#                 "HTTP-Referer": "http://localhost:5000",
#                 "X-Title": "R38 Assistant",
#             },
#             model="openai/gpt-3.5-turbo",  # Changed to verified model
#             messages=[{"role": "user", "content": user_message}]
#         )
        
#         # Add validation for response structure
#         if not completion.choices or len(completion.choices) == 0:
#             return "Error: Empty response from API"
            
#         return completion.choices[0].message.content
        
#     except Exception as e:
#         print(f"API Error Details: {str(e)}")
#         # Print the actual API error response if available
#         if hasattr(e, 'response'):
#             print(f"API Response: {e.response.text}")
#         return f"Error: {str(e)}"

# @app.route('/chat', methods=['POST'])
# def chat():
#     user_message = request.json.get('message')
#     if not user_message:
#         return jsonify({"error": "No message provided"}), 400
    
#     bot_response = chat_with_bot(user_message)
#     return jsonify({"response": bot_response})

# if __name__ == '__main__':
#     port = int(os.environ.get('PORT', 5000))
#     app.run(host='0.0.0.0', port=port)








from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get('OPENROUTER_API_KEY'),
)

def chat_with_bot(user_message):
    try:
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": os.environ.get('SITE_URL', 'https://your-domain.com'),
                "X-Title": "R38 Assistant",
            },
            model="openai/gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    return jsonify({"response": chat_with_bot(user_message)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)