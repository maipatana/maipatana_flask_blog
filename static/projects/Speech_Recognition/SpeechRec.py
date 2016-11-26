import serial, time
import speech_recognition as sr

port = "COM6"  # Change to coreect COM Port
baud = 9600

# Record Audio
r = sr.Recognizer()
m = sr.Microphone()
#set threhold level
with m as source: r.adjust_for_ambient_noise(source)
print("Set minimum energy threshold to {}".format(r.energy_threshold))

# Speech recognition using Google Speech Recognition
def checkspeech(r):
    with sr.Microphone() as source:
        audio = r.listen(source)
    try:
    # for testing purposes, we're just using the default API key
    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    # instead of `r.recognize_google(audio)`
        print("You said: " + r.recognize_google(audio))
        return (r.recognize_google(audio))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return ("WW")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return ("WW")

def writetolcd(text):
    arduino = serial.Serial()
    arduino.port = port
    arduino.baud = baud
    arduino.setDTR(False)
    arduino.open()
    time.sleep(1)
    arduino.write(text.encode('ascii'))
    time.sleep(.1)
    arduino.close()

def main():
    while run == True:
        with m as source: r.adjust_for_ambient_noise(source)
        print("Set minimum energy threshold to {}".format(r.energy_threshold))
        print("How can I help you Patana?")

        speech = str(checkspeech(r))

        if "light on" in speech:
            print ("Light On")
            writetolcd("on")
            
        elif "light off" in speech:
            print ("Light Off")
            writetolcd("off")
run = True
main()
