# Programming a humanoid robot
This project is developed and maintained by two students of TU Berlin. 
It shows some of the capabilities of NAO developed by Aldeberan Robotics.

## Introduction
In this small documentation you'll get an overview about this project. 
To understand the purpose and how-to-use the code we recommend reading carefully each section of this documentation. 
The project was initially created in the context of the lecture "RoboCup" of TU Berlin in summerterm 2018. 
Purpose was to program NAO - a humanoid programmable robot which is developed by the french company Aldeberan Robotics. 
The code is completely written in Python and is using the API of NAO called NAOqi.

### "The greeting Agent"
The main idea of our project is an easy-to-interact NAO with enabled speech recognition to control the robot and voice feedback. 
NAO should also be able to recognize known and unknown persons and give some feedback if such an event happens.
We call this configuration "The greeting Agent".

### Demonstration

### Used features of NAOqi
We used mainly following API features:
- ALMotion
- ALTextToSpeech
- ALFaceDetection

We also wanted to use ALSpeechRecognition for the speech recognition ability.
Sadly this dosen't work on the image of our NAO so we had to implement a workaround.
Instead of ALSpeechRecognition we used the free online google service "speech-to-text".
It works quite well. You send an audiostream to the service and you get in return a string of the analyzed stream. 

For detailed information about the used functions of NAOqi please refer to the provided links:
1. http://doc.aldebaran.com/2-1/naoqi/motion/index.html
2. http://doc.aldebaran.com/2-1/naoqi/audio/altexttospeech.html
3. http://doc.aldebaran.com/2-1/naoqi/peopleperception/alfacedetection.html

Detailed information about the used google service "speech-to-text":
1. https://cloud.google.com/speech-to-text/

## Getting started
Before you can run the code you need to install the prerequisite listed in the following section.

### Prerequirements
Firstly you need a running Python environment with configured NAOqi framework. A detailed installation guide is provided in the [aldeberan documentation](http://doc.aldebaran.com/2-1/dev/python/install_guide.html). We used a Linux "Ubuntu 16.04" running in a virtual machine.
As workaround for the speech recogognition we used the Python library SpeechRecognition in version 3.8.1
The installation guide is provided [here](https://pypi.org/project/SpeechRecognition/)

To use the google service you need to provide an active internet connection when running the code.

### Running 
To start the program you've to run following command in a terminal:
```
Python project.py <IP-Adress of NAO>
```
### List of commands
When the project is running you can use following commands to control NAO:
* **hello** - gives a voice feedback 
* **database** - prints face database content to CLI
* **reset** - reset stored faces in database
* **wake up** - NAO goes to standInit posture
* **new person** - learning process for facerecognition is started
* **rest** - NAO goes to rest posture
* **stop** - NAO goes to rest posture and python program is stopped
* **start** - starts the demonstration

## Authors
* **Willy Cai** - [wiilee](https://github.com/wiilee)
* **Simon Blanck** - [honigwald](https://github.com/honigwald)

