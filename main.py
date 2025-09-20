# ---------------------------------------------------------------------------------------------------------------------------------------------------
import speech_recognition as sr
from gtts import gTTS
import pygame
import time
import datetime
import os
import subprocess
import webbrowser
import musicLibrary

# ------------------ gTTS with pygame Speak Function ------------------
def speak(text):
    print("Jarvis:", text)
    tts = gTTS(text=text, lang='en')
    filename = "voice_output.mp3"
    tts.save(filename)

    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        time.sleep(0.3)

    pygame.mixer.quit()
    os.remove(filename)

# ------------------ Process Command ------------------
def processCommand(c):
    print("You said:", c)
    c = c.lower()

    if "google" in c:
        webbrowser.open("https://google.com")

    elif "youtube" in c:
        webbrowser.open("https://youtube.com")

    elif "chatgpt" in c:
        webbrowser.open("https://chat.openai.com")

    elif c.startswith("play"):
        words = c.split(" ", 1)
        if len(words) > 1:
            song = words[1].strip()
            if song in musicLibrary.music:
                link = musicLibrary.music[song]
                speak(f"Playing {song}")
                webbrowser.open(link)
            else:
                speak(f"Sorry, I couldn't find the song named {song}.")
        else:
            speak("Please say the name of the song after play.")

    elif "time" in c:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {now}")
    elif "date" in c:
        today = datetime.datetime.now().strftime("%A, %B %d, %Y")
        speak(f"Today is {today}")
    elif "open notepad" in c:
        subprocess.Popen("notepad.exe")



    else:
        speak("Sorry, I didn't understand that command.")

# ------------------ Main Loop ------------------
if __name__ == "__main__":
    speak("Initializing Jarvis")

    while True:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Adjusting for noise...")
            r.adjust_for_ambient_noise(source, duration=1)
            print("Listening...")

            try:
                audio = r.listen(source, timeout=5, phrase_time_limit=5)
                command = r.recognize_google(audio)
                print("You said:", command)

                if "jarvis" in command.lower():
                    speak("Yes?")
                    with sr.Microphone() as source:
                        print("Jarvis Active, Listening...")
                        r.adjust_for_ambient_noise(source, duration=1)
                        audio = r.listen(source, timeout=5, phrase_time_limit=5)
                        command = r.recognize_google(audio)
                        processCommand(command)

            except sr.WaitTimeoutError:
                print("Listening timed out, no speech detected.")
            except sr.UnknownValueError:
                print("Google could not understand the audio.")
            except sr.RequestError as e:
                print(f"Google API error: {e}")
