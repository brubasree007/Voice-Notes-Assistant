from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from modules.transcriber import transcribe_audio
from modules.assistant import generate_summary, chat_with_transcription, highlight_key_sentences
from modules.utils import save_uploaded_file, delete_file
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Temporary in-memory storage for the current transcription
# In a real app, this would be in a database or session
current_data = {
    "transcription": "",
    "summary": "",
    "chat_history": []
}

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    try:
        text = transcribe_audio(file_path)
        print(f"DEBUG: Transcription result: {text[:100]}...")
        current_data["transcription"] = text
        # Reset summary and chat for new transcription
        current_data["summary"] = ""
        current_data["chat_history"] = []
        
        return jsonify({"transcription": text})
    finally:
        delete_file(file_path)

@app.route('/summarize', methods=['GET'])
def summarize():
    if not current_data["transcription"]:
        return jsonify({"error": "Nothing to summarize. Transcribe audio first."}), 400
    
    summary = generate_summary(current_data["transcription"])
    highlights = highlight_key_sentences(current_data["transcription"])
    
    current_data["summary"] = summary
    return jsonify({
        "summary": summary,
        "highlights": highlights
    })

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_query = data.get("query")
    
    if not current_data["transcription"]:
        return jsonify({"error": "No transcription found. Please transcribe audio first."}), 400
    
    response = chat_with_transcription(
        current_data["transcription"], 
        user_query, 
        current_data["chat_history"]
    )
    
    # Store history
    current_data["chat_history"].append((user_query, response))
    
    return jsonify({"response": response})

@app.route('/get_data', methods=['GET'])
def get_data():
    return jsonify(current_data)

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True, port=int(os.getenv("FLASK_PORT", 5000)))
