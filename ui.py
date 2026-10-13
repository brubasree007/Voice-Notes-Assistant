import gradio as gr
import requests
import os
from dotenv import load_dotenv

load_dotenv()

FLASK_URL = f"http://127.0.0.1:{os.getenv('FLASK_PORT', 5000)}"

def transcribe_api(audio_path):
    if audio_path is None:
        return "No audio provided."
    
    try:
        with open(audio_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{FLASK_URL}/transcribe", files=files)
        
        if response.status_code == 200:
            result = response.json()
            return result['transcription']
        else:
            return f"Error: {response.text}"
    except Exception as e:
        return f"Connection Error: {str(e)}"

def summarize_api():
    try:
        response = requests.get(f"{FLASK_URL}/summarize")
        if response.status_code == 200:
            result = response.json()
            return result['summary'], result['highlights']
        else:
            return f"Error: {response.text}", "No highlights"
    except Exception as e:
        return f"Connection Error: {str(e)}", "Error"

def chat_api(message, history):
    try:
        payload = {"query": message}
        response = requests.post(f"{FLASK_URL}/chat", json=payload)
        if response.status_code == 200:
            return response.json()['response']
        else:
            return f"Error: {response.text}"
    except Exception as e:
        return f"Connection Error: {str(e)}"

def download_transcription(text):
    if not text or text.startswith("Error"):
        return None
    file_path = "transcription.txt"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(text)
    return file_path

# Premium Glassmorphism CSS
css = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');

:root {
    --primary: #6366f1;
    --secondary: #a855f7;
    --bg-gradient: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
}

body {
    font-family: 'Inter', sans-serif;
    background: var(--bg-gradient);
    color: white;
}

.gradio-container {
    background: rgba(255, 255, 255, 0.03) !important;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 24px !important;
    padding: 20px;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}

.main-header {
    text-align: center;
    padding: 40px 0;
    background: linear-gradient(to right, #818cf8, #c084fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2.5rem !important;
    font-weight: 800 !important;
}

.tab-nav {
    border-bottom: none !important;
    display: flex;
    justify-content: center;
    gap: 10px;
}

.tab-nav button {
    border-radius: 12px !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    background: rgba(255, 255, 255, 0.05) !important;
    transition: all 0.3s ease;
}

.tab-nav button.selected {
    background: var(--primary) !important;
    box-shadow: 0 0 15px rgba(99, 102, 241, 0.4);
}

.action-btn {
    background: linear-gradient(90deg, var(--primary), var(--secondary)) !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    transition: transform 0.2s ease;
}

.action-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 20px -5px rgba(99, 102, 241, 0.5);
}

.chatbot-container {
    border-radius: 16px !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    background: rgba(0, 0, 0, 0.2) !important;
}
"""

with gr.Blocks() as demo:
    gr.Markdown("# 🎙️ AI Voice Notes Assistant", elem_classes="main-header")
    
    with gr.Tabs() as tabs:
        with gr.Tab("📝 Transcription", id=0):
            with gr.Row():
                with gr.Column(scale=1):
                    audio_input = gr.Audio(
                        sources=["upload", "microphone"], 
                        type="filepath", 
                        label="Source Audio"
                    )
                    transcribe_btn = gr.Button("🚀 Start Transcription", variant="primary", elem_classes="action-btn")
                
                with gr.Column(scale=2):
                    transcription_output = gr.Textbox(
                        label="Transcribed Text", 
                        lines=12, 
                        placeholder="Your transcription will appear here..."
                    )
                    with gr.Row():
                        prepare_btn = gr.Button("📂 Prepare Download")
                        download_file = gr.File(label="Download TXT")
            
            prepare_btn.click(download_transcription, inputs=[transcription_output], outputs=[download_file])
            transcribe_btn.click(
                transcribe_api, 
                inputs=[audio_input], 
                outputs=[transcription_output]
            )

        with gr.Tab("📊 Summary & Insights", id=1):
            summarize_btn = gr.Button("✨ Generate AI Insights", variant="primary", elem_classes="action-btn")
            
            with gr.Row():
                with gr.Column():
                    summary_output = gr.Markdown("### Summary\n*Generate insights to see summary...*")
                with gr.Column():
                    highlights_output = gr.Markdown("### Key Highlights\n*Generate insights to see highlights...*")
            
            def update_insights():
                summary, highlights = summarize_api()
                return f"### Summary & Keywords\n{summary}", f"### Key Highlights\n{highlights}"
            
            summarize_btn.click(update_insights, outputs=[summary_output, highlights_output])

        with gr.Tab("💬 Chat Assistant", id=2):
            gr.Markdown("### Ask questions based on the recording")
            chatbot = gr.Chatbot(height=500, elem_classes="chatbot-container")
            
            with gr.Row():
                msg = gr.Textbox(
                    label="Ask anything", 
                    placeholder="What were the main action items?", 
                    scale=9
                )
                submit_btn = gr.Button("Send", scale=1, variant="primary")
            
            clear = gr.ClearButton([msg, chatbot])

            def respond(message, chat_history):
                # Prepare history in old format for the API if needed, 
                # but Gradio 6 history is list of dicts: [{"role": "user", "content": "..."}, ...]
                
                # Convert Gradio 6 history to list of tuples for our existing API
                api_history = []
                for msg_obj in chat_history:
                    if msg_obj['role'] == 'user':
                        user_msg = msg_obj['content']
                    elif msg_obj['role'] == 'assistant':
                        api_history.append((user_msg, msg_obj['content']))

                bot_message = chat_api(message, api_history)
                
                chat_history.append({"role": "user", "content": message})
                chat_history.append({"role": "assistant", "content": bot_message})
                return "", chat_history

            msg.submit(respond, [msg, chatbot], [msg, chatbot])
            submit_btn.click(respond, [msg, chatbot], [msg, chatbot])

    gr.Markdown("---")
    gr.Markdown("Built with Flask + Gradio + Whisper + Llama 3", elem_id="footer")

if __name__ == "__main__":
    demo.launch(
        server_port=int(os.getenv("GRADIO_PORT", 7860)),
        share=True,
        theme=gr.themes.Default(primary_hue="indigo", secondary_hue="purple", font=("Inter", "ui-sans-serif", "system-ui")),
        css=css
    )
