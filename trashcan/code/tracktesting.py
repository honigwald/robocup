import sys
import time
from naoqi import ALProxy
from hello import *
import json

ip = sys.argv[1]
port = 9559


try:
    tts = ALProxy("ALTextToSpeech", ip, port)
    tts.say('Hello')

except Exception, e:
    print "Could not create proxy to ALTextToSpeech!"
    print "Error was: ", e


try:
    motion = ALProxy("ALMotion", ip, port)
except Exception, e:
    print "Could not create proxy to ALMotion!"
    print "Error was: ", e

try:
    tracker = ALProxy("ALTracker", ip, port)
except Exception, e:
    print "Could not create proxy to ALTracker!"
    print "Error was: ", e

# First, wake up.
motion.wakeUp()

# Add target to track.
targetName = "Face"
faceWidth = 0.1
tracker.setMode('Move')
tracker.registerTarget(targetName, faceWidth)

# Then, start tracker.
tracker.track(targetName)

print "ALTracker successfully started, now show your face to robot!"
print "Use Ctrl+c to stop this script."

try:
    while True:
        # TODO TESTEN!!!!
        if tracker.isNewTargetDetected():
            print "new target detected"
            position = tracker.getRelativePosition()
            print position
            p = tracker.setRelativePosition(position)

#            break
        else:
            print "no target"
        time.sleep(3)

except KeyboardInterrupt:
    print
    print "Interrupted by user"
    print "Stopping..."

tracker.stopTracker()
tracker.unregisterAllTargets()
motion.rest()
