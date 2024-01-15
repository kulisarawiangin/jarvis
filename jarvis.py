import openai
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_KEY = os.getenv('OPENAI_KEY')

openai.api_key = OPENAI_KEY

def SpeakText(command):
    tts = gTTS(text=command, lang='en')
    tts.save("output.mp3")
    playsound("output.mp3")

r = sr.Recognizer()

def record_text():
    with sr.Microphone() as source2:
        r.adjust_for_ambient_noise(source2, duration=0.2)
        print("I'm listening...")
        audio2 = r.listen(source2, timeout=5)

    try:
        MyText = r.recognize_google(audio2)
        print("You:", MyText)
        return MyText

    except sr.UnknownValueError as e:
        print("Could not understand audio; {0}".format(e))

    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

def send_to_chatGPT(messages, model="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = response.choices[0].message.content
    messages.append(response.choices[0].message)
    return message

messages = [{"role": "user", "content": "Please act like Jarvis from Iron man."}]

while True:
    text = record_text()

    if text:
        messages.append({"role": "user", "content": text})
        response = send_to_chatGPT(messages)
        SpeakText(response)
        print("JARVIS:", response)
