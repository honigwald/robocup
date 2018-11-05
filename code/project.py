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

    #def learn_face(self, name):
    def flearn(self, name):
        try:
            faceProxy = ALProxy("ALFaceDetection", self.ip, self.port)
        except Exception, e:
            print "Error when creating face detection proxy:"
            print str(e)

        #print "Actual DB: %s" % (faceProxy.getLearnedFacesList()) 
        if (faceProxy.learnFace(name)):
            print "Learning is complete"
        else:
            print "Something went wrong"

    #def clear_facedb(self):
    def fcleardb(self):
        try:
            faceProxy = ALProxy("ALFaceDetection", self.ip, self.port)
        except Exception, e:
            print "Error when creating face detection proxy:"
            print str(e) 

        #print "Actual DB: %s" % (faceProxy.getLearnedFacesList()) 
        if (faceProxy.clearDatabase()):
            print "DB cleared"
        else:
            print "Something went wrong"

    def fidentify(self):
        try:
            faceProxy = ALProxy("ALFaceDetection", self.ip, self.port)
        except Exception, e:
            print "Error when creating face detection proxy:"
            print str(e) 

        period = 500
        faceProxy.subscribe("Test_Face", period, 0.0 )

        # ALMemory variable where the ALFaceDetection module
        # outputs its results.
        memValue = "FaceDetected"

        # Create a proxy to ALMemory
        try:
            memoryProxy = ALProxy("ALMemory", IP, PORT)
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


    def demo(self):
        return 0

    def faceTracker(self):
        try:
            motion = ALProxy("ALMotion", self.ip, self.port)
        except Exception, e:
            print "Could not create proxy to ALMotion!"
            print "Error was: ", e
            return

        try:
            tracker = ALProxy("ALTracker", self.ip, self.port)
        except Exception, e:
            print "Could not create proxy to ALTracker!"
            print "Error was: ", e
            return

        # Add target to track.
        tracker.setMode('Move')
        targetName = "Face"
        faceWidth = 0.1
        tracker.registerTarget(targetName, faceWidth)

        # Then, start tracker.
        tracker.track(targetName)

        try:
            while True:
                # TODO TESTEN!!!!
                if tracker.isNewTargetDetected():
                    # Stop tracker.
                    tracker.stopTracker()
                    tracker.unregisterAllTargets()
                    motion.rest()
                    break

                else:
                    time.sleep(1)

        except KeyboardInterrupt:
            print
            print "Interrupted by user"
            print "Stopping..."


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
                self.say('ok')
                motionProxy.wakeUp()

            elif state == 'rest':
                self.say('ok')
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
                nao.say('listen for a command!')
                try:
                    command = nao.speech_recognize(2.0).lower()
                    print "You said: " + command

                    # test speech capabilities of NAO
                    if command == 'hello':
                        nao.say('hello, sir!')

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
                            nao.say('tell me your name')
                            name = nao.speech_recognize(1.0).lower()
                            nao.flearn(name)
                        else:
                            nao.say('oh oh something went wrong')

                    # remove all faces from facedb
                    elif command == 'clear all faces':
                        # TODO: NEEDS TO BE TESTED
                        nao.say('removing all faces from face database')
                        nao.say('say ok if you really want that')
                        resp = nao.speech_recognize(2.0).lower()
                        if resp == 'ok':
                            nao.fcleardb(name)
                            nao.say('database cleared')
                        else:
                            nao.say('oh oh something went wrong')

                    # run the demonstration of the project
                    elif command == 'start demo':
                        # TODO
                        print "todo"

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
