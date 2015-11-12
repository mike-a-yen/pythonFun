import speech_recognition as sr
import pyaudio
r = sr.Recognizer('en-US')
r.energy_threshold = 2000
mic = sr.Microphone()
with mic as source:
    audio = r.listen(source)

try:
    print 'You said ', r.recognize(audio)
except LookUpError:
    print 'I didnt get that'
