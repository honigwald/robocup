import snowboydecoder
import sys
import signal

# Demo code for listening two hotwords at the same time
def hotWord(models):

	sensitivity = [0.5]*len(models)
	detector = snowboydecoder.HotwordDetector(models, sensitivity=sensitivity)
	print('Listening... Press Ctrl+C to exit')

	# main loop
	# make sure you have the same numbers of callbacks and models
	word = detector.start(detected_callback=snowboydecoder.play_audio_file,
					sleep_time=0.03)
	return(word)

words = ['jarvis.pmdl, say.pmdl']
word = hotWord(words)
if word == '1':
	print "Yes"
elif word == '2':
	print "No"
