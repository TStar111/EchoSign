import pyttsx3

def speak_letters(letters):
    engine = pyttsx3.init()
    engine.say(letters)
    engine.runAndWait()

# Example usage:
input_letters = input("Enter letters to speak out loud: ")
speak_letters(input_letters)
