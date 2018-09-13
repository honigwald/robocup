'''
USAGE:
    - type in terminal: python project.py "10.0.7.1X"
    - X is the number of the naobot
    - default port is 9559 for all naobot in the project
    - 1. hotword: jarvis
    - 2. command: debug, hello/goobbye, dance, repeat,

TODO:
    - speech regcognition is offline for nao! implement alternative in python \\ DONE
    - implement listener function for the naobot to execute actions \\ DONE
    - face'n name recognition ??? (Gehad)
    - complete documentation
'''


import sys
import time
from naoqi import ALProxy
from hello import *

#import speech_recognition as sr
#import string
#import threading
#import pyttsx3
import snowboydecoder


class AssistentAgent:

    port = 9559


    def __init__(self, ip):
        self.ip = ip

    # let nao do a motion based on the state
    def motion(self, state, detector):

        try:
            motionProxy = ALProxy("ALMotion", self.ip, self.port)
            detector.terminate()

            if state == 'wakeUp':
                self.say('ok')
                motionProxy.wakeUp()
            elif state == 'rest':
                self.say('ok')
                motionProxy.rest()

            self.initDetector()
            self.say('i am ready for your next command')

        except Exception, e:
            print "Could not create proxy to ALRobotPosture"
            print "Error was: ", e
            self.exceptionHandler(detector)

    def keyframes(self):

        try:
            motionProxy = ALProxy("ALMotion", self.ip, self.port)
        except Exception, e:
            print "Could not create proxy to ALRobotPosture"
            print "Error was: ", e

        # Constraint Balance Motion
        #isEnable   = True
        #supportLeg = "Legs"
        #proxy.wbEnableBalanceConstraint(isEnable, supportLeg)

        '''
        names      = ["LElbowYaw"]
        angleLists = [[1.9, -0.5, 1.9, -0.5]]
        times      = [[1.0,  4.0, 9.0,  13.0]]
        isAbsolute = True
        motionProxy.angleInterpolation(names, angleLists, times, isAbsolute)
        '''

        names, times, keys = hello()
        isAbsolute = True
        motionProxy.angleInterpolation(names, keys, times, isAbsolute)

        '''
        names      = ["LShoulderPitch", "LElbowYaw"]
        angleLists = [[1.9, -0.5, 1.9, -0.5],[-1.0,  -0.2, -1.0,  -0.4]]
        times      = [[1.0,  4.0, 9.0,  13.0],[5.0,  6.0, 7.0,  8.0]]
        isAbsolute = True
        motionProxy.angleInterpolation(names, angleLists, times, isAbsolute)
        '''

    # let nao say something out loud based on a text; detector only, if it's a command
    def say(self, text, detector = None):

        try:
            tts = ALProxy("ALTextToSpeech", self.ip, self.port)

            if detector != None:
                detector.terminate()
                self.initDetector()

            tts.say(text)

        except Exception, e:
            print "Could not create proxy to ALTextToSpeech"
            print "Error was: ", e
            self.exceptionHandler(detector)

    # simple example for build-in posture
    def posture(self, posture):

        try:
            postureProxy = ALProxy("ALRobotPosture", self.ip, self.port)
            postureProxy.goToPosture(posture, 1.0)
        except Exception, e:
            print "Could not create proxy to ALRobotPosture"
            print "Error was: ", e

    # first detector for hot word
    def activateDetector(self):

        # setup for hot word: 'jarvis'
        activater = snowboydecoder.HotwordDetector(['jarvis.pmdl'], sensitivity=0.5)
        print 'wait for activation...'

        # start hot word detector
        callback = [lambda: nao.commandDetector(activater)]
        activater.start(detected_callback=callback, sleep_time=0.5)

    # second detector for command
    def commandDetector(self, activater):

        activater.terminate()

        # setup for command: 'say', 'wake up', 'go to sleep'
        words = ['say.pmdl','wake_up.pmdl', 'go_to_sleep.pmdl']
        detector = snowboydecoder.HotwordDetector(words, sensitivity=0.5)

        print 'wait for command...'
        self.say('What should i do?')

        # start hot command detector
        callbacks = [lambda: self.speak('hello', detector), lambda: self.motion('wakeUp', detector), lambda: self.motion('rest', detector)]
        detector.start(detected_callback=callbacks, sleep_time=0.5)

    # exeption handler for errors
    def exceptionHandler(detector):
        detector.terminate()
        self.activateDetector()


if __name__ =='__main__':

    # parameter for naobot
    if len(sys.argv) <= 1:
        print "USAGE: python project.py <robotIP>"
    else:
        nao_ip = sys.argv[1]

    nao = AssistentAgent(nao_ip)
    nao.say('hello, my name is jarvis, your personal assistant bot)
    nao.activateDetector()


    # before u ran your code, NaoBot needs to wake up!
    #nao.motion('wakeUp')

    # enter your code here down below

    #nao.speechRegcognition2()
    #nao.speak("hi")
    #nao.posture("StandZero")
    #nao.keyframes()
    #nao.speakRegcognition()

    # after u ran your code, let Naobot rest!
    #nao.motion('rest')
