'''
USAGE:
    - type in terminal: python project.py "10.0.7.1X"
    - X is the number of the naobot
    - default port is 9559 for all naobot in the project
    - 1. hotword: jarvis
    - 2. command: debug, hello/goobbye, dance, repeat,

TODO:
    - face'n name recognition
    - complete documentation
'''


import sys
import time
from naoqi import ALProxy
from hello import *
import json
import speech_recognition as sr



class AssistentAgent:

    port = 9559

    def __init__(self, ip):
        self.ip = ip
        self.r = sr.Recognizer()


    def learn_face(self):
        return 0

    def demo(self):
        return 0

    def move(self):
        return 0

    def say(self):
        return 0


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

            self.activateDetector()
            self.say('i am ready for your next command')

        except Exception, e:
            print "Could not create proxy to ALRobotPosture"
            print "Error was: ", e
            self.exceptionHandler(detector)

    def faceLearning(self, detector = None):

        try:
            faceProxy = ALProxy("ALFaceDetection", IP, PORT)
        except Exception, e:
            print "Error when creating face detection proxy:"
            print str(e)

        for i in range(0, 20):
            time.sleep(0.5)
            val = memoryProxy.getData(memValue, 0)
            print ""
            print "\*****"
            print ""

            # Check whether we got a valid output: a list with two fields.
            if(val and isinstance(val, list) and len(val) == 2):
                # We detected faces !
                # For each face, we can read its shape info and ID.
                # First Field = TimeStamp.
                timeStamp = val[0]
                # Second Field = array of face_Info's.
                faceInfoArray = val[1]
                print val

                # todo: check database
                with open('database.txt') as data_file:
                    data = json.load(data_file)

                try:
                    name = data[faceInfoArray[1][0]]
                    print name
                except Exception, e:

                    print e

                f = open("write.json", "w")
                f.write(data)



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
                self.activateDetector()

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


    def speech_recognize(self, time):

        with sr.Microphone() as source:
            self.r.adjust_for_ambient_noise(source)
            audio = self.r.listen(source, phrase_time_limit=time)
            try:
                return self.r.recognize_google(audio)
            except LookupError, e:
                print e
                return ''
            except sr.UnknownValueError, e:
                print e
    '''
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
    def exceptionHandler(self, detector):
        detector.terminate()
        self.activateDetector()
    '''

if __name__ =='__main__':

    # parameter for naobot
    if len(sys.argv) <= 1:
        print "USAGE: python project.py <robotIP>"
    else:
        nao_ip = sys.argv[1]

    nao = AssistentAgent(nao_ip)

    # TODO: print statements in nao.say()
    while True:

        print "I listen hotword... sir"
        try:
            hotword = nao.speech_recognize(1.0).lower()
            print "You said " + hotword
            if hotword == "alexa":
                print "I listen for command... sir"
                try:
                    command = nao.speech_recognize(2.0).lower()
                    print "You said " + command
                    if command == 'hello':
                        print 'hello'
                    elif command == "stop":
                        break
                except Exception as e:
                    print 'WTF ... NONETYPE'
        except Exception as e:
            print e
