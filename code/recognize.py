def flearn(self, name):
    try:
        faceProxy = ALProxy("ALFaceDetection", self.ip, self.port)
    except Exception, e:
        print "Error when creating face detection proxy:"
        print str(e)
    
    #print "Actual DB: %s" % (faceProxy.getLearnedFacesList()) 
    if (faceProxy.learnFace(name)):
        print "Learning is complete"
    else:
        print "Something went wrong"

def fcleardb(self):
    try:
        faceProxy = ALProxy("ALFaceDetection", self.ip, self.port)
    except Exception, e:
        print "Error when creating face detection proxy:"
        print str(e) 
    
    #print "Actual DB: %s" % (faceProxy.getLearnedFacesList()) 
    if (faceProxy.clearDatabase()):
        print "DB cleared"
    else:
        print "Something went wrong"

def fidentify(self):
    try:
        faceProxy = ALProxy("ALFaceDetection", self.ip, self.port)
    except Exception, e:
        print "Error when creating face detection proxy:"
        print str(e) 

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
