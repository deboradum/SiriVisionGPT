# SiriVisionGPT
Talk with ChatGPT using your voice and camera. 

As an extension to [SiriGPT](https://github.com/deboradum/SiriGPT), I created SiriVisionGPT. With SiriVisionGPT, you can not only talk to chatGPT with your voice, but also using your camera, making use of YOLO-NAS object recognition.

SiriVisionGPT uses pytorch mps to speed up the yolo object detection, but can also run on CPU. This will limit the framerate of yolo however.

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
-h, --help            show this help message and exit
-mh, --history        Maximum number of messages GPT will save and use as history of the conversation. 
                      More hisotry means more tokens used. Default is 10.
-c, --channels        Number of channels to record. Default is 2.
-d, --duration        Number of seconds to record. Default is 6.
-yd, --yoloduration   Number of seconds to record video. Default is 9.
-yc, --camera         Index of the camera yolo will use as input. Default is 0.
```

The max history parameter is the amount of messages ChatGPT uses as reference history. All the tokens of these messages will need to parsed, so more history means a more expensive chat.

## Vision mode
After the word 'show' has been spoken, the camera will automatically be activated in the next prompt. A comma seperated string of the detected objects will then be used as the a prompt. For example:

> (You) Im going to *show* you items of food, and you need to tell me if they are gluten free.

> (SiriVisionGPT) Okay!

> (You) ***Shows items on camera***

> (SiriVisionGPT) ***Answers***

## Barcode mode
After the words 'show' and 'barcode' have been spoken, barcode mode is activated. You can now show a barcode on the camera and if this barcode is present in the [openfoodfacts](https://world.openfoodfacts.org/) database, information about the product is sent to GPT to use in the answer to your question. For example:

> (You) Im going to *show* you a *barcode*. Can I eat this if I am allergic to peanuts?

> (SiriVisionGPT) Okay!

> (You) ***Shows barcode on camera***

> (SiriVisionGPT) ***Answers***

# Demo
WIP
