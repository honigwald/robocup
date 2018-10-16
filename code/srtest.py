import speech_recognition as sr
r = sr.Recognizer()

def recognize(time):

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, phrase_time_limit=time)
        try:
            return r.recognize_google(audio)
        except LookupError, e:
            print e
            return ''
        except sr.UnknownValueError, e:
            print e


while True:

    print "I listen hotword... sir"
    try:
        word = recognize(1)
        print "You said " + word
    except:
        print 'WTF ... NONETYPE'
    if word == "Alexa":
        print "I listen for command... sir"
        try:
            word2 = recognize(2).lower()
            print "You said " + word2
            if word2 == 'hello':
                print 'hello'
            elif word2 == "stop":
                break
        except Exception as e:
            print 'WTF ... NONETYPE'
