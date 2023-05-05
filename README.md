# SiriGPT
Talk with ChatGPT using your voice. 

To gain experience with the OpenAI api, I created this tool to chat with GPT3.5-turbo using your voice. The OpenAI Whisper api is used to transcribe voices, and the GPT api is used as the chat client. 

# Usage
To use SiriGPT, you first need to install all requirements, use the following command.
```
python3 -m pip install -r requirements.txt
```
Next, you need an [OpenAI api key](https://platform.openai.com/overview). Add this key to your .env file, and you can start the client using:
```
python3 siriGPT.py
```
or:
```
python3 siriGPT.py -mh <max_history> -c <num_channels> -d <recording_duration>
```
With parameters:
```
-h, --help          show this help message and exit
-mh, --history      Maximum number of messages GPT will save and use as history of the conversation. More hisotry means more tokens used. Default is 10.
-c, --channels      Number of channels to record. Default is 2.
-d , --duration     Number of seconds to record. Default is 6.
```

The max history parameter is the amount of messages ChatGPT uses as reference history. All the tokens of these messages will need to parsed, so more history means a more expensive chat.

# Demo
