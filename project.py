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
import speech_recognition as sr
from random import uniform
from functools import reduce

from commands import demo as d

class AssistentAgent():

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.r = sr.Recognizer()
        self.r.energy_threshold = 4000

    def speech_recognize(self, time):
        with sr.Microphone() as source:
            self.r.adjust_for_ambient_noise(source)
            print 'mic on... start recording!'
            audio = self.r.listen(source, phrase_time_limit=time)
            try:
                print 'Reconized words: ' + self.r.recognize_google(audio)
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
        elif state == 'getHeadyawAngle':
            return motion.getAngles(["HeadYaw"], False)

    ### Controlling facerecognition API
    def face(self, state):
        faceProxy = self.create_proxy("ALFaceDetection")
        faceProxy.setTrackingEnabled(False)

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
                    learn = faceProxy.learnFace(name)
                    self.say('look left')
                    time.sleep(1)
                    relearn = faceProxy.reLearnFace(name)
                    self.say('look right')
                    time.sleep(1)
                    relearn = faceProxy.reLearnFace(name)
                    if relearn:
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
                    print ' - Score: ' + str(face['score'])
                    print ' - Name: ' + str(face['name'])
                    print ' - Coords: ' + str(face['coords'])
                    #print ' - m = ' + reduce((lambda x, y: x / y), face['coords'])
                # --------------------------------------------------

                #print "I know you: %s" % name
                #data.append(name)
                #data.append(val[3])             # append CameraPose_InRobotFrame
                #faceProxy.unsubscribe("face")   # Unsubscribe the module.

            #else:
                ### nobody is detected
                #faceProxy.unsubscribe("face")   # Unsubscribe the module.

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
            print faceInfo[len(faceInfo) - 1]
            # ExtraInfo = [ faceID, scoreReco, faceLabel, leftEyePoints, ...], ShapeInfo = [ 0, alpha, beta, sizeX, sizeY ]
            info['score'] = faceExtraInfo[1]
            info['name'] = faceExtraInfo[2]
            info['coords'] = [faceShapeInfo[1], faceShapeInfo[2]]

            list.append(info)

        return list

    ### DEPRACTED
    ### The final demonstration of the project
    def rundemo(self):
        print "Demo is running"

        faceProxy = self.create_proxy("ALFaceDetection")
        ### initialize NAO for the demonstration
        self.motion('wakeUp')
        self.motion('moveHead', 'HeadPitch', -0.5)
        self.tracker('stop')
        checked = []

        period = 500
        faceProxy.subscribe("face", period, 0.0 )

        # outer loop: each loop do a 90 degree turn
        for i in range(4):
            j = 0
            angleOfHeadYaw = (-2.0)
            self.motion('moveHead', 'HeadPitch', -0.5)
            time.sleep(2)
            counter = 0

            # inner loop: each loop turn headyaw
            for j in range(3):
                faces = self.face('getdata')
                ### <NAME> IS RECOGNIZED - START GREETING PROCEDURE
                if faces:
                    for face in faces:
                        # recognize someone known and not checked
                        print 'Name: ' + face['name']
                        print 'Checked: ' + str(checked)
                        if not face['name'] in checked and face['score'] > 0.5:
                            ### turn into direction of recognized person
                            self.tracker('start')
                            headyaw_angle = self.motion('getHeadyawAngle')
                            if headyaw_angle > 0.5:
                                self.move('moveTo', [0,0,headyaw_angle[0]])
                                time.sleep(3)
                            self.tracker('stop')
                            # greet
                            self.animated('hello', face['name'])
                            checked.append(face['name'])            # mark as recognized
                            self.motion('moveHead', 'HeadPitch', -0.4)

                            # prevents nao is stuck while recognized someone
                            time.sleep(2)

                        ### SOMEONE UNKOWN IS RECOGNIZED - TRY TO LEARN
                        '''
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
                        '''

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
        faceProxy.unsubscribe("face")
        self.motion('rest')
        print "Demo is finished"

    ### DEPRACTED
    ### Controlling the facetracking function of nao
    def tracker(self, state):
        tracker = self.create_proxy("ALTracker")

        # start the tracker [modes: Head, Body, Move]
        if state == "start":
            targetName = "Face"
            faceWidth = 0.1
            tracker.setMode('Head')
            tracker.registerTarget(targetName, faceWidth)
            tracker.track(targetName)

        # stops the tracker and cleanup
        elif state == "stop":
            tracker.stopTracker()
            tracker.unregisterAllTargets()

    ### Controlling the movement of nao
    def move(self, cntrl, coords):
        motion = self.create_proxy("ALMotion")
        posture = self.create_proxy("ALRobotPosture")

        # Prepare NAO to walk
        motion.wakeUp()
        posture.goToPosture("StandInit", 0.5)

        # check which move to do
        if cntrl == 'forward':
            motion.moveTo(coords[0], 0, 0)
        elif cntrl == 'backward':
            motion.moveTo(-(coords[0]), 0, 0)
        elif cntrl == 'position':
            motion.moveTo(coords[3], coords[4], 0)
        elif cntrl == 'turnleft':
            theta = math.pi/2
            motion.moveTo(coords[0], coords[1], theta)
        elif cntrl == 'moveTo':
            motion.moveTo(coords[0], coords[1], coords[2])

    ### Learn a new person
    def newPerson(self):
        self.say('position yourself in front me')
        time.sleep(1)
        self.say('say ok when you are ready')
        resp = nao.speech_recognize(2.0).lower()
        if resp == 'ok':
            nao.face('learn')
        else:
            nao.say('oh something went wrong')

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

    nao.say('Hi, i am Norman!')

    while True:
        print "Waiting for Keyword"
        keyword = nao.speech_recognize(2.0).lower()
        print "You said: " + keyword
        if keyword == "norman":
            print "Yes?"

            nao.say('listening')
            command = nao.speech_recognize(2.0).lower()
            print "You said: " + command

            # test speech capabilities of NAO
            if command == 'hello':
                nao.say('hello')

            # wakeup NAO - goto motion standInit
            elif command == 'wake up':
                nao.motion('wakeUp')
                nao.motion('moveHead', 'HeadPitch', -0.6)

            # get stored faces
            elif command == 'get data':
                nao.face('getdb')

            # remove all faces from facedb
            elif command == 'clear data':
                nao.say('removing all faces from database')
                nao.face('cleardb')
                nao.say('database cleared')

            # execute face_learning phase
            elif command == 'new person':
                nao.learnPerson()

            # DEPRACTED
            # run the demonstration of the project
            elif command == 'test':
                # TODO: RUNDEMO STILL NOT FINISHED - WE'RE MAKING PROGRESS
                nao.say('starting demo')
                nao.rundemo()

            # start command from another module
            elif command == 'start':
                demo = d.Demo(nao_ip, port)
                demo.run()

            # NAO will rest
            elif command == 'rest':
                nao.motion('rest')

            elif command == 'left':
                nao.move('turnleft', [0,0])

            # stop processing and let NAO rest
            elif command == "stop":
                nao.say('ok, i will rest now!')
                nao.motion('rest')
                break
