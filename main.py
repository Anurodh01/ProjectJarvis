import pyttsx3
from decouple import config
from datetime import datetime
import speech_recognition as sr
from random import choice
from utils import opening_text
from functions.os_ops import open_calculator,open_camera,open_cmd,open_git,open_notepad
from functions.online_ops import get_weather_report,send_email,search_on_wikipedia,play_on_youtube,search_on_google,send_whatsapp_message,find_my_ip
import requests

USERNAME=config('USER')
BOTNAME=config('BOTNAME')

engine=pyttsx3.init('sapi5')

engine.setProperty('rate',190)

engine.setProperty('volume',1.0)

# setting voice
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def greet_user():
    hour=datetime.now().hour
    if (hour >= 6) and (hour < 12):
        speak(f"Good Morning {USERNAME}")
    elif (hour >= 12) and (hour < 16):
        speak(f"Good afternoon {USERNAME}")
    elif (hour >= 16) and (hour < 21):
        speak(f"Good Evening {USERNAME}")
    speak(f"I am {BOTNAME}. How may I assist you?")

""" taking input from user"""

def take_user_input():
    r=sr.Recognizer()
    with sr.Microphone()  as source:
        print("Listening....")
        r.pause_threshold=1
        audio=r.listen(source)

    try:
        print("Recognizing....")
        query=r.recognize_google(audio,language='en-in')
        if not 'exit' in query or 'stop' in query or 'thank' in query:
            speak(choice(opening_text))
        else:
            hour=datetime.now().hour
            if hour>=21 and hour<6:
                speak('Good night sir, take care!')
            else:
                speak('have a good day sir')
            exit()
    except Exception:
        speak('Sorry, I could not understand. Could you please say that again?')
        query='None'
    return query


if __name__ == '__main__':
    greet_user()
    while True:
        query = take_user_input().lower()

        if 'notepad' in query:
            open_notepad()
            speak('What is the message sir?')
            text=take_user_input().lower()
            with open('anurodh.txt',mode='a') as file:
                file.write('Recognized text:')
                file.write("\n")
                file.write(text)
            speak("I have complted the task sir.")


        elif 'open command prompt' in query or 'open cmd' in query:
            open_cmd()

        elif 'open camera' in query:
            open_camera()

        elif 'open calculator' in query:
            open_calculator()

        elif 'ip address' in query:
            ip_address=find_my_ip()
            speak(f'Your Ip Address is {ip_address}.\n For your convenience, I am printing it on the screen sir.')
            print(f'Your Ip address is {ip_address}')

        elif 'youtube' in query:
            speak('what do you want to play on youtube, sir')
            video=take_user_input().lower()
            play_on_youtube(video)

        elif 'search on google' in query:
            speak('what do you want to search in google,sir?')
            query=take_user_input().lower()
            search_on_google(query)

        elif 'send whatsapp message' in query:
            speak("On what number you want to send the whatsapp message sir, please enter the number on console?")
            number=input('Enter the number')
            speak('what is your message sir?')
            message=take_user_input().lower()
            send_whatsapp_message(number,message)
            speak('I have sent the message sir')
        
        elif 'send email' in query:
            speak('on what email address you want to send an email sir, please enter it in console?')
            receiver_address=input('Enter the receriver_address: ')
            speak('what should be the subject sir')
            subject=take_user_input().capitalize()
            speak('what is the message sir?')
            message=take_user_input().lower()
            if send_email(receiver_address,subject,message):
                speak('I have sent the email sir.')
            else:
                speak('Something went wrong while I was sending the mail. Please check the error logs sir.')
        
        elif 'wikipedia' in query:
            speak('What you want to search on wikipedia sir?')
            search_query=take_user_input().lower()
            results=search_on_wikipedia(search_query)
            speak(f'According to wikipedia, {results}')
            speak("For your convenience, i am printing it on your screen sir")
            print(results)
        
        elif 'weather' in query:
            ip_address=find_my_ip()
            city = requests.get(f"https://ipapi.co/{ip_address}/city/").text
            speak(f"Getting the weather report for  your city {city}")
            weather,temperature,feels_like=get_weather_report(city)
            speak(f"The Current temperature is {temperature} but it feels like {feels_like}")
            speak(f"Also the weather report talks about {weather}")
            speak("For your convenience, I am printing it on the screen sir.")
            print(f"Description: {weather}\nTemperature: {temperature}\nFeels like: {feels_like}")

