# Programming a humanoid robot
This project is developed and maintained by two students of TU Berlin.
It was created in the context of the lecture [RoboCup](https://github.com/honigwald/programming-humanoid-robot-in-python).
The main goal was to show some of the capabilities of NAO developed by Aldeberan Robotics.

## Introduction
In this small documentation you'll get an overview about this project. 
To understand the purpose and how-to use the code we recommend reading carefully each section of this documentation. 
As mentioned this project was initially created in the context of the lecture "RoboCup" of TU Berlin in summerterm 2018. 
Purpose was to program NAO - a humanoid programmable robot which is developed by the french company Aldeberan Robotics. 
Therefore the code is completely written in Python and is using the API of NAO called NAOqi.

### "The greeting Agent"
The main idea of our project is an easy-to-interact NAO with enabled speech recognition to control the robot and voice feedback. 
NAO should also be able to recognize known and unknown persons and give some feedback if such an event happens.
We call this "The greeting Agent".

### Demonstration
To show our project goal we've implemented a special function called "rundemo". 
When running this function NAO will try to scan his closer environment to identify real persons around him.
Therefore he's standing up and looking from right to left.
After that he's turing 90 degrees to the left and start looking again from right to left. 
This behaviour is repeated until he finished a full 360 degree circle.

Each time he's recognizing a person in his closer environment he tries to identify the person with the data returned by a picture taken by NAOs camera.
Two different options are possible:
1. The person is known: NAO ask for the name of the identified person and stores a name-face tuple
2. The person is unknown: NAO greets the known person by saying the name and doing a greeting move

In this manner NAO is nearly able to identify all persons in his closer environmet

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

