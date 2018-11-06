import time
from naoqi import ALProxy

# Replace this with your robot's IP address
IP = "10.0.7.183"
PORT = 9559

# Create a proxy to ALFaceDetection
try:
    faceProxy = ALProxy("ALFaceDetection", IP, PORT)


    ### get the name
    newName = "simon"

    print "Actual DB: %s" % (faceProxy.getLearnedFacesList())

    ### start learning
    print "Start learning"
    o=faceProxy.learnFace(newName)
    print o
    print "Learning is complete"

    print "Actual DB: %s" % (faceProxy.getLearnedFacesList())
except Exception, e:
  print "Error when creating face detection proxy:"
  print str(e)
  exit(1)
