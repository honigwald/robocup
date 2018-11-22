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

    # make nao say a given text
    def say(self, text):

        tts = self.create_proxy("ALTextToSpeech")
        tts.say(text)

    # animated hello with given name
    def animatedHello(self, name):

        atts = self.create_proxy("ALAnimatedSpeech")

        animation = '^start(animations/Stand/Gestures/Hey_1)'
        wait = '^wait(animations/Stand/Gestures/Hey_1)'
        string = 'Hello,' + animation + name + wait
        atts.say(string)

    # init ALProxy for given module
    def create_proxy(self, name):

        try:
            proxy = ALProxy(name, self.ip, self.port)
        except Exception, e:
            print "Error when creating " + name + " proxy:"
            print str(e)

        return proxy

    # start speech recognition within a given time in sec, return reconized words
    def speech_recognize(self, time):
        with sr.Microphone() as source:
            self.r.adjust_for_ambient_noise(source)
            print 'Mic activated. Start listening...'
            audio = self.r.listen(source, phrase_time_limit=time)
            try:
                print 'Reconized words: ' + self.r.recognize_google(audio)
                return self.r.recognize_google(audio)
            except LookupError, e:
                print e
                return 'there was an error!'
            except sr.UnknownValueError, e:
                print e
                print 'Reconized nothing within ' + str(time) + ' second!'
                return ''

    # reduce memory array from nao, return required information
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

    # let nao turn into a given direction (alpha, beta)
    def turnBody(self, alpha, beta):

        motion = self.create_proxy('ALMotion')
        headYawP = motion.getAngles(["HeadYaw"], False)[0]
        value = 0

        # turn head into init position (0) to avoid collide, if head yaw is turned
        if headYawP != 0:
            motion.setAngles('HeadYaw', 0, 0.1)

        # turn whole body into alpha position only if its necessary
        if -2 < alpha < 2:
            if alpha - headYawP > 0.1 or alpha - headYawP < -0.1:
                motion.moveTo(0, 0, headYawP + alpha)
                value = headYawP + alpha

        # turn head pitch to direction (beta) of target
        if -0.6 < beta - 0.3 < 0.5:
            motion.setAngles('HeadPitch', beta - 0.3, 0.1)
        elif -0.6 < beta < 0.5:
            motion.setAngles('HeadPitch', beta, 0.1)

        time.sleep(2)

        return value


    # let nao learn or relearn new faces
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
                    break

    # decision tree for greeting. Greet, learn or relearn person based on score and already greeted
    def greeting(self, face):

        if face['name'] != '':

            # less than 20%, person is unknown -> learn
            if face['score'] <= 0.2:
                self.learnNewFace()

            # less than 60%, person is known but score to low -> relearn
            elif face['score'] <= 0.6:
                self.learnNewFace(face['name'])

            # more than 60% probability, person is well known
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

    # compare all faces and return the person (index) with the lowest distance
    def compareFaces(self, faces):

        # remove all faces with more than 0.7 score
        if len(faces) > 1:
            for face in faces:
                if face['name'] in self.checked and face['score'] > 0.6:
                    # remove face from faces
                    faces.remove(face)

        alphas = [face['alpha'] for face in faces]
        betas = [face['beta'] for face in faces]
        distances = map(lambda a, b: math.sqrt(a**2 + b**2), alphas, betas)
        minDistance = distances.index(min(distances))

        # HOW IS THE PRIORITY FOR FACES? DISTANCE OR SCORE?
        # scores = [face['score'] for face in faces]
        # minScore = scores.index(min(scores))

        return minDistance


    def run(self):

        # Init
        faceProxy = self.create_proxy("ALFaceDetection")
        memoryProxy = self.create_proxy("ALMemory")
        motion = self.create_proxy("ALMotion")

        faceProxy.subscribe("Test_Face", 500, 0.0)
        motion.wakeUp()

        faces = []

        # Main loop
        for i in range(4):

            # For each loop set head into position
            # motion.setAngles('HeadPitch', -0.4, 0.1)
            headYawPosition = -0.6
            sumAngle = 0

            # side loop: for each iteration check for face recognition
            for j in range(6,24):

                # turn head, avoid deadlock
                if j % 6 == 0:
                    motion.setAngles(['HeadYaw', 'HeadPitch'], [ headYawPosition, -0.4 ], 0.1)
                    headYawPosition += 0.6

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
                        sumAngle += self.turnBody(face['alpha'], face['beta'])

                else:
                    print 'No one detected: ' + val


            # end of side loop, turn body 90 degree to left
            motion.setAngles('HeadYaw', 0, 0.1)
            motion.setAngles('HeadPitch', 0, 0.1)
            motion.moveTo(0, 0, math.pi/2 - sumAngle)
            time.sleep(2)

        # end of main loop
        faceProxy.unsubscribe("Test_Face")
        motion.rest()
        print "Test terminated successfully."




if __name__ == '__main__':

    demo = Demo('10.0.7.183', 9559)
    demo.run()
