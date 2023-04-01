import os
import openai
from flask import Flask, request, jsonify
import secrets
import json
from api_key_manager import APIKeyManager


api_key_manager = APIKeyManager()


app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


system_prompt = "You are a helpful assistant."

def get_chat_response(user_input):
    out = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input},
        ]
    )
    response = out.choices[0].message.content
    return response

@app.route('/api/chat', methods=['POST'])
def chat():
    api_key = request.headers.get('X-Api-Key')

    if not api_key_manager.is_valid_key(api_key):
        return jsonify({"error": "Invalid API key"}), 403

    user_input = request.json.get('user_input')
    response = get_chat_response(user_input)
    return jsonify({"response": response})


@app.route('/api/issue_key', methods=['POST'])
def issue_key():
    user = request.json.get('user')
    new_key = api_key_manager.issue_key(user)
    return jsonify({"api_key": new_key})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
