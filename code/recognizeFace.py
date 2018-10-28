import time
from naoqi import ALProxy

# Replace this with your robot's IP address
IP = "10.0.7.103"
PORT = 9559

# Create a proxy to ALFaceDetection
try:
  faceProxy = ALProxy("ALFaceDetection", IP, PORT)
except Exception, e:
  print "Error when creating face detection proxy:"
  print str(e)
  exit(1)

print "Actual DB: %s" % (faceProxy.getLearnedFacesList())

if (faceProxy.clearDatabase()):
    print "DB cleared"
else:
    print "Something went wrong"

print "Actual DB: %s" % (faceProxy.getLearnedFacesList())
