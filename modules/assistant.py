import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Determine provider and client
groq_key = os.getenv("GROQ_API_KEY")
openrouter_key = os.getenv("OPENROUTER_API_KEY")

if groq_key:
    client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=groq_key
    )
    DEFAULT_MODEL = os.getenv("LLM_MODEL", "openai/gpt-oss-120b")
    print(f"DEBUG: Using Groq as provider with model {DEFAULT_MODEL}")
elif openrouter_key:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=openrouter_key
    )
    DEFAULT_MODEL = os.getenv("LLM_MODEL", "meta-llama/llama-3.3-70b-instruct")
    print(f"DEBUG: Using OpenRouter as provider with model {DEFAULT_MODEL}")
else:
    client = None
    print("DEBUG: No LLM provider configured")

def generate_summary(text):
    """Generates a concise summary and extracts keywords."""
    if not text:
        return "No text provided for summarization."
    
    prompt = f"""
    Please provide a concise summary of the following transcription.
    Also, extract 5-7 key terms/keywords.
    
    Transcription:
    {text}
    
    Format:
    Summary: [Summary here]
    Keywords: [Key terms here]
    """
    
    try:
        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"DEBUG: Summary Error: {str(e)}")
        return f"Error generating summary: {str(e)}"

def chat_with_transcription(transcription, user_query, chat_history):
    """
    Handles Q&A based ONLY on the transcription context.
    """
    if not transcription:
        return "Please transcribe an audio first."

    system_prompt = f"""
    You are an AI assistant. Answer the user's questions based ONLY on the provided transcription.
    If the information is not in the transcription, politely say you don't know.
    
    Transcription:
    {transcription}
    """
    
    messages = [{"role": "system", "content": system_prompt}]
    
    # Add chat history for context
    for human, ai in chat_history:
        messages.append({"role": "user", "content": human})
        messages.append({"role": "assistant", "content": ai})
    
    messages.append({"role": "user", "content": user_query})
    
    try:
        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=messages
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"DEBUG: Chat Error: {str(e)}")
        return f"Error in chat: {str(e)}"

def highlight_key_sentences(text):
    """Bonus: Highlights important sentences (simulated with LLM)."""
    prompt = f"Identify the 3 most important sentences in this text and return them as a bulleted list:\n\n{text}"
    try:
        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"DEBUG: Highlight Error: {str(e)}")
        return "Could not highlight sentences."
