# SiriGPT
Talk with ChatGPT using your voice and camera. 

As an extension to [SiriGPT](https://github.com/deboradum/SiriGPT), I created SiriVisionGPT. With SiriVisionGPT, you can not only talk to chatGPT with your voice, but also using your camera, making use of YOLO-NAS object recognition.

WIP

# Usage
To use siriVisionGPT.py, you first need to install all requirements, use the following command.
```
python3 -m pip install -r requirements.txt
```
Next, you need an [OpenAI api key](https://platform.openai.com/overview). Add this key to your .env file, and you can start the client using:
```
python3 siriVisionGPT.py.py
```
or:
```
python3 siriVisionGPT.py.py -mh <max_history> -c <num_channels> -d <recording_duration>
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
