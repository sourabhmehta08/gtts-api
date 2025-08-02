from flask import Flask, request, send_file
from gtts import gTTS
import os
import uuid

app = Flask(__name__)

@app.route('/tts', methods=['POST'])
def tts():
    data = request.get_json()
    text = data.get('text', '')
    if not text:
        return {'error': 'Text is required'}, 400

    filename = f"{uuid.uuid4()}.mp3"
    tts = gTTS(text)
    tts.save(filename)

    response = send_file(filename, mimetype='audio/mpeg')
    os.remove(filename)
    return response
