import pyttsx3
import speech_recognition as sr
import webbrowser
import os
import subprocess
import requests
import datetime
from ecapture import ecapture as ec
import shutil
import wikipedia

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

api_key = "cde14d10fca1f2ff48679114686901eb"  
base_url = "http://api.openweathermap.org/data/2.5/weather?"

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning Sir!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon Sir!")
    else:
        speak("Good Evening Sir!")  
    speak("I am your Assistant")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening...")
        r.pause_threshold = 0.7
        audio = r.listen(source)
    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print(e)    
        print("Unable to Recognize your voice.")  
        return "None"
    return query

def get_temperature(city_name):
    complete_url = f"{base_url}appid={api_key}&q={city_name}&units=metric"
    response = requests.get(complete_url)
    data = response.json()
    if data["cod"] != "404":
        main = data["main"]
        temperature = main["temp"]
        return temperature
    else:
        speak("City Not Found")
        return None

def news():
    newsApi = "8845439ccd4944cfbcd31545875cec9e"
    print("Please specify the country code for the news you want to hear.")
    print("For example, enter 'us' for the United States or 'in' for India.")
    country_code = input().lower()
    
    if country_code != "none":
        newsurl = f"https://newsapi.org/v2/top-headlines?country={country_code}&apiKey={newsApi}"
        try:
            response = requests.get(newsurl)
            news = response.json()
            
            if news["status"] == "ok":
                articles = news["articles"]
                for article in articles[:5]:  
                    speak(article["title"])
                    print(article["title"])
            else:
                print("Unable to fetch news. Please check the country code and try again.")
        except Exception as e:
            print(e)
            print("There was an error fetching the news. Please try again later.")
    else:
        print("No country code provided. Please try again.")

if __name__ == "__main__":
    wishMe()
    speak("Hello, how can I assist you today?")
    while True:
        query = takeCommand().lower()
        if query == 'none':
            continue
        if 'shanu' in query:
            print("Yes sir")
            speak("Yes sir")
        elif 'wikipedia' in query:
            speak("Searching Wikipedia...")
            query = query.replace('wikipedia', "")
            try:
                results = wikipedia.summary(query, sentences=3)
                speak("According to Wikipedia")
                speak(results)
                print(results)
            except wikipedia.exceptions.DisambiguationError as e:
                speak(f"There are multiple results for {query}. Please be more specific.")
            except wikipedia.exceptions.PageError:
                speak(f"I couldn't find any results for {query}.")
            except wikipedia.exceptions.WikipediaException as e:
                speak(f"An error occurred: {e}")
        elif 'hello' in query:
            speak("Hello! How are you?")
        elif 'your name' in query:
            speak("I am your assistant.")
        elif 'exit' in query or 'stop' in query:
            speak("Goodbye!")
            break
        elif 'open google' in query:
            speak("What should I search?")
            search_query = takeCommand().lower()
            if search_query != 'none':
                webbrowser.open(f"https://www.google.com/search?q={search_query}")
        elif 'open youtube' in query:
            speak("What should I search on YouTube?")
            search_query = takeCommand().lower()
            if search_query != 'none':
                webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")
        elif 'shutdown' in query:
            speak("Do you really want to shut down the computer?")
            confirmation = takeCommand().lower()
            if confirmation == "yes":
                os.system("shutdown /s /t 30")
            else:
                continue
        elif 'open anime' in query:
            speak("What should I search on anime?")
            search_query = takeCommand().lower()
            if search_query != 'none':
                webbrowser.open(f"https://hianime.to/search?keyword={search_query}")
        elif 'open excel' in query:
            speak('Opening Excel')
            subprocess.Popen(['start', 'excel.exe'], shell=True)
        elif 'open notepad' in query:
            speak('Opening Notepad')
            subprocess.Popen(['notepad.exe'], shell=True)
        elif 'open chrome' in query:
            speak('Opening Google Chrome')
            subprocess.Popen(['start', 'chrome.exe'], shell=True)
            speak("What should I search?")
            search_query = takeCommand().lower()
            if search_query != 'none':
                webbrowser.open(f"https://www.google.com/search?q={search_query}")
        elif 'temperature' in query:
            speak("Please tell me the city name.")
            city_name = takeCommand().lower()
            if city_name != 'none':
                temperature = get_temperature(city_name)
                if temperature is not None:
                    speak(f"The current temperature in {city_name} is {temperature} degrees Celsius.")
                    print(temperature)
        elif "camera" in query or "take a photo" in query:
            ec.capture(0, "Assistant Camera ", "img.jpg")
        elif "lock window" in query:
            speak("Locking the device")
            os.system("rundll32.exe user32.dll, LockWorkStation")
        elif "restart" in query:
            subprocess.call(["shutdown", "/r"])
        elif "news" in query:
            news()

        else:
            speak("I didn't understand that. Please try again.")
