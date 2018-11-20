from optparse import OptionParser
from naoqi import ALProxy
import speech_recognition as sr
import time

class TestClass:


    def __init__(self):
        self.ip = '10.0.7.183'
        self.port =  9559
        self.r = sr.Recognizer()
        self.r.energy_threshold = 4000
        self.checked = []


    def say(self, text):

        tts = self.create_proxy("ALTextToSpeech")
        tts.setVolume(0.1)
        tts.say(text)


    def create_proxy(self, name):

        try:
            proxy = ALProxy(name, self.ip, self.port)
        except Exception, e:
            print "Error when creating " + name + " proxy:"
            print str(e)

        return proxy


    def speech_recognize(self, time):
        with sr.Microphone() as source:
            self.r.adjust_for_ambient_noise(source)
            print 'mic on... start recording!!!'
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


    def filter_info(self, array):

        list = []

        #  array = [ TimeStamp, [ FaceInfo[N], Time_Filtered_Reco_Info ], CameraPose_InTorsoFrame, CameraPose_InRobotFrame, Camera_Id ]
        faceInfo = array[1]

        # faceInfoArray = [ FaceInfo[N], Time_Filtered_Reco_Info ], get rid of Time_Filtered_Reco_Info in faceInfoArray
        for i in range( len(faceInfo) - 1 ):

            info = {}

            # FaceInfo = [ ShapeInfo, ExtraInfo[N] ?????? ]
            faceShapeInfo = faceInfo[i][0]
            faceExtraInfo = faceInfo[i][1]

            # ExtraInfo = [ faceID, scoreReco, faceLabel, leftEyePoints, ...], ShapeInfo = [ 0, alpha, beta, sizeX, sizeY ]
            info['id'] = faceExtraInfo[0]
            info['score'] = faceExtraInfo[1]
            info['name'] = faceExtraInfo[2]
            info['alpha'] = faceShapeInfo[1]
            info['beta'] = faceShapeInfo[2]

            list.append(info)

        return list

    def turnBody(self, alpha, beta):
        motion = self.create_proxy('ALMotion')

        print alpha > 0.1 or alpha < -0.1
        if alpha > 0.1 or alpha < -0.1:
        # turn body to direction of target

            motion.moveTo(0, 0, alpha)

        # turn head to direction of target
        #motion.setAngles('HeadYaw', alpha, 0.1)
        motion.setAngles('HeadPitch', beta - 0.3, 0.1)
        time.sleep(1)


    def learnNewFace(self, rename = ''):

        faceProxy = self.create_proxy("ALFaceDetection")

        while True:

            if rename != '':
                self.say('Are you ' + rename + '?')
                ans = self.speech_recognize(2.0)
                if ans == 'yes':
                    reLearnFace = faceProxy.reLearnFace(str(rename))
                    if reLearnFace:
                        self.say('thank you, ' + rename)
                        break
                    else:
                        self.say('got an error')


            self.say('Whats your name?')
            name = self.speech_recognize(2.0)
            print str(name)
            if name != '':

                time.sleep(2)
                #nm = self.name.pop(0)
                learnFace = faceProxy.learnFace(str(name))
                time.sleep(2)
                #print learnFace
                #relearnFace = self.relearnFace(str(name))
                #time.sleep(2)


                if learnFace:
                    self.say('thank you')
                    break
                else:
                    self.say('got an error')
                    break
                    print 'ERROR WITH LEARNING YOUR FACE!! '

    def greeting(self, faces):


        print faces
        if faces:
            for face in faces:

                time.sleep(2)

                if face['name'] != '':

                    if face['score'] < 0.2:
                        self.learnNewFace()
                    elif face['score'] < 0.6:
                        self.learnNewFace(face['name'])
                    #elif face['name'] not in self.checked:
                    else:
                        self.say('hi, ' + face['name'])
                        #self.checked.append(face['name'])

                elif face['name'] == '':
                    self.learnNewFace()

                else:
                    print 'I already greet you.'

        else:
            print 'Nobody to greet!'


    def demo(self):

        faceProxy = self.create_proxy("ALFaceDetection")
        memoryProxy = self.create_proxy("ALMemory")
        motion = self.create_proxy("ALMotion")
        motion.wakeUp()
        motion.setAngles('HeadPitch', -0.4, 0.1)

        faceProxy.clearDatabase()

        period = 500

        #faceProxy.setTrackingEnabled(False)
        faceProxy.subscribe("Test_Face", period, 0.0)

        memValue = "FaceDetected"
        faces = []
        lp = [10, 10]

        for i in range(0, 200):
            time.sleep(1)
            val = memoryProxy.getData(memValue, 0)
            #print val

            if(val and isinstance(val, list) and len(val) == 5):

                faces = self.filter_info(val)
                print str(faces)

                a = faces[0]['alpha']
                b = faces[0]['beta']
                score = faces[0]['score']
                # TESTING !!!
                # Turn body to the first recognized target



                if -0.2 < a < 0.2 and -0.2 < b < 0.2 :
                    self.greeting(faces)
                else:
                    self.turnBody(faces[0]['alpha'], faces[0]['beta'])
            else:
                print 'No one'
            time.sleep(1)

        faceProxy.unsubscribe("Test_Face")
        print "Test terminated successfully."



if __name__ == '__main__':

    test = TestClass()
    test.demo()
