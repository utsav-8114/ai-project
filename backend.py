from flask import Flask, redirect, render_template, request, jsonify, url_for
from google import generativeai as genai
import requests

app = Flask(__name__)

# API key directly in code
api_key = "AIzaSyCXrGYdexNO2Nj7T4TdMqQmoO6GitQ7LWQ"
genai.configure(api_key=api_key)

@app.route('/')
def hello():
    return render_template('hello.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route("/gemini", methods=['POST'])
def api_call():
    if not api_key:
        return jsonify({"error": "Gemini API key is missing."}), 500
    
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"error": "No message provided"}), 400
        
        chat_input = data.get("message")
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(chat_input)

        # Define quick replies based on the context
        quick_replies = [
            "Tell me more about that",
            "Can you explain in detail?",
            "What are the next steps?",
            "Show me examples"
        ]

        return jsonify({
            "response": response.text,
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
        return jsonify({"error": "An unexpected error occurred. Please try again."}), 500

if __name__ == "__main__":
    app.run(debug=True)