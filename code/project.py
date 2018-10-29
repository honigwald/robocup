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
import json
import speech_recognition as sr


class AssistentAgent:

    port = 9559

    def __init__(self, ip):
        self.ip = ip
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


    def learn_face(self):

        try:
            faceProxy = ALProxy("ALFaceDetection", IP, PORT)
        except Exception, e:
            print "Error when creating face detection proxy:"
            print str(e)

        # TODO Finish this function


    def demo(self):
        return 0


    def faceTracker(self):

        try:
            motion = ALProxy("ALMotion", IP, PORT)
        except Exception, e:
            print "Could not create proxy to ALMotion!"
            print "Error was: ", e
            return

        try:
            tracker = ALProxy("ALTracker", IP, PORT)
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


    def set_nao_face_detection_tracking(nao_ip, nao_port, tracking_enabled):
        """Make a proxy to nao's ALFaceDetection and enable/disable tracking.
        """
        try:
            faceProxy = ALProxy("ALFaceDetection", self.ip, self.port)
        except Exception, e:
            print e

        print "Will set tracking to '%s' on the robot ..." % tracking_enabled

        # Enable or disable tracking.
        faceProxy.enableTracking(tracking_enabled)

        # Just to make sure correct option is set.
        print "Is tracking now enabled on the robot?", faceProxy.isTrackingEnabled()


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


    # -----------------------------------------------------------------------
    # let nao do a motion based on the state

    def faceLearning(self):

        try:
            faceProxy = ALProxy("ALFaceDetection", IP, PORT)
        except Exception, e:
            print "Error when creating face detection proxy:"
            print str(e)

        # TODO Finish this function


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


    #------------------------------------------------------------------------

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
        nao.say('waiting for a hotword!')
        try:
            hotword = nao.speech_recognize(1.0).lower()
            print "You said: " + hotword
            if hotword == "alexa":
                print "I listen for command... sir"
                nao.say('listen for a command!')
                try:
                    command = nao.speech_recognize(2.0).lower()
                    print "You said: " + command

                    if command == 'hello':
                        nao.say('hello, sir!')

                    elif command == 'wake up':
                        nao.motion('wakeUp')

                    elif command == "stop":
                        nao.say('ok, i will rest now!')
                        nao.motion('rest')
                        break

                    elif command == 'start face learning':
                        # TODO

                    elif command == 'start demo':
                        # TODO
                except Exception as e:
                    nao.say('Sorry, i do not understand what you want from me.')
                    print 'WTF ... NONETYPE'
        except Exception as e:
            print 'not alexa!!!'
            print e
