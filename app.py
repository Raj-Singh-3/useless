# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import os
# from langchain.chains import ConversationChain
# from langchain.chains.conversation.memory import ConversationBufferWindowMemory
# from langchain_groq import ChatGroq
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# app = Flask(__name__)
# CORS(app)  # Enable CORS for frontend-backend communication

# # Chatbot Configuration
# model = "mixtral-8x7b-32768"
# conversational_memory_length = 10

# # Initialize chat memory
# memory = ConversationBufferWindowMemory(k=conversational_memory_length)

# groq_chat = ChatGroq(
#     groq_api_key=os.getenv("GROQ_API_KEY"),  # Secure API key
#     model_name=model
# )

# conversation = ConversationChain(
#     llm=groq_chat,
#     memory=memory,
#     output_key="response"
# )

# @app.route("/chat", methods=["POST"])
# def chat():
#     user_input = request.json.get("message")
#     if not user_input:
#         return jsonify({"error": "No input provided"}), 400
    
#     response = conversation.run(user_input)
#     return jsonify({"response": response})

# if __name__ == "__main__":
#     app.run(debug=True)




from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from langchain.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq
from langchain_core.runnables.history import RunnableWithMessageHistory
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Chatbot Configuration
model = "mixtral-8x7b-32768"
conversational_memory_length = 10

# Initialize chat memory
memory = ConversationBufferWindowMemory(k=conversational_memory_length)

groq_chat = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name=model
)

conversation = RunnableWithMessageHistory(
    groq_chat,
    memory=memory
)

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"error": "No input provided"}), 400
    
    response = conversation.invoke(user_input)
    return jsonify({"response": response})

@app.route("/")
def home():
    return jsonify({"message": "Chatbot API is running!"})

if __name__ == "__main__":
    app.run(debug=True)
