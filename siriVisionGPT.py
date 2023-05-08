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
    global language
    s = gtts.gTTS(text, lang=language)
    s.save('tts.mp3')
    playsound.playsound('tts.mp3')

    if os.path.isfile('tts.mp3'):
        os.remove('tts.mp3')


# Checks if language is supported.
def is_supported_lan(lan):
    # Supported languages by Whisper, ChatGPT and gtts.
    supported = ['af', 'ar', 'bg', 'bs', 'ca', 'cs', 'da', 'de', 'el', 'en',
                 'es', 'et', 'fi', 'fr', 'hi', 'hr', 'hu', 'id', 'is', 'it',
                 'iw', 'ja', 'kn', 'ko', 'lv', 'mr', 'ms', 'ne', 'nl', 'no',
                 'pl', 'pt', 'ro', 'ru', 'sk', 'sr', 'sv', 'sw', 'ta', 'th',
                 'tr', 'uk', 'ur', 'vi']

    if lan in supported:
        return lan
    else:
        raise argparse.ArgumentTypeError(f"Language {lan} is not supported.")

# Returns starting chat sentence.
def get_start_sentence(lan):
    sentences = {'af': "Wat kan ek vir jou doen?", 'ar': "ما الذي يمكنني أن أفعله من أجلك؟",
                 'bg': "Какво мога да направя за теб?", 'bs': "Šta mogu učiniti za vas?",
                 'ca': "Què puc fer per tu?", 'cs': "Co pro vás mohu udělat?",
                 'da': "Hvad kan jeg gøre for dig?", 'de': "Was kann ich für Dich tun?",
                 'el': "Τι μπορώ να κάνω για σένα?", 'en': "What can I do for you?",
                 'es': "¿Qué puedo hacer por ti?", 'et': "Mida ma saan teie heaks teha?",
                 'fi': "Mitä voin tehdä puolestasi?", 'fr': "Que puis-je faire pour vous?",
                 'hi': "मेरे द्वारा आपके लिए क्या किया जा सकता है?", 'hr': "Što mogu učiniti za tebe?",
                 'hu': "Mit tehetek önért?", 'id': "Apa yang bisa saya lakukan untuk Anda?",
                 'is': "Hvað get ég gert fyrir þig?", 'it': "Cosa posso fare per lei?",
                 'iw': "מה אני יכול לעשות בשבילך?", 'ja': "どういうご用件ですか？",
                 'kn': "ನಾನು ನಿಮಗಾಗಿ ಏನು ಮಾಡಬಹುದು?", 'ko': "내가 당신을 위해 무엇을 할 수?",
                 'lv': "Ko es varu darīt jūsu labā?", 'mr': "मी तुमच्यासाठी काय करू शकतो?",
                 'ms': "Apa yang boleh saya lakukan untuk awak?", 'ne': "म तिम्रो लागि के गर्न सक्छु?",
                 'nl': "Wat kan ik voor je doen?", 'no': "Hva kan jeg gjøre for deg?",
                 'pl': "Co mogę dla ciebie zrobić?", 'pt': "O que posso fazer para você?",
                 'ro': "Cu ce vă pot ajuta?", 'ru': "Что я могу сделать для вас?",
                 'sk': "Čo pre vás môžem urobiť?", 'sr': "Шта могу да учиним за вас?",
                 'sv': "Vad kan jag hjälpa dig med?", 'sw': "Naweza kukusaidia vipi?",
                 'ta': "உனக்காக நான் என்ன செய்ய முடியும்?", 'th': "ฉันทำอะไรให้คุณได้บ้าง",
                 'tr': "Sizin için ne yapabilirim?", 'uk': "Чим я можу тобі допомогти?",
                 'ur': "میں آپکے لیے کیا کرسکتا ہوں؟", 'vi': "Tôi có thể làm gì cho bạn?"}

    return sentences[lan]


def main():
    # Initial text.
    global language, history_len
    gpt_handler = gpt.GPThandler(history_len, language)
    response = get_start_sentence(language)
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

            response, tokens_used = gpt_handler.conversate(prompt)
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
    parser.add_argument('-l', '--language', type=is_supported_lan, default='en',
                        help="Language to chat in. Supported languages are: af, ar, bg, bs, ca, cs, da, de, el, en, es, et, fi, fr, hi, hr, hu, id, is, it, iw, ja, kn, ko, lv, mr, ms, ne, nl, no, pl, pt, ro, ru, sk, sr, sv, sw, ta, th, tr, uk, ur, vi")
    args = vars(parser.parse_args())
    global channels, rec_dur, language, history_len
    history_len = args['history']
    channels = args['channels']
    rec_dur = args['duration']
    language = args['language']

    main()
