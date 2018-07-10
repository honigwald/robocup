'''
USAGE: type in terminal: python project.py "10.0.7.1X"
    X is the number of the robot
'''


import sys
from naoqi import ALProxy


class AssistentAgent:

    port = 9559

    def __init__(self, ip):
        self.ip = ip


    # simple example for motion
    def motion(self, state):

        try:
            motion = ALProxy("ALMotion", self.ip, self.port)
        except Exception, e:
            print "Could not create proxy to ALRobotPosture"
            print "Error was: ", e

        if state == 'wakeUp':
            motion.wakeUp()
        elif state == 'rest':
            motion.rest()


    # simple example for speaking
    def speak(self, text):

        try:
            tts = ALProxy("ALTextToSpeech", self.ip, self.port)
        except Exception, e:
            print "Could not create proxy to ALTextToSpeech"
            print "Error was: ", e

        tts.say(text)


    # simple example for build-in posture
    def posture(self, posture):

        try:
            postureProxy = ALProxy("ALRobotPosture", self.ip, self.port)
        except Exception, e:
            print "Could not create proxy to ALRobotPosture"
            print "Error was: ", e

        postureProxy.goToPosture(posture, 1.0)


if __name__ =='__main__':
    # parameter for naobot
    try:
        nao_ip = sys.argv[1]
    except Exception, e:
        print "Invalid IP address! Usage: python project.py <IP address>"
        print "Error was: ", e

    nao = AssistentAgent(nao_ip)

    # before u ran your code, NaoBot needs to wake up!
    nao.motion('wakeUp')

    # enter your code here down below

    #nao.speak("mama")
    #nao.posture("StandInit")

    # after u ran your code, let Naobot rest!
    nao.motion('rest', nao_ip, nao_port)
