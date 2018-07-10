import sys
from naoqi import ALProxy

'''
USAGE: type in terminal: python project.py "10.0.7.1X"
    X is the number of the robot
'''


# different motion listed here
def nao_motion(state, ip, port):

    try:
        motion = ALProxy("ALMotion", ip, port)
    except Exception, e:
        print "Could not create proxy to ALRobotPosture"
        print "Error was: ", e

    if state == 'wakeUp':
        motion.wakeUp()
    elif state == 'rest':
        motion.rest()


# simple example for speaking
def nao_speak(text, ip, port):

    try:
        tts = ALProxy("ALTextToSpeech", ip, port)
    except Exception, e:
        print "Could not create proxy to ALTextToSpeech"
        print "Error was: ", e

    tts.say(text)

# simple example for build-in posture
def nao_posture(posture, ip, port):

    try:
        postureProxy = ALProxy("ALRobotPosture", ip, port)
    except Exception, e:
        print "Could not create proxy to ALRobotPosture"
        print "Error was: ", e

    postureProxy.goToPosture(posture, 1.0)



def main():

    # parameter for naobot
    nao_ip = sys.argv[1]
    nao_port = 9559

    # before u ran your code, NaoBot needs to wake up!
    nao_motion('wakeUp', nao_ip, nao_port)

    # enter your code here down below

    #nao_speak("mama", nao_ip, nao_port)
    #nao_posture("StandInit", nao_ip, nao_port)
    #nao_motion(nao_ip, nao_port)

    # after u ran your code, let Naobot rest!
    nao_motion('rest', nao_ip, nao_port)

if __name__ =='__main__':
    main()
