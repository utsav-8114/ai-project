from flask import Flask, redirect, render_template, request, jsonify, url_for,Blueprint
from google import generativeai as genai
import requests

backend_app = Blueprint('backend_app',__name__)

# API key directly in code
api_key = "AIzaSyCXrGYdexNO2Nj7T4TdMqQmoO6GitQ7LWQ"
genai.configure(api_key=api_key)

@backend_app.route('/')
def hello():
    
    return render_template('hello.html')

@backend_app.route('/room')
def room():
    return render_template('chat.html')

@backend_app.route("/gemini", methods=['POST'])
def api_call():
    if not api_key:
        return jsonify({"error": "Gemini API key is missing."}), 500
    
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"error": "No message provided"}), 400

        chat_input = data.get("message")
        conversation_history = data.get("history", [])  # Expect history from frontend

        # Format conversation history
        history_text = "\n".join([f"User: {msg['user']}\nBot: {msg['bot']}" for msg in conversation_history])

        # Structured prompt to maintain context
        formatted_prompt = f"""
        You are an expert AI assistant providing concise, structured, and interactive responses.
        
        Conversation so far:
        {history_text}

        User's latest message: {chat_input}
        
        Instructions:
        - Respond concisely while maintaining the conversation flow.
        - Refer to past messages for consistency.
        - Provide step-by-step guidance when necessary.
        - Avoid repeating previous answers.
        """

        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(formatted_prompt)

        if not response or not hasattr(response, 'text'):
            return jsonify({"error": "No response from AI"}), 500

        refined_response = response.text.strip()

        # Smart Quick Replies
        quick_replies = [
            "Can you simplify this?",
            "Provide a step-by-step guide",
            "Give me a real-world example",
            "Summarize this in one line"
        ]

        return jsonify({
            "response": refined_response,
            "quick_replies": quick_replies
        }), 200

    except requests.exceptions.RequestException as e:
        print(f"Request error: {str(e)}")
        return jsonify({"error": f"Request failed: {str(e)}"}), 500
    except KeyError as e:
        print(f"Key error: {str(e)}")
        return jsonify({"error": "Invalid response format from Gemini API"}), 500
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
