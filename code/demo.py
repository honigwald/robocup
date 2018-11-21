from naoqi import ALProxy
import speech_recognition as sr
import time
import math

class Demo():


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

            info['name'] = faceExtraInfo[2]
            info['score'] = faceExtraInfo[1]
            info['alpha'] = faceShapeInfo[1]
            info['beta'] = faceShapeInfo[2]

            list.append(info)

        return list


    def turnBody(self, alpha, beta):

        motion = self.create_proxy('ALMotion')

        headYawP = motion.getAngles(["HeadYaw"], False)[0]

        if headYawP != 0:
            motion.setAngles('HeadYaw', 0, 0.1)

        if alpha- headYawP > 0.1 or alpha - headYawP < -0.1:
            motion.moveTo(0, 0, + headYawP + alpha)

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

    def greeting(self, face):

        if face['name'] != '':

            if face['score'] <= 0.2:
                self.learnNewFace()

            # less than 60%, can be him/her or not
            elif face['score'] <= 0.6:
                self.learnNewFace(face['name'])

            # more than 60% probability
            elif face['score'] > 0.6 and face['name'] not in self.checked:
                motion = self.create_proxy('ALMotion')

                headPitchP = motion.getAngles(["HeadPitch"], False)
                self.animatedHello(face['name'])

                motion.setAngles(["HeadPitch"], headPitchP[0], 0.1)
                self.checked.append(face['name'])

            else:
                print 'already greeted!!!'

        else:
            self.learnNewFace()

    # this filter will compare all faces and return the person (index) with the lowest score
    def compareFaces(self, faces):

        # remove all faces with more than 0.7 score
        for face in faces:
            if face['name'] in self.checked and face['score'] > 0.7 and len(faces) > 1:
                # remove face from faces
                faces.remove(face)


        scores = [face['score'] for face in faces]
        alphas = [face['alpha'] for face in faces]
        betas = [face['beta'] for face in faces]
        distances = map(lambda a, b: math.sqrt(a**2 + b**2), alphas, betas)

        # TODO HOW IS THE PRIORITY FOR FACES? DISTANCE OR SCORE?
        #minScore = scores.index(min(scores))
        minDistance = distances.index(min(distances))

        return minDistance


    def run(self):

        # Init
        faceProxy = self.create_proxy("ALFaceDetection")
        memoryProxy = self.create_proxy("ALMemory")
        motion = self.create_proxy("ALMotion")

        faceProxy.clearDatabase()

        faceProxy.subscribe("Test_Face", 500, 0.0)
        motion.wakeUp()

        faces = []

        # Main loop
        for i in range(4):

            # For each loop set head into position
            motion.setAngles('HeadPitch', -0.4, 0.1)
            headYawPosition = -0.6

            # side loop: for each iteration check for face recognition
            for j in range(1,24):

                time.sleep(1)
                val = memoryProxy.getData("FaceDetected", 500)

                if(val and isinstance(val, list) and len(val) == 5):

                    faces = self.filter_info(val)
                    print str(faces)
                    index = self.compareFaces(faces)
                    face = faces[index]
                    print 'lowest score: ' + str(faces[index])

                    if -0.2 < face['alpha'] < 0.2 and -0.2 < face['beta'] < 0.2 :
                        self.greeting(face)
                    else:
                        self.turnBody(face['alpha'], face['beta'])
                        j -= 1

                else:
                    print 'No one detected'

                    # turn head, avoid deadlock
                    if j % 6 == 0:
                        motion.setAngles(['HeadYaw', 'HeadPitch'], [ headYawPosition, -0.4 ], 0.1)


                        headYawPosition += 0.6

                time.sleep(1)

            # turn body 90 degree to left
            motion.setAngles('HeadYaw', 0, 0.1)
            motion.setAngles('HeadPitch', 0, 0.1)
            motion.moveTo(0, 0, math.pi/2)
            time.sleep(2)


        faceProxy.unsubscribe("Test_Face")
        motion.rest()
        print "Test terminated successfully."




if __name__ == '__main__':

    demo = Demo('10.0.7.183', 9559)
    demo.run()
