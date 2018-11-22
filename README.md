# Programming a humanoid robot
### Introduction
In this small documentation you'll get an overview of this project. 
To understand the purpose and how-to-use the code we recommend reading carefully each section of this documentation. 
This project was initially created in the context of the lecture RoboCup of TU Berlin. 
Purpose was to program NAO - a humanoid programmable robot which is developed by the french company Aldeberan Robotics. 
The code is completely written in Python and is using the API of NAO called NAOqi.

### "The greeting Agent"
The main idea of our project is an easy-to-interact NAO with enabled speech recognition to control the robot and voice feedback. 
NAO should also be able to recognize known and unknown persons and give some feedback if such an event happens.
We call this configuration "The greeting Agent".

### Used features of NAOqi
We used mainly following API features:
- ALMotion
- ALTextToSpeech
- ALFaceDetection

We also wanted to use ALSpeechRecognition for the speech recognition abillity.
Sadly this dosen't work on the image of our NAO so we had to implement a workaround.
Instead of ALSpeechRecognition we used the free online service "Google SpeechAPI".
It works quite well. You send an audio-file or something similar to the API and you get a string of the analyzed file. 
