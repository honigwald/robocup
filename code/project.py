'''
USAGE:
    - type in terminal: python project.py "10.0.7.1X"
    - X is the number of the naobot
    - default port is 9559 for all naobot in the project
'''

import sys
import time
import math
from naoqi import ALProxy
from hello import *
import speech_recognition as sr
from random import uniform

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

    ### Goto predefined motions
    def motion(self, state, joint = None, angle = None):
        try:
            motion = ALProxy("ALMotion", self.ip, self.port)
        except Exception, e:
            print "Error when creating face detection proxy:"
            print str(e)

        if state == 'wakeUp':
            motion.wakeUp()
        elif state == 'rest':
            motion.rest()
        elif state == 'moveHead' and joint != None and angle != None:
            # motion.setStiffnesses(joint, 1)
            fractionMaxSpeed  = 0.2
            motion.setAngles(joint, angle, fractionMaxSpeed)

    ### Controlling facerecognition API
    def face(self, state):
        try:
            faceProxy = ALProxy("ALFaceDetection", self.ip, self.port)
        except Exception, e:
            print "Error when creating face detection proxy:"
            print str(e)

        # store recognized face with given name in database
        if state == 'learn':
            while True:                     # loops until NAO understood the correct name
                name = ''
                resp = ''
                self.say('Whats your name')
                name = self.speech_recognize(2.0).lower()
                name = str(name)
                self.say('Is')
                self.say(name)
                self.say('correct. say yes')
                resp = self.speech_recognize(1.0).lower()
                resp = str(resp)
                if resp == 'yes':           # finally learn face-name-tuple
                    print "response " + resp
                    if faceProxy.learnFace(name):
                        print "Actual DB: %s" % (faceProxy.getLearnedFacesList())
                        self.say('Thank you')
                        break
                    else:
                        self.say('Oh I had a problem')
                        print "Something went wrong"
                elif resp == 'stop':
                    break

        # remove all names stored in database
        elif state == 'cleardb':
            if (faceProxy.clearDatabase()):
                print "DB cleared"
                print "Actual DB: %s" % (faceProxy.getLearnedFacesList())
            else:
                print "Something went wrong"

        # returns the name of recognized person
        elif state == 'getname':
            period = 500
            faceProxy.subscribe("face", period, 0.0 )
            memValue = "FaceDetected"
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
                name = val[1][0][1][2]
                print "I know you: %s" % name
            else:
                print "Unkown person"
                name = ''

            faceProxy.unsubscribe("face")   # Unsubscribe the module.
            return name

        # prints content of database
        elif state == 'getdb':
            print "Actual DB: %s" % (faceProxy.getLearnedFacesList())

    ### The final demonstration of the project
    def rundemo(self):
        print "Demo is running"

        ### initialize NAO for the demonstration
        self.motion('wakeUp')
        self.motion('moveHead', 'HeadPitch', -0.6)
        self.tracker('start')
        checked = []                        # This array stores already greeted people
        angleOfHeadYaw = -(math.pi)

        for i in range(0,4):                            # outer loop - turn your body 90* left
            j = 0
            while j < 3:                                # inner loop - head looks from right 2center 2left
                if self.tracker('check'):               # check if a target is detected
                    name = self.face('getname')
                    print name
                    print "Checked: %s" % checked
                    if str(name) in checked:            # check if target already recognized
                        print "Checked: %s" % checked
                        continue
                    else:
                        name = str(name)
                        if name != '':                  # check if we have a name
                            if name in checked:         # check if target already greeted
                                continue
                            else: 
                                self.animated('hello', name)
                                checked.append(name)    # mark name as greeted
                        else:
                            ### TODO: TESTING - DETECTED SOMEONE WHO IS NOT KNOWN
                            self.say('hello')
                            self.say('would you tell me your name')
                            time.sleep(1)
                            self.say('then say yes')
                            resp = nao.speech_recognize(2.0).lower()
                            resp = str(resp)
                            if resp == 'yes':           # start learning
                                self.face('learn')
                            else:                       # person won't tell his name
                                self.say('awww. thats sad')
                        time.sleep(3)
                # no target detected
                else:
                    # move head of NAO - in three steps from right to left
                    angleOfHeadYaw = angleOfHeadYaw + (math.pi)/2
                    self.motion('moveHead', 'HeadYaw', angleOfHeadYaw)
                    j += 1
                    time.sleep(3)
                ### --- END OF INNER LOOP --- ### 

            # turn left in place
            coords = [0.0, 0.0]
            nao.move('turnleft', coords)
            ### --- END OF OUTER LOOP --- ### 

        # cleanup after finished demonstration
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

        # start the tracker [modes: Head, Body, Move]
        if state == "start":
            targetName = "Face"
            faceWidth = 0.1
            tracker.setMode('Move')
            tracker.registerTarget(targetName, faceWidth)
            tracker.track(targetName)

        # return true if new target is detected
        elif state == "check":
            if tracker.isNewTargetDetected():
                return True
            else:
                # stop tracker to manualy move the head
                #self.tracker('stop')
                # random move of head yaw
                # start tracker again to return to the flow
                #self.tracker('start')
                return False

        # stops the tracker and cleanup
        elif state == "stop":
            tracker.stopTracker()
            tracker.unregisterAllTargets()

    ### Controlling the movement of nao
    ### TODO: HERE WE'VE TO IMPLEMENT RANDOM MOVEMENT
    def move(self, cntrl, coords):
        try:
            motion = ALProxy("ALMotion", self.ip, self.port)
            posture= ALProxy("ALRobotPosture", self.ip, self.port)

            # Prepare NAO to walk
            motion.wakeUp()
            posture.goToPosture("StandInit", 0.5)
            #motion.standInit()

            # check which move to do
            if cntrl == 'forward':
                motion.moveTo(coords[0], 0, 0)
            elif cntrl == 'backward':
                motion.moveTo(-(coords[0]), 0, 0)
            elif cntrl == 'turnleft':
                theta = math.pi/2
                motion.moveTo(coords[0], coords[1], theta)

            motion.rest()

        except Exception, e:
            print e

    ### Nao speaks given text
    def say(self, text):
        try:
            tts = ALProxy("ALTextToSpeech", self.ip, self.port)
            tts.setVolume(0.5)
            tts.say(text)

        except Exception, e:
            print "Could not create proxy to ALTextToSpeech!"
            print "Error was: ", e

    ### Nao speaks given text with emotions ;)
    def animated(self, cntrl, name):
        try:
            atts = ALProxy("ALAnimatedSpeech", self.ip, self.port)

            if cntrl == 'hello':
                animation = '^start(animations/Stand/Gestures/Hey_1)'
                wait = '^wait(animations/Stand/Gestures/Hey_1)'
                string = 'Hi' + animation + name + 'nice to see you' + wait
                atts.say(string)

        except Exception, e:
            print "Could not create proxy to ALTextToSpeech!"
            print "Error was: ", e


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
            keyword = nao.speech_recognize(1).lower()
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
                    elif command == 'database':
                        nao.face('getdb')

                    # wakeup NAO - goto motion standInit
                    elif command == 'wake up':
                        nao.motion('wakeUp')
                        nao.motion('moveHead', 'HeadPitch', -0.6)

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
                    elif command == 'rest':
                        nao.motion('rest')

                    # stop processing and let NAO rest
                    elif command == "stop":
                        nao.say('ok, i will rest now!')
                        nao.motion('rest')
                        break

                    elif command == "move":
                        coords = [0.0, 0.0]
                        nao.move('turnleft', coords)


                except Exception as e:
                    nao.say('I dont know')
                    print 'WTF ... NONETYPE'
                    print e
        except Exception as e:
            print 'Keyword not recognized!!!'
            print e
