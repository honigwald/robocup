'''
USAGE:
    - type in terminal: python project.py "10.0.7.1X"
    - X is the number of the naobot
    - default port is 9559 for all naobot in the project
'''

import sys
import time
from naoqi import ALProxy
from hello import *
import speech_recognition as sr

class AssistentAgent:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.r = sr.Recognizer()

    def speech_recognize(self, time):
        with sr.Microphone() as source:
            self.r.adjust_for_ambient_noise(source)
            audio = self.r.listen(source, phrase_time_limit=time)
            try:
                return self.r.recognize_google(audio)
            except LookupError, e:
                print e
                return 'there was an error!'
            except sr.UnknownValueError, e:
                print e
                return 'what do you mean? i do not understand'

    def motion(self, state):
        try:
            motionProxy = ALProxy("ALMotion", self.ip, self.port)

            if state == 'wakeUp':
                motionProxy.wakeUp()
            elif state == 'rest':
                motionProxy.rest()

        except Exception, e:
            print "Error when creating face detection proxy:"
            print str(e)

    ### Controlling facerecognition API
    def face(self, state):
        try:
            faceProxy = ALProxy("ALFaceDetection", self.ip, self.port)
        except Exception, e:
            print "Error when creating face detection proxy:"
            print str(e)

        if state == 'learn':
            self.say('Whats your name')
            name = self.speech_recognize(1.0).lower()
            if (faceProxy.learnFace(str(name))):
                print "Actual DB: %s" % (faceProxy.getLearnedFacesList())
                self.say('Thank you')
            else:
                print "Something went wrong"
        elif state == 'cleardb':
            if (faceProxy.clearDatabase()):
                print "DB cleared"
                print "Actual DB: %s" % (faceProxy.getLearnedFacesList())
            else:
                print "Something went wrong"
        elif state == 'getname':
            period = 500
            faceProxy.subscribe("Test_Face", period, 0.0 )
            memValue = "FaceDetected"
            name = "unknown"
            try:
                memoryProxy = ALProxy("ALMemory", self.ip, self.port)
            except Exception, e:
                print "Error when creating memory proxy:"
                print str(e)
                exit(1)

            val = memoryProxy.getData(memValue, 0)
            if(val and isinstance(val, list) and len(val) == 5):
                ### THIS IS IMPORTANT
                ### DETERMINING THE NAME OF RECOGNIZED PERSON
                print "Name of recognized Person: %s" % val[1][0][1][2]
                name = val[1][0][1][2]
            else:
                print "Error with getData. ALValue = %s" % (str(val))

            # Unsubscribe the module.
            faceProxy.unsubscribe("Test_Face")
            return name
        elif state == 'getdb':
            print "Actual DB: %s" % (faceProxy.getLearnedFacesList())

    ### The final demonstration of the project
    def rundemo(self):
        #TODO: Actually it's just some small testing here
        print "Demo is running"
        self.motion('wakeUp')
        self.tracker('start')
        checked = []        # This array stores already greeted people
        for i in range(20):
            # new target detected
            if self.tracker('check'):
                name = self.face('getname')
                # check if target already recognized
                if str(name) in checked:
                    continue
                else:
                    # check if we know the name
                    if name != 'unknown':
                        self.say('Hello')
                        self.say(name)
                        ### TODO: MOVE YOUR ASS - ENSURE NOT TO GREET A 2nd TIME
                    else:
                        ### TODO: TESTING - DETECTED SOMEONE WHO IS NOT KNOWN
                        self.say('Hello you!')
                        self.say('Will u tell me your name.')
                        time.sleep(1)
                        self.say('Say yes or no') 
                        if (str(nao.speech_recognize(1.0).lower() == 'yes')):
                            self.say('ok')
                            self.face('learn')
                            self.say('thank u')
                        else:
                            self.say('awww. thats sad')
                    time.sleep(1)
                checked.append(name)
            # no target
            else:
                ### TODO:MOVE YOUR BODY
        
        # finish the demo
        self.tracker('stop')
        self.motion('rest')
        print "Demo is finished"

    ### Controlling the facetracking function of nao
    def tracker(self, state):
        try:
            tracker = ALProxy("ALTracker", self.ip, self.port)
        except Exception, e:
            print "Could not create proxy to ALTracker!"
            print "Error was: ", e

        if state == "start":
            targetName = "Face"
            faceWidth = 0.1
            tracker.setMode('Move')
            tracker.registerTarget(targetName, faceWidth)
            tracker.track(targetName)

        elif state == "check":
            if tracker.isNewTargetDetected():
                return True
            else:
                return False

        elif state == "stop":
            tracker.stopTracker()
            tracker.unregisterAllTargets()

    ### Controlling the movement of nao
    ### TODO: HERE WE'VE TO IMPLEMENT RANDOM MOVEMENT
    def move(self, X, Y):
        try:
            motionProxy = ALProxy("ALMotion", self.ip, self.port)
            postureProxy = ALProxy("ALRobotPosture", self.ip, self.port)

            # Wake up robot
            motionProxy.wakeUp()

            # Send robot to Stand
            postureProxy.goToPosture("StandInit", 0.5)

            # go to position x, y
            Theta = 0.5
            Frequency = 0.5 # max speed
            try:
                motionProxy.moveToward(X, Y, Theta, [["Frequency", Frequency]])
            except Exception, errorMsg:
                print str(errorMsg)
                print "This example is not allowed on this robot."
                exit()

            motionProxy.rest()

        except Exception, e:
            print e

        return 0

    ### Nao speaks given text
    def say(self, text):
        try:
            tts = ALProxy("ALTextToSpeech", self.ip, self.port)
            tts.setVolume(0.7)
            tts.say(text)

        except Exception, e:
            print "Could not create proxy to ALTextToSpeech!"
            print "Error was: ", e
