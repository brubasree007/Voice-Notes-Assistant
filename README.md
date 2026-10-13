# 🎙️ Voice Notes Assistant

An intelligent, AI-powered voice note assistant that transcribes speech, generates summaries and key highlights, and allows you to chat interactively with your transcripts. Built with **OpenAI Whisper**, **Flask**, **Gradio**, and powered by **Groq / OpenRouter** LLMs.

---

## ✨ Features

- **🎯 High-Accuracy Transcription**: Transcribe recorded audio or upload pre-recorded audio files using OpenAI's Whisper model.
- **📝 Smart Summarization**: Automatically generate concise summaries along with key terms and keywords extracted from your audio.
- **💡 Key Sentence Highlighting**: Pinpoint the most critical sentences and takeaways from long discussions.
- **💬 Context-Aware Q&A Chat**: Ask questions directly about the transcribed content with conversational memory.
- **🎨 Glassmorphic Web Interface**: Sleek, modern Gradio UI with dedicated tabs for transcription, summary, and interactive Q&A.
- **📥 One-Click Export**: Download transcriptions directly as `.txt` files.
- **🔌 Decoupled Architecture**: Modular Flask REST API backend paired with a standalone frontend.

---

## 🛠️ Tech Stack

- **Audio Processing / ASR**: [OpenAI Whisper](https://github.com/openai/whisper)
- **Backend API**: [Flask](https://flask.palletsprojects.com/) + Flask-CORS
- **Frontend UI**: [Gradio](https://www.gradio.app/)
- **LLM Reasoning**: [Groq](https://groq.com/) / [OpenRouter](https://openrouter.ai/) via `openai` Python SDK
- **Media Utilities**: [FFmpeg](https://ffmpeg.org/)

---

## 📁 Project Structure

```text
Voice-Notes-Assistant/
├── modules/
│   ├── assistant.py       # LLM integration (summaries, chat, highlights)
│   ├── transcriber.py     # Whisper audio transcription engine
│   └── utils.py           # File handling and cleanup utilities
├── app.py                 # Flask REST API backend
├── ui.py                  # Gradio frontend application
├── requirements.txt       # Python package dependencies
├── .env.template          # Environment variables template
├── .gitignore             # Git ignored files & directories
└── README.md              # Project documentation
```

---

## 🚀 Getting Started

### 1. Prerequisites

- **Python 3.10+**
- **FFmpeg**: Required by Whisper for audio decoding.
  - **Windows**: Install via WinGet: `winget install Gyan.FFmpeg` or download from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) and ensure it is added to your `PATH`.
  - **macOS**: `brew install ffmpeg`
  - **Linux (Ubuntu/Debian)**: `sudo apt update && sudo apt install ffmpeg`

### 2. Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/brubasree007/Voice-Notes-Assistant.git
   cd Voice-Notes-Assistant
   ```

2. **Create and activate a virtual environment (recommended):**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # macOS / Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## ⚙️ Configuration

1. Copy `.env.template` to a new `.env` file:
   ```bash
   cp .env.template .env      # macOS / Linux
   copy .env.template .env    # Windows
   ```

2. Open `.env` and configure your API keys and ports:
   ```env
   # At least one LLM key is required
   GROQ_API_KEY="your_groq_api_key_here"
   # OR
   OPENROUTER_API_KEY="your_openrouter_api_key_here"

   # Optional custom model (defaults to openai/gpt-oss-120b or meta-llama/llama-3.3-70b-instruct)
   LLM_MODEL="openai/gpt-oss-120b"

   # Server Ports
   FLASK_PORT=5000
   GRADIO_PORT=7860
   ```

---

## 🖥️ Running the Application

To run the application, start both the Flask backend and the Gradio UI:

### Step 1: Start the Flask Backend
```bash
python app.py
```
*The backend API will run on `http://127.0.0.1:5000`.*

### Step 2: Start the Gradio Frontend
In a separate terminal:
```bash
python ui.py
```
*Open your browser and navigate to `http://127.0.0.1:7860`.*

---

## 📡 API Endpoints

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/transcribe` | `POST` | Upload an audio file to transcribe with Whisper |
| `/summarize` | `GET` | Generate summary and extract key highlights |
| `/chat` | `POST` | Ask questions grounded strictly in the transcription |
| `/get_data` | `GET` | Retrieve current transcription, summary, and chat history |

---

## 🔒 Security & Privacy

- `.env` is excluded in `.gitignore` to prevent credential exposure.
- Audio uploads are processed and cleaned up from local storage after transcription.
