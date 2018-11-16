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
from functools import reduce

class AssistentAgent:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.r = sr.Recognizer()
        self.r.energy_threshold = 4000

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
                print 'what do you mean? i do not understand'
                return ''

    def create_proxy(self, name):

        try:
            proxy = ALProxy(name, self.ip, self.port)
        except Exception, e:
            print "Error when creating " + name + " proxy:"
            print str(e)

        return proxy

    ### Goto predefined motions
    def motion(self, state, joint = None, angle = None):

        motion = self.create_proxy("ALMotion")

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

        faceProxy = self.create_proxy("ALFaceDetection")

        faceProxy.setTrackingEnabled(False)
        #faceProxy.setRecognitionConfidenceThreshold(0.6)

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

        # returns the name and position of recognized persons
        elif state == 'getdata':
            period = 500
            faceProxy.subscribe("face", period, 0.0 )
            memValue = "FaceDetected"

            memoryProxy = self.create_proxy("ALMemory")

            # store all return values data = [[name, coords], [...]]
            data = []
            val = memoryProxy.getData(memValue, 0)

            if(val and isinstance(val, list) and len(val) == 5):
                ### THIS IS IMPORTANT
                ### DETERMINING THE NAME OF RECOGNIZED PERSON

                #name = val[1][0][1][2]

                # NEED TESTS!!! ------------------------------------
                data = self.filter_info(val)             # replace data with faceData if work
                for i, face in enumerate(data):
                    print str(i) + '. Face information:'
                    print ' - ID: ' + str(face['id'])
                    print ' - Name: ' + str(face['name'])
                    print ' - Coords: ' + str(face['coords'])
                    #print ' - m = ' + reduce((lambda x, y: x / y), face['coords'])
                # --------------------------------------------------

                #print "I know you: %s" % name
                #data.append(name)
                #data.append(val[3])             # append CameraPose_InRobotFrame
                faceProxy.unsubscribe("face")   # Unsubscribe the module.

            else:
                ### nobody is detected
                faceProxy.unsubscribe("face")   # Unsubscribe the module.

            return data

        # prints content of database
        elif state == 'getdb':
            print "Actual DB: %s" % (faceProxy.getLearnedFacesList())

    def filter_info(self, array):

        list = []
        print array

        #  array = [ TimeStamp, [ FaceInfo[N], Time_Filtered_Reco_Info ], CameraPose_InTorsoFrame, CameraPose_InRobotFrame, Camera_Id ]
        faceInfo = array[1]

        # faceInfoArray = [ FaceInfo[N], Time_Filtered_Reco_Info ], get rid of Time_Filtered_Reco_Info in faceInfoArray
        for i in range( len(faceInfo) - 1 ):

            info = {}

            # FaceInfo = [ ShapeInfo, ExtraInfo[N] ?????? ]
            faceShapeInfo = faceInfo[i][0]
            faceExtraInfo = faceInfo[i][1]

            #print faceExtraInfo

            # ExtraInfo = [ faceID, scoreReco, faceLabel, leftEyePoints, ...], ShapeInfo = [ 0, alpha, beta, sizeX, sizeY ]
            info['id'] = faceExtraInfo[0]
            info['name'] = faceExtraInfo[2]
            info['coords'] = [faceShapeInfo[1], faceShapeInfo[2]]

            list.append(info)

        return list

    ### The final demonstration of the project
    def rundemo(self):
        print "Demo is running"

        ### initialize NAO for the demonstration
        self.motion('wakeUp')
        self.motion('moveHead', 'HeadPitch', -0.6)
        self.tracker('stop')
        checked = []                                    # This array stores already greeted people

        for i in range(4):                            # outer loop - turn your body 90* left
            j = 0
            angleOfHeadYaw = (-2.0)
            self.motion('moveHead', 'HeadPitch', -0.4)
            time.sleep(2)
            counter = 0

            for j in range(3):                                # inner loop - head looks from right 2center 2left

                # TODO: direct head of nao to face of person if 1. someone recognized and known and 2. someone recognized and unknown
                faces = self.face('getdata')

                ### <NAME> IS RECOGNIZED - START GREETING PROCEDURE
                #if data and data[0] != '' and data[0] not in checked:
                if faces:
                #if data and data[0] != '':
                    #self.move('position', data[1])
                    for face in faces:
                        # recognize someone known and not checked
                        print 'Name: ' + face['name']
                        print 'Checked: ' + str(checked)
                        if face['name'] != '' and not face['name'] in checked:
                            #name = data[0]
                            #if str(name) not in checked:        # check if target already recognized
                                # greet
                            self.animated('hello', face['name'])
                            checked.append(face['name'])            # mark as recognized
                            self.motion('moveHead', 'HeadPitch', -0.4)

                            # prevents nao is stuck while recognized someone
                            time.sleep(2)
                            '''
                            counter += 1
                            if counter == 5:
                                angleOfHeadYaw = angleOfHeadYaw + 1.0
                                self.motion('moveHead', 'HeadYaw', angleOfHeadYaw)
                                j += 1
                        '''

                        ### SOMEONE UNKOWN IS RECOGNIZED - TRY TO LEARN
                        elif face['name'] == '':
                            #self.tracker('start')
                            #self.motion('moveHead', 'HeadYaw', face['coords'][1])
                            #self.motion('moveHead', 'HeadPitch', face['coords'][0])
                            #self.move('position', data[1][3:4])
                            #print data[1][3:4]
                            self.say('hello')
                            self.say('would you tell me your name')
                            time.sleep(0.5)
                            self.say('say yes')
                            resp = nao.speech_recognize(2.0).lower()
                            resp = str(resp)
                            if resp == 'yes':                 # start learning
                                self.face('learn')
                            else:                             # person won't tell his name
                                self.say('awww. thats sad')
                            #self.tracker('stop')
                            #print data

                ### NO ONE IS RECOGNIZED
                # move head of NAO - in three steps from right to left
                angleOfHeadYaw = angleOfHeadYaw + 1.0
                self.motion('moveHead', 'HeadYaw', angleOfHeadYaw)
                time.sleep(3)

                ### --- END OF INNER LOOP --- ###

            self.motion('moveHead', 'HeadYaw', 0)
            # turn left in place
            nao.move('turnleft', [0.0, 0.0])
            time.sleep(2)
            ### --- END OF OUTER LOOP --- ###

        # cleanup after finished demonstration
        #self.tracker('stop')
        self.motion('rest')
        print "Demo is finished"

    ### Controlling the facetracking function of nao
    def tracker(self, state):

        tracker = self.create_proxy("ALTracker")

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

        motion = self.create_proxy("ALMotion")
        posture = self.create_proxy("ALRobotPosture")

        # Prepare NAO to walk
        motion.wakeUp()
        posture.goToPosture("StandInit", 0.5)
        #motion.standInit()

        # check which move to do
        if cntrl == 'forward':
            motion.moveTo(coords[0], 0, 0)
        elif cntrl == 'backward':
            motion.moveTo(-(coords[0]), 0, 0)
        elif cntrl == 'position':
            print coords
            motion.moveTo(coords[3], coords[4], 0)
        elif cntrl == 'turnleft':
            theta = math.pi/2
            motion.moveTo(coords[0], coords[1], theta)


    ### Nao speaks given text
    def say(self, text):

        tts = self.create_proxy("ALTextToSpeech")
        tts.setVolume(0.1)
        tts.say(text)

    ### Nao speaks given text with emotions ;)
    def animated(self, cntrl, name):
        atts = self.create_proxy("ALAnimatedSpeech")

        if cntrl == 'hello':
            animation = '^start(animations/Stand/Gestures/Hey_1)'
            wait = '^wait(animations/Stand/Gestures/Hey_1)'
            string = 'Hi' + animation + name + 'nice to see you' + wait
            atts.say(string)


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

    #nao.say('awaiting keyword!')
    #nao.say('hello')
    nao.face('cleardb')
    nao.rundemo()
    # nao.move(0.8, 0.4)
    while True:
        print "Waiting for Keyword"
        keyword = nao.speech_recognize(2.0).lower()
        print "You said: " + keyword
        if keyword == "no":
            print "Listening..."

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
                nao.face('cleardb')
                nao.say('database cleared')

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
