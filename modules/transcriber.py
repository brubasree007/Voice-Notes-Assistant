import whisper
import os

# Manually add FFmpeg to PATH for this process
ffmpeg_path = r"C:\Users\Admin\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1-full_build\bin"
if os.path.exists(ffmpeg_path) and ffmpeg_path not in os.environ["PATH"]:
    os.environ["PATH"] += os.pathsep + ffmpeg_path
elif not any(os.path.exists(os.path.join(p, "ffmpeg.exe")) for p in os.environ["PATH"].split(os.pathsep)):
    print("WARNING: FFmpeg not found in PATH or hardcoded location.")

# Load model once to avoid reloading on every request
# Using 'small' for better accuracy (requires slightly more VRAM/RAM)
model = whisper.load_model("small")

def transcribe_audio(file_path):
    """
    Transcribes audio file using OpenAI Whisper.
    Returns the transcribed text.
    """
    try:
        if not os.path.exists(file_path):
            return "Error: File not found."
            
        result = model.transcribe(file_path)
        return result["text"].strip()
    except Exception as e:
        return f"Error during transcription: {str(e)}"
