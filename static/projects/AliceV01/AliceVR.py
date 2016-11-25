import datetime
import webbrowser
import os
import serial, time
import speech_recognition as sr
from pyowm import OWM
from google import search
from gtts import gTTS


port = "COM6"  # Change to correct COM Port
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
    

def writetolcd(text):  # This is to send message to display on Arduino's LED Screen
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
        print("How can I help you?")

        speech = str(checkspeech(r))
        if speech == "Alice" or "Alice" in speech and "wake up" or "listen" in speech:
            
            os.system("start Aliceisup.wav")
            time.sleep(.5)
            print("How can I help you Patana?")
            speech = str(checkspeech(r))
            
            if speech == "what is your name":
                print ("My name is Alice")
                os.system("start MynameisAlice.wav")
                time.sleep(1.5)
                #writetolcd("   I am Alice")  # If you are not using Arduino, you can comment this all out
                #writetolcd("What's yours?")
                os.system("start Whatisyourname.wav")
                print("What's yours?")
                speech = str(checkspeech(r))
                Greeting = "Hi "+speech
                #writetolcd(Greeting)
                tts = gTTS(text= Greeting, lang='en')
                tts.save("Greeting.wav")
                os.system("mpg321 Greeting.wav")
                os.system("start Greeting.wav")
                
            elif speech == "hello Alice":
                print("Hello")
                time.sleep(2)
                os.system("start HowcanIhelpyou.wav")   
                
            elif speech == "what time is it":
                print ("Let me Check")
                now = datetime.datetime.now()
                timenow= (str(now.hour)+"o clock "+str(now.minute)+"minute")
                timetoar = "Now is "+str(now.hour)+":"+str(now.minute)
                #writetolcd(timetoar)   
                tts = gTTS(text= timenow, lang='en')
                tts.save("TimeNow.wav")
                os.system("mpg321 TimeNow.wav")
                os.system("start TimeNow.wav")

            elif speech =="repeat after me":
                print("ok")
                speech = str(checkspeech(r))
                #writetolcd(speech)
                tts = gTTS(text= speech, lang='en')
                tts.save("speech.wav")
                os.system("mpg321 speech.wav")
                os.system("start speech.wav")
                
            elif "weather" and "Bangkok" in speech:
                print ("Weather in Bangkok")
                API_key = 'xxxxxxxxxxxxxxxxxxx'  # Your Open Weather Map API Key
                owm = OWM(API_key)
                observation = owm.weather_at_place('Bangkok, THA')
                wc = observation.get_weather()
                temp = wc.get_temperature()
                humi = wc.get_humidity()
                wind = wc.get_wind()
                WtoAr = "BKK T="+str(int(float(temp['temp'])-273.15))+"C H="+str(humi)+"%"
                #writetolcd(WtoAr)
                weathercon = "The Current Temperature in Bangkok is "+str(int(float(temp['temp'])-273.15))+" degree celsius"+" with "+str(humi)+"percent humidity"
                wind = wc.get_wind()
                try:  # Get Wind Direction
                    winddeg = wind['deg']
                    if int(winddeg) in range(0,22):
                        winddi = 'North'
                    elif int(winddeg) in range(22,67):
                        winddi = 'North East'
                    elif int(winddeg) in range(67,112):
                        winddi = 'East'
                    elif int(winddeg) in range(112,157):
                        winddi = 'South East'
                    elif int(winddeg) in range(157,202):
                        winddi = 'South'
                    elif int(winddeg) in range(202,247):
                        winddi = 'South West'
                    elif int(winddeg) in range(247,292):
                        winddi = 'West'
                    elif int(winddeg)in range(292,337):
                        winddi = 'North West'
                    elif int(winddeg)in range(337,360):
                        winddi = 'North'
                    else:
                        pass
                except:
                    winddi = "Not Known"
                    print (wind)
                windcon = "The wind speed is "+str(wind['speed'])+" metre per second coming from"+str(winddi)
                #print (wind)
                #print (wind['deg'])
                #print (winddi)
                tts = gTTS(text= weathercon, lang='en')
                tts.save("WeatherCon.wav")
                tts = gTTS(text= windcon, lang='en')
                tts.save("WindCon.wav")
                os.system("mpg321 WeatherCon.wav")
                os.system("mpg321 WindCon.wav")
                os.system("start WeatherCon.wav")
                time.sleep(8)
                os.system("start WindCon.wav")

            elif "weather" and "Cardiff" in speech:
                print ("Weather in Cardiff")
                API_key = 'xxxxxxxxxxxxxxxxxxx'  # Your Open Weather Map API Key
                owm = OWM(API_key)
                observation = owm.weather_at_place('Cardiff, UK')
                wc = observation.get_weather()
                temp = wc.get_temperature()
                humi = wc.get_humidity()
                wind = wc.get_wind()
                WtoAr = "CWL T="+str(int(float(temp['temp'])-273.15))+"C H="+str(humi)+"%"
                #writetolcd(WtoAr)
                weathercon = "The Current Temperature in Cardiff is "+str(int(float(temp['temp'])-273.15))+" degree celsius"+" with "+str(humi)+"percent humidity"
                wind = wc.get_wind()
                try:
                    winddeg = wind['deg']
                    if int(winddeg) in range(0,22):
                        winddi = 'North'
                    elif int(winddeg) in range(22,67):
                        winddi = 'North East'
                    elif int(winddeg) in range(67,112):
                        winddi = 'East'
                    elif int(winddeg) in range(112,157):
                        winddi = 'South East'
                    elif int(winddeg) in range(157,202):
                        winddi = 'South'
                    elif int(winddeg) in range(202,247):
                        winddi = 'South West'
                    elif int(winddeg) in range(247,292):
                        winddi = 'West'
                    elif int(winddeg)in range(292,337):
                        winddi = 'North West'
                    elif int(winddeg)in range(337,360):
                        winddi = 'North'
                    else:
                        pass
                except:
                    winddi = "Not Known"
                    print (wind)
                windcon = "The wind speed is "+str(wind['speed'])+" metre per second coming from"+str(winddi)
                #print (wind)
                #print (wind['deg'])
                #print (winddi)
                tts = gTTS(text= weathercon, lang='en')
                tts.save("WeatherCon.wav")
                tts = gTTS(text= windcon, lang='en')
                tts.save("WindCon.wav")
                os.system("mpg321 WeatherCon.wav")
                os.system("mpg321 WindCon.wav")
                os.system("start WeatherCon.wav")
                time.sleep(8)
                os.system("start WindCon.wav")

            elif speech =="goodbye Alice":
                os.system("start goodbye.wav")
                run = "End Program"
                print (run)

            elif "light" in speech and "on" in speech:
                print ("Light On")
                writetolcd("on")  # Send on to Arduino where Arduino recognise as a signal to turn on the light
                
            elif "light" in speech and "off" in speech or "of" in speech:
                print ("Light Off")
                writetolcd("off")  # Send on to Arduino where Arduino recognise as a signal to turn off the light

            elif "search" in speech:
                new =2
                searchwW = speech.strip("search")
                url = "https://www.google.co.uk/search?q="+str(searchwW)
                print (searchwW)
                pth = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"  # Your chrome.exe destination. Change if different.
                webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(pth))
                chrome = webbrowser.get('chrome')
                chrome.open_new_tab(url)

            elif "open website" in speech or "open" and ".com" in speech:
                # Windows
                chrome_path = 'C:\Program Files (x86)\Google\Chrome\Applicationchrome.exe %s'  # Your chrome.exe destination. Change if different.
                new =2
                if "open website" in speech:
                    openW = speech.strip("open website")
                else:
                    openW = speech.strip("open ")
                print(openW)
                url = str(openW)
                pth = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"  # Your chrome.exe destination. Change if different.
                webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(pth))
                chrome = webbrowser.get('chrome')
                chrome.open_new_tab(url)

            else:
                print("I can't understand that yet")
                os.system("start Dontun.wav")
                #writetolcd("Don't understand")
                
        elif speech == "what time is it":
                print ("Let me Check")
                now = datetime.datetime.now()
                timenow= (str(now.hour)+"o clock "+str(now.minute)+"minute")
                timetoar = "Now is "+str(now.hour)+":"+str(now.minute)
                #writetolcd(timetoar)   
                tts = gTTS(text= timenow, lang='en')
                tts.save("TimeNow.wav")
                os.system("mpg321 TimeNow.wav")
                os.system("start TimeNow.wav")
                
        elif "thank you" in speech:
            print("Your Welcome")
            os.system("start yourwelcome.wav")
                    
        elif "light" in speech and "on" in speech:
            print ("Light On")
            writetolcd("on")
                
        elif "light" in speech and "off" in speech or "of" in speech:
            print ("Light Off")
            writetolcd("off")
            
        else:
            print ("Alice is still here. You can talk to me anytime")
            pass
        
        time.sleep(.5) #wait 2 sec to start again
        

main()

