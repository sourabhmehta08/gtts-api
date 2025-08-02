from flask import Flask, request, send_file, jsonify
from gtts import gTTS
from flask_cors import CORS
import uuid
import os

app = Flask(__name__)
CORS(app)  # Allow CORS so you can call this from your Next.js frontend

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "gTTS API is running"}), 200

@app.route('/tts', methods=['POST'])
def tts():
    try:
        data = request.get_json()
        text = data.get('text', '').strip()

        if not text:
            return jsonify({'error': 'Text is required'}), 400

        filename = f"{uuid.uuid4()}.mp3"
        tts = gTTS(text)
        tts.save(filename)

        response = send_file(filename, mimetype='audio/mpeg')
        os.remove(filename)
        return response

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Required for Render
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))  # Render sets PORT env variable
    app.run(host='0.0.0.0', port=port)
