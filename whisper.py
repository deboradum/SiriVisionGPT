import dotenv
import openai

# Sets API key.
config = dotenv.dotenv_values(".env")
openai.api_key = config['OPENAI_API_KEY']

def transcribe():
    with open("prompt.wav", "rb") as f:
        transcript = openai.Audio.transcribe("whisper-1", f)

    return transcript
