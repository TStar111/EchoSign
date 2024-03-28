# import pyttsx3

# def speak_letters(letters):
#     engine = pyttsx3.init()
#     engine.say(letters)
#     engine.runAndWait()

# # Example usage:
# input_letters = input("Enter letters to speak out loud: ")
# speak_letters(input_letters)

# from gtts import gTTS
# import os

# text = "Hello, how are you?"
# tts = gTTS(text)
# tts.save("output.mp3")

from win32com.client import Dispatch

speak = Dispatch("SAPI.SpVoice").Speak

speak("l")