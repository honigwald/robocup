from optparse import OptionParser
from naoqi import ALProxy
import speech_recognition as sr

class TestClass:


    def __init__(self):
        self.ip = '10.0.7.183'
        self.port =  9559
        self.r = sr.Recognizer()
        self.r.energy_threshold = 4000
        self.checked = []


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
            info['id'] = faceExtraInfo[0]
            info['score'] = faceExtraInfo[1]
            info['name'] = faceExtraInfo[2]
            info['coords'] = [faceShapeInfo[1], faceShapeInfo[2]]

            list.append(info)

        return list

    def greeting(self, faces):

        if faces:
            for face in faces:

                if face['name'] != '' and face['name'] not in self.checked:
                    print 'HELLO, ' + face['name']
                    self.checked.append(face['name'])

                elif face['name'] == '':
                    while True:
                        print 'WHATS YOUR NAME?:'
                        name = speech_recognize(5.0)
                        if name != '':
                            time.sleep(2)
                            faceProxy = create_proxy("ALFaceDetection")
                            learnFace = faceProxy.learnFace(name)
                            time.sleep(2)
                            print learnFace
                            if learnFace:
                                print 'i got it! ' + name
                                break
                            else:
                                print 'ERROR WITH LEARNING YOUR FACE!! '

                else:
                    print 'I already greet you, ' + face['name']

        else:
            print 'Nobody to greet!'


    def demo(self):

        faceProxy = self.create_proxy("ALFaceDetection")
        memoryProxy = self.create_proxy("ALMemory")

        period = 500
        faceProxy.setRecognitionConfidenceThreshold(0.7)
        faceProxy.setTrackingEnabled(False)
        faceProxy.subscribe("Test_Face", period, 0.0)

        memValue = "FaceDetected"
        faces = []

        for i in range(0, 20):
            time.sleep(2)
            val = memoryProxy.getData(memValue, 0)

            if(val and isinstance(val, list) and len(val) == 2):
                # We detected faces !
                # For each face, we can read its shape info and ID.
                # First Field = TimeStamp.
                faces = filter_info(val)
                print str(faces)

            self.greeting(faces)

        faceProxy.unsubscribe("Test_Face")
        print "Test terminated successfully."



if __name__ == '__main__':

    test = TestClass()
    test.demo()
