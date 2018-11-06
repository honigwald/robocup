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

    ### Controlling facerecognition API
    def face(self, state):
        try:
            faceProxy = ALProxy("ALFaceDetection", self.ip, self.port)
        except Exception, e:
            print "Error when creating face detection proxy:"
            print str(e)

        if state == 'learn':
            self.say('Tell me your name')
            name = self.speech_recognize(1.0).lower()
            if (faceProxy.learnFace(name)):
                print "Learning is complete"
                self.say('Thank you')
            else:
                print "Something went wrong"
        elif state == 'cleardb':
            if (faceProxy.clearDatabase()):
                print "DB cleared"
                self.say('Database cleared')
            else:
                print "Something went wrong"
        elif state == 'identify':
            period = 500
            faceProxy.subscribe("Test_Face", period, 0.0 )
            memValue = "FaceDetected"
            try:
                memoryProxy = ALProxy("ALMemory", self.ip, self.port)
            except Exception, e:
                print "Error when creating memory proxy:"
                print str(e)
                exit(1)

            val = memoryProxy.getData(memValue, 0)
            if(val and isinstance(val, list) and len(val) == 5):
                # We detected faces !
                # For each face, we can read its shape info and ID.
                # First Field = TimeStamp.
                timeStamp = val[0]
                # Second Field = array of face_Info's.
                faceInfoArray = val[1]

                ### THIS IS IMPORTANT
                ### DETERMINING THE NAME OF RECOGNIZED PERSON
                print "Name of recognized Person: %s" % val[1][0][1][2]
                name = val[1][0][1][2]
                if name != '':
                    name = "unknown"
            else:
                print "Error with getData. ALValue = %s" % (str(val))

            # Unsubscribe the module.
            faceProxy.unsubscribe("Test_Face")
            return name

        ### The final demonstration of the project
        def rundemo(self):
            #TODO: Actually it's just some small testing here
            print "Demo is running"
            self.motion('wakeUp')
            self.tracker('start')

            for i in 20:
                self.tracker('check')
                name = self.face('identify')
                if name != 'unknown':
                    self.say('Hello')
                    self.say(name)
                time.sleep(1)
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
                tracker.setMode('Head')
                tracker.registerTarget(targetName, faceWidth)

                # Then, start tracker.
                tracker.track(targetName)

            elif state == "check":
                if tracker.isNewTargetDetected():
                    print "new target detected"
                else:
                    print "no target"

            elif state == "stop":
                tracker.stopTracker()
                tracker.unregisterAllTargets()

        ### Controlling the movement of nao
        def move(self, X, Y):
        try:
            motionProxy  = ALProxy("ALMotion", self.ip, self.port)
            postureProxy = ALProxy("ALRobotPosture", self.ip, self.port)

            # Wake up robot
            motionProxy.wakeUp()

            # Send robot to Stand
            postureProxy.goToPosture("StandInit", 0.5)

            # go to position x, y
            Theta = 0.0
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
            tts.say(text)

        except Exception, e:
            print "Could not create proxy to ALTextToSpeech!"
            print "Error was: ", e


    ### Make a proxy to nao's ALFaceDetection and enable/disable tracking.
    def set_nao_face_detection_tracking(nao_ip, nao_port, tracking_enabled):
        try:
            faceProxy = ALProxy("ALFaceDetection", self.ip, self.port)
        except Exception, e:
            print e

        print "Will set tracking to '%s' on the robot ..." % tracking_enabled

        # Enable or disable tracking.
        faceProxy.enableTracking(tracking_enabled)

        # Just to make sure correct option is set.
        print "Is tracking now enabled on the robot?", faceProxy.isTrackingEnabled()


    ### let nao do a motion based on the state
    def motion(self, state):
        try:
            motionProxy = ALProxy("ALMotion", self.ip, self.port)
            detector.terminate()

            if state == 'wakeUp':
                motionProxy.wakeUp()

            elif state == 'rest':
                motionProxy.rest()

        except Exception, e:
            print "Could not create proxy to ALRobotPosture"
            print "Error was: ", e


#=============================================================
# INSECURE CODE SNIPPETS - NOT SURE IF NEEDED - END IS MARKED
#=============================================================
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


    # simple example for build-in posture
    def posture(self, posture):

        try:
            postureProxy = ALProxy("ALRobotPosture", self.ip, self.port)
            postureProxy.goToPosture(posture, 1.0)
        except Exception, e:
            print "Could not create proxy to ALRobotPosture"
            print "Error was: ", e
#=============================================================
# END OF INSECURE CODE SNIPPETS
#=============================================================

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

    # TODO: print statements in nao.say()
    while True:
        print "Waiting for Keyword"
        nao.say('awaiting keyword!')
        try:
            keyword = nao.speech_recognize(1.0).lower()
            print "You said: " + keyword
            if keyword == "alexa":
                print "Listening..."
                nao.say('listening')
                try:
                    command = nao.speech_recognize(2.0).lower()
                    print "You said: " + command

                    # test speech capabilities of NAO
                    if command == 'hello':
                        nao.say('hello')

                    # wakeup NAO - goto motion standInit
                    elif command == 'wake up':
                        nao.motion('wakeUp')

                    # execute face_learning phase
                    elif command == 'learn new face':
                        # TODO: NEEDS TO BE TESTED
                        # RESULT: Voice speed has to slowdown!
                        nao.say('position yourself in front of my cameras.')
                        nao.say('say ok when you are ready')
                        resp = nao.speech_recognize(2.0).lower()
                        if resp == 'ok':
                            nao.face('learn')
                        else:
                            nao.say('oh oh something went wrong')

                    # remove all faces from facedb
                    elif command == 'clear all faces':
                        # TODO: NEEDS TO BE TESTED
                        nao.say('removing all faces from face database')
                        nao.say('say ok if you really want that')
                        resp = nao.speech_recognize(2.0).lower()
                        if resp == 'ok':
                            nao.face('cleardb')
                            nao.say('database cleared')
                        else:
                            nao.say('oh oh something went wrong')

                    # run the demonstration of the project
                    elif command == 'start demo':
                        # TODO
                        nao.say('starting demo')
                        nao.rundemo()

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
