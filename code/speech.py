import speech_recognition as sr
import string
import sys
import threading
import time
import pyttsx3

KEYWORD = "alexa"
audio = None
r = sr.Recognizer()
engine = pyttsx3.init();
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[32].id)

def waitingForVoiceinput(result, desc):
    with sr.Microphone() as source:
        print("[t_waiting] %s" % desc)
        global audio
        audio = None
        audio = r.listen(source)

def feedback(string):
    engine.say(string)
    engine.runAndWait()

while True:
### PROCESSING KEYWORD
    t = threading.Thread(target=waitingForVoiceinput, args=(audio, "keyword"))
    t.start()
    t.join(5)
    if audio is not None:
        string = r.recognize_google(audio, language="de_DE")
        string = string.lower()
        print 'alt1: ' + string
        idx = string.find(KEYWORD)

        words = string.split(' ')
        print 'alt2: ' , words

        if idx != -1:
            # hier ist spass
            feedback("yes sire")

            # hier wieder ernst
            string.lower().find(KEYWORD, idx, len(KEYWORD))
            if string[idx:].split()[0] == KEYWORD:
### PROCESSING COMMAND
                t = threading.Thread(target=waitingForVoiceinput, args=(audio, "command"))
                t.start()
                t.join(10)
                if audio is not None:
                    string = r.recognize_google(audio, language="de_DE")
                    string = string.lower()
                    print string
                    if string == "wake up":
                        feedback("okay waking up")
                    elif string == "go to sleep":
                        feedback("okay going to sleep")
                    elif string == "say something":
                        feedback("this is a random string")
                    elif string == "start face recognition":
                        feedback("start with scanning")
                    elif string == "stop processing":
                        # hier ist spass
                        feedback("okay goodbye")
                        break
                    audio = None
### NO INPUT
    else:
        print "kein input"
