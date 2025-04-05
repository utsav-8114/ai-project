from flask import Flask, redirect, render_template, request, jsonify, url_for, Blueprint
from google import generativeai as genai
import requests

app= Flask( __name__)

# API key directly in code
api_key = "AIzaSyCXrGYdexNO2Nj7T4TdMqQmoO6GitQ7LWQ"
genai.configure(api_key=api_key)

@app.route('/')
def hello():
    return render_template('hello.html')

@app.route('/room')
def room():
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

        # Structured prompt for better responses
        formatted_prompt = f"""
        You are an expert assistant providing concise, structured, and high-quality responses.
        
        User Query: {chat_input}
        
        - Keep the explanation clear and direct.
        - If applicable, give step-by-step instructions.
        - Include real-world examples if needed.
        - Summarize the key takeaway in one sentence.
        """

        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(
            formatted_prompt,
            temperature=0.7,
            max_tokens=300
        )

        if not response or not response.text:
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
        return jsonify({"error": "An unexpected error occurred. Please try again."}), 500
if __name__ == "__main__":
    app.run(debug=True)