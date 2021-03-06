# This test demonstrates how to use the ALFaceDetection module.
# Note that you might not have this module depending on your distribution
#
# - We first instantiate a proxy to the ALFaceDetection module
#     Note that this module should be loaded on the robot's NAOqi.
#     The module output its results in ALMemory in a variable
#     called "FaceDetected"
# - We then read this ALMemory value and check whether we get
#   interesting things.
import time
from naoqi import ALProxy

# Replace this with your robot's IP address
IP = "10.0.7.16"
PORT = 9559

# Create a proxy to ALFaceDetection
try:
  faceProxy = ALProxy("ALFaceDetection", IP, PORT)
except Exception, e:
  print "Error when creating face detection proxy:"
  print str(e)
  exit(1)

# Subscribe to the ALFaceDetection proxy
# This means that the module will write in ALMemory with
# the given period below
period = 500
faceProxy.subscribe("Test_Face", period, 0.0 )

# ALMemory variable where the ALFaceDetection module
# outputs its results.
memValue = "FaceDetected"

# Create a proxy to ALMemory
try:
  memoryProxy = ALProxy("ALMemory", IP, PORT)
except Exception, e:
  print "Error when creating memory proxy:"
  print str(e)
  exit(1)

### testing the api
learnedFaces = faceProxy.getLearnedFacesList()
for face in learnedFaces:
    print face

# A simple loop that reads the memValue and checks whether faces are detected.
for i in range(0, 20):
    time.sleep(0.5)
    val = memoryProxy.getData(memValue, 0)
    print ""
    print "\*****"
    print ""

    # Check whether we got a valid output: a list with two fields.
    print len(val)
    if(val and isinstance(val, list) and len(val) == 5):
        # We detected faces !
        # For each face, we can read its shape info and ID.
        # First Field = TimeStamp.
        timeStamp = val[0]
        # Second Field = array of face_Info's.
        faceInfoArray = val[1]
        
        ### THIS IS IMPORTANT
        ### DETERMINING THE NAME OF RECOGNIZED PERSON
        print "Name of recognized Person: %s" % val[1][0][1][2]
        
        try:
        # Browse the faceInfoArray to get info on each detected face.
            for faceInfo in faceInfoArray:
                # First Field = Shape info.
                faceShapeInfo = faceInfo[0]
                # Second Field = Extra info (empty for now).
                faceExtraInfo = faceInfo[1]
                print "  faceID: %f" % (faceExtraInfo[0])
        except Exception, e:
            print "faces detected, but it seems getData is invalid. ALValue ="
            #print val
            print "Error msg %s" % (str(e))
        else:
            print "Error with getData. ALValue = %s" % (str(val))
            # Unsubscribe the module.

faceProxy.unsubscribe("Test_Face")
print "Test terminated successfully."
