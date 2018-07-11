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

        # TODO: : TEST!!!!!
        # save proxies into a dict, no need to reinit?
        self.proxy = {}

    # simple example for motion
    def motion(self, state):
        '''
        TODO: TEST!!!
        check if proxy already exist
         - yes? skip!
         - no? -> create one and save in the dict
        '''
        if !self.proxy[motion]:
            try:
                self.proxy[motion] = ALProxy("ALMotion", self.ip, port)
            except Exception, e:
                print "Could not create proxy to ALRobotPosture"
                print "Error was: ", e

        if state == 'wakeUp':
            self.proxy[motion].wakeUp()
        elif state == 'rest':
            self.proxy[motion].rest()


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
    if len(sys.args) <= 1:
        print "USAGE: python project.py <robotIP>"
    else:
        nao_ip = sys.argv[1]


    nao = AssistentAgent(nao_ip)

    # before u ran your code, NaoBot needs to wake up!
    nao.motion('wakeUp')

    # enter your code here down below

    #nao.speak("mama")
    #nao.posture("StandInit")

    # after u ran your code, let Naobot rest!
    nao.motion('rest')