'''
    ### Nao speaks given text with emotions ;)
    def esay(self, text):

        try:
            atts = ALProxy("ALAnimatedSpeech", self.ip, self.port)
            atts.

        except Exception, e:
            print "Could not create proxy to ALTextToSpeech!"
            print "Error was: ", e
'''


### MAIN-FUNCTION OF THIS PROJECT
if __name__ =='__main__':
    # get cli parameter
    if len(sys.argv) <= 1:
        print "USAGE: python project.py <robotIP>"
    else:
        nao_ip = sys.argv[1]

    # initializing connection to naobot
    port = 9559
    nao = AssistentAgent(nao_ip, port)

    nao.say('awaiting keyword!')
    #nao.move(0.8, 0.4)
    while True:
        print "Waiting for Keyword"
        try:
            keyword = nao.speech_recognize(1.0).lower()
            print "You said: " + keyword
            if keyword == "no":
                print "Listening..."
                try:
                    nao.say('listening')
                    command = nao.speech_recognize(2.0).lower()
                    print "You said: " + command

                    # test speech capabilities of NAO
                    if command == 'hello':
                        nao.say('hello')

                    # get stored faces
                    elif command == 'database'
                        nao.face('getdb')

                    # wakeup NAO - goto motion standInit
                    elif command == 'wake up':
                        nao.motion('wakeUp')

                    # execute face_learning phase
                    elif command == 'new person':
                        # TODO: NEEDS TO BE TESTED
                        # RESULT: Voice speed has to slowdown!
                        nao.say('position yourself in front me')
                        time.sleep(1)
                        nao.say('say ok when you are ready')
                        resp = nao.speech_recognize(2.0).lower()
                        print resp
                        if resp == 'ok':
                            nao.face('learn')
                        else:
                            nao.say('oh something went wrong')

                    # remove all faces from facedb
                    elif command == 'reset':
                        nao.say('removing all faces from database')
                        nao.say('say ok to process')
                        resp = nao.speech_recognize(2.0).lower()
                        if resp == 'ok':
                            nao.face('cleardb')
                            nao.say('database cleared')
                        else:
                            nao.say('oh something went wrong')

                    # run the demonstration of the project
                    elif command == 'test':
                        # TODO: RUNDEMO STILL NOT FINISHED - WE'RE MAKING PROGRESS
                        nao.say('starting demo')
                        nao.rundemo()

                    # NAO will rest
                    elif command == 'rest'
                        nao.motion('rest')

                    # stop processing and let NAO rest
                    elif command == "stop":
                        nao.say('ok, i will rest now!')
                        nao.motion('rest')
                        break

                except Exception as e:
                    nao.say('I dont know')
                    print 'WTF ... NONETYPE'
                    print e
        except Exception as e:
            print 'Keyword not recognized!!!'
            print e
