import sys
from naoqi import ALProxy

# example
def nao_speak(text, ip, port):

    tts = ALProxy("ALTextToSpeech", ip, port)
    tts.say(text)

# write function down below and test it in main()


def main():

    # parameter for naobot
    nao_ip = sys.argv[1]
    nao_port = 9559

    # example
    nao_speak("Test dat shit!", nao_ip, nao_port)

    # test....

# Command: python project.py "10.0.7.16"
if __name__ =='__main__':
    main()
