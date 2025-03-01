from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

# Route for the chatbot interaction
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if user_message:
        # Interact with the Ollama model (Assuming Ollama is installed and Llama2 model is pulled)
        result = subprocess.run(
            ['ollama', 'run', 'llama2', '--text', user_message], 
            capture_output=True, text=True
        )
        bot_response = result.stdout.strip()
        return jsonify({'response': bot_response})
    return jsonify({'response': 'Sorry, I didn\'t get that.'}), 400

if __name__ == '__main__':
    app.run(debug=True)
