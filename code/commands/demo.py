from naoqi import ALProxy
import speech_recognition as sr
import time

class Demo:


    def __init__(self, ip, port):
        self.ip = ip
        self.port =  port
        self.r = sr.Recognizer()
        self.r.energy_threshold = 4000
        self.checked = []


    def say(self, text):

        tts = self.create_proxy("ALTextToSpeech")
        tts.setVolume(0.1)
        tts.say(text)


    def animatedHello(self, name):

        atts = self.create_proxy("ALAnimatedSpeech")

        animation = '^start(animations/Stand/Gestures/Hey_1)'
        wait = '^wait(animations/Stand/Gestures/Hey_1)'
        string = 'Hello,' + animation + name + wait
        atts.say(string)


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
            print 'Mic activated. Start listening...'
            audio = self.r.listen(source, phrase_time_limit=time)
            try:
                print 'Reconized: ' + self.r.recognize_google(audio)
                return self.r.recognize_google(audio)
            except LookupError, e:
                print e
                return 'there was an error!'
            except sr.UnknownValueError, e:
                print e
                print 'Reconized nothing within ' + str(time) + ' second!'
                return ''


    def filter_info(self, array):

        list = []
        faceInfo = array[1]

        for i in range( len(faceInfo) - 1 ):

            info = {}

            faceShapeInfo = faceInfo[i][0]
            faceExtraInfo = faceInfo[i][1]

            info['id'] = faceExtraInfo[0]
            info['score'] = faceExtraInfo[1]
            info['name'] = faceExtraInfo[2]
            info['alpha'] = faceShapeInfo[1]
            info['beta'] = faceShapeInfo[2]

            list.append(info)

        return list


    def turnBody(self, alpha, beta):

        motion = self.create_proxy('ALMotion')

        if alpha > 0.1 or alpha < -0.1:
        # turn body to direction of target

            motion.moveTo(0, 0, motion.getAngles(["HeadYaw"], False) + alpha)

        # turn head to direction of target
        motion.setAngles('HeadPitch', beta - 0.3, 0.1)
        time.sleep(2)


    def learnNewFace(self, rename = ''):

        faceProxy = self.create_proxy("ALFaceDetection")

        while True:

            # Someone reconized, but score probability is too low -> relearn
            if rename != '':
                self.say('Sorry, Are you ' + rename + '?')
                ans = self.speech_recognize(2.0)
                if ans == 'yes':
                    reLearnFace = faceProxy.reLearnFace(str(rename))
                    if reLearnFace:
                        self.say('Haha I know it! Thank you! ' + rename)
                        break
                    else:
                        self.say('Oh, sorry my dear!')
                        continue

            # learn new person
            self.say('Whats your name?')
            name = self.speech_recognize(2.0)

            if name != '':

                learnFace = faceProxy.learnFace(str(name))

                if learnFace:
                    self.say('thank you')
                    break
                else:
                    self.say('Something went wrong! Please position your face in front of mine!')
                    time.sleep(2)
                    print 'ERROR WITH LEARNING YOUR FACE!! '

    def greeting(self, faces):

        for face in faces:

            if face['name'] != '':

                if face['score'] <= 0.2:
                    self.learnNewFace()

                # less than 60%, can be him/her or not
                elif face['score'] <= 0.6:
                    self.learnNewFace(face['name'])

                # more than 60% probability
                elif face['score'] > 0.6 and face['name'] not in self.checked:
                    animatedHello(self, face['name'])
                    self.checked.append(face['name'])

            else:
                self.learnNewFace()


    def run(self):

        faceProxy = self.create_proxy("ALFaceDetection")
        memoryProxy = self.create_proxy("ALMemory")
        motion = self.create_proxy("ALMotion")
        faceProxy.subscribe("Test_Face", period, 0.0)

        motion.wakeUp()

        period = 500
        faces = []

        for i in range(4):

            motion.setAngles('HeadPitch', -0.4, 0.1)
            headYawPosition = -0.4

            for j in range(1,24):
                time.sleep(1)
                val = memoryProxy.getData("FaceDetected", 500)
                #print val

                if(val and isinstance(val, list) and len(val) == 5):

                    faces = self.filter_info(val)
                    print str(faces)

                    if -0.2 < faces[0]['alpha'] < 0.2 and -0.2 < faces[0]['beta'] < 0.2 :
                        self.greeting(faces)
                    else:
                        self.turnBody(faces[0]['alpha'], faces[0]['beta'])

                else:
                    print 'No one detected'
                    if j % 6 == 0:
                        motion.setAngles('HeadYaw', headposition, 0.1)
                        headYawPosition += 0.4

                time.sleep(1)

            # turn body 90 degree to left
            motion.setAngles('HeadYaw', 0, 0.1)
            motion.setAngles('HeadPitch', 0, 0.1)
            motion.moveTo(coords[0], coords[1], math.pi/2)
            time.sleep(2)


        faceProxy.unsubscribe("Test_Face")
        motion.rest()
        print "Test terminated successfully."




if __name__ == '__main__':

    demo = Demo('10.0.7.183', 9559)
    demo.run()
