import snowboydecoder
import sys
import signal

# Demo code for listening two hotwords at the same time

word = None

def hotWord(models):

	sensitivity = [0.5]*len(models)
	detector = snowboydecoder.HotwordDetector(models, sensitivity=sensitivity)
	print('Listening... Press Ctrl+C to exit')

	# main loop
	# make sure you have the same numbers of callbacks and models
	callbacks = [lambda: haha(detector)]
	detector.start(detected_callback=callbacks, sleep_time=0.5)

def haha(detector):

    detector.terminate()
	sensitivity = [0.5]*len(['say.pmdl'])
	detector2 = snowboydecoder.HotwordDetector(['say.pmdl'], sensitivity=sensitivity)
	callbacks2 = [lambda: hoho(detector2)]
	detector2.start(detected_callback=callbacks2, interrupt_check=interrupt_callback, sleep_time=0.5)
	print 'before terminate'
	detector2.terminate()
	global interrupted
	interrupted = False
	print 'after terminate'


def hoho(detector2):
    detector2.terminate()
	print 'hoho'
    hotWord('jarvis.pmdl')


words = ['jarvis.pmdl']
word = hotWord(words)

print word
if word == '1':
	print "Yes"
elif word == '2':
	print "No"
