import wikipedia
import requests
import pywhatkit as kit
from email.message import EmailMessage
import smtplib
from decouple import config

# NEWS_API_KEY = config("NEWS_API_KEY")
OPENWEATHER_APP_ID = config("OPENWEATHER_APP_ID")
# TMDB_API_KEY = config("TMDB_API_KEY")
EMAIL = config("EMAIL")
PASSWORD = config("PASSWORD")

def find_my_ip():
    ip_address=requests.get('https://api64.ipify.org?format=json').json()
    return ip_address['ip']

def search_on_wikipedia(query):
    results=wikipedia.summary(query,sentences=2)
    return results

def play_on_youtube(video):
    kit.playonyt(video)

def search_on_google(query):
    kit.search(query)

def send_whatsapp_message(number,message):
    kit.sendwhatmsg_instantly(f"+91{number}",message)

def send_email(receiver_address,subject,message):
    try:
        email=EmailMessage()
        email['To']=receiver_address
        email['Subject']=subject
        email['From']=EMAIL
        email.set_content(message)
        s=smtplib.SMTP("smtp.gmail.com",587)
        s.starttls()
        s.login(EMAIL,PASSWORD)
        s.send_message(email)
        s.close()
        return True
    except Exception as e:
        print(e)
        return False

def get_weather_report(city):
    res=requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_APP_ID}&units=metric").json()
    weather=res["weather"][0]["main"]
    temperature=res["main"]["temp"]
    feels_like=res["main"]["feels_like"]
    return weather,f"{temperature}℃",f"{feels_like}℃"
