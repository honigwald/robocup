from naoqi import ALProxy

Class FaceRecognition():

    def __init__(self, ip, port):
        self.ip = ip
        self.port =  port

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

    def learn(self):

    def reset(self):

    def getDatabase(self):
