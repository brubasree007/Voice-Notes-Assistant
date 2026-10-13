import os
import uuid

def save_uploaded_file(audio_file, upload_folder):
    """Saves an audio file to the upload folder and returns the path."""
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    
    # Generate unique filename
    ext = os.path.splitext(audio_file.name)[-1]
    filename = f"{uuid.uuid4()}{ext}"
    file_path = os.path.join(upload_folder, filename)
    
    # In Flask context, audio_file would be a werkzeug file object
    # In Gradio, it's often a string (path) or a numpy array
    # We'll handle both in the respective calling functions
    return file_path

def delete_file(file_path):
    """Deletes a file if it exists."""
    if os.path.exists(file_path):
        os.remove(file_path)
