# Imports.
import argparse
import gtts
import openai
import os
import playsound
import sounddevice as sd
import sys
import threading
import time
import wavio as wv

# Module files.
import gpt
import whisper


# Whisper prijs tracken
global total_tokens
total_tokens = 0
global total_recordings
total_recordings = 0

# Recording settings.
rec_fs = 44100

# https://openai.com/pricing
def calculate_cost():
    # As of may 4th 2023

    # $0.002 / 1K tokens
    gpt_cost = (total_tokens / 1000) * 0.002
    # $0.006 / minute
    whisper_cost = (total_recordings * 0.1) * 0.006

    return gpt_cost + whisper_cost


# Records prompt & sends to whisper API.
def record(event, query):
    # Deletes recording file if one exists.
    if os.path.isfile("prompt.wav"):
        os.remove("prompt.wav")

    global channels, rec_dur
    # Records & saves prompt.
    myrecording = sd.rec(int(rec_dur * rec_fs), samplerate=rec_fs, channels=channels, blocking=True)  # Need to check channel
    wv.write("prompt.wav", myrecording, rec_fs, sampwidth=2)

    transcript = whisper.transcribe()
    query[0] = transcript.text

    # Deletes recording file.
    if os.path.isfile("prompt.wav"):
        os.remove("prompt.wav")

    # Sets event to signal recording is over.
    event.set()


# handles text to speech.
def tts(text):
    if os.path.isfile('tts.mp3'):
        os.remove('tts.mp3')

    s = gtts.gTTS(text)
    s.save('tts.mp3')
    playsound.playsound('tts.mp3')

    if os.path.isfile('tts.mp3'):
        os.remove('tts.mp3')


def main():
    # Initial text.
    response = "What can I do for you?"
    try:
        while True:
            # prints & speaks response.
            print(response)
            t = threading.Thread(target=tts, args=(response, ), daemon=True)
            t.start()

            prompt = ""
            prompt = input("\t")
            # Empty prompt means use voice chat
            if prompt == "":
                queryT = [None]
                e = threading.Event()
                t = threading.Thread(target=record, args=(e, queryT), daemon=True)
                t.start()
                while not e.is_set():
                    print('\tRecording.', end="\r", flush=True)
                    time.sleep(0.4)
                    print('\tRecording..', end="\r", flush=True)
                    time.sleep(0.4)
                    print('\tRecording...', end="\r", flush=True)
                    time.sleep(0.4)
                    sys.stdout.write("\033[K")
                    time.sleep(0.4)
                prompt = queryT[0]
                if prompt is None:
                    print('\tError parsing prompt.\n')
                    continue
                else:
                    print(f'\t{prompt}\n')

            response, tokens_used = gpt.conversate(prompt)
            global total_tokens
            total_tokens += tokens_used

    # Catches ctrl+c & exits program.
    except KeyboardInterrupt:
        print(f"\nGoodbye. Total cost of our conversation: ${calculate_cost()}")
        # Cleans up & deletes files on ctrl+c
        sd.stop()
        if os.path.isfile('tts.mp3'):
            os.remove('tts.mp3')
        if os.path.isfile("prompt.wav"):
            os.remove("prompt.wav")

        exit()


if __name__ == "__main__":
    # max history length en recording length als argparse doen
    parser = argparse.ArgumentParser()
    parser.add_argument('-mh', '--history', type=int, default=10,
                        help='Maximum number of messages GPT will save and use as history of the conversation. More hisotry means more tokens used.')
    parser.add_argument('-c', '--channels', type=int, default=2,
                        help='Number of channels to record.')
    parser.add_argument('-d', '--duration', type=int, default=6,
                        help='Number of seconds to record.')
    args = vars(parser.parse_args())
    gpt.max_history = args['history']
    global channels, rec_dur
    channels = args['channels']
    rec_dur = args['duration']

    main()

