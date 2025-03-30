import speech_recognition as sr  
import pyttsx3  
import webbrowser  
import datetime  
import os  
import requests  
import wikipedia  
import tkinter as tk
from tkinter import scrolledtext, Button, Label
import threading  

# Initialize text-to-speech
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)

def speak(text):
    """Convert text to speech and update chat."""
    engine.say(text)
    engine.runAndWait()
    update_chat(f"Friday: {text}")

def listen_in_background():
    """Continuously listen for 'Hello Friday' to activate the assistant."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        update_chat("Friday is waiting for 'Hello Friday'...")

        while True:
            try:
                audio = recognizer.listen(source)
                command = recognizer.recognize_google(audio).lower()

                if "hello friday" in command:
                    speak("I am listening. How can I assist you?")
                    listen_for_commands()

            except sr.UnknownValueError:
                continue  
            except sr.RequestError:
                update_chat("There seems to be a network issue. Please check your connection.")

def listen_for_commands():
    """Listen for user commands after activation."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        update_chat("Listening...")

        try:
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio).lower()
            update_chat(f"You: {command}")

            if "exit" in command or "bye" in command:
                speak("Goodbye. Have a great day.")
                root.quit()

            else:
                perform_task(command)

        except sr.UnknownValueError:
            update_chat("I didn't catch that. Could you please repeat?")
        except sr.RequestError:
            update_chat("There seems to be a network issue.")

def perform_task(command):
    """Perform a task based on the command."""
    if "open youtube" in command:
        speak("Opening YouTube.")
        webbrowser.open("https://youtube.com")

    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}.")

    elif "open notepad" in command:
        speak("Opening Notepad.")
        os.system("notepad")

    elif "search google for" in command:
        query = command.replace("search google for", "").strip()
        speak(f"Searching Google for {query}.")
        webbrowser.open(f"https://www.google.com/search?q={query}")

    elif "wikipedia" in command:
        query = command.replace("wikipedia", "").strip()
        speak(f"Searching Wikipedia for {query}.")
        try:
            result = wikipedia.summary(query, sentences=2)
            speak(result)
        except wikipedia.exceptions.DisambiguationError:
            speak("There are multiple results. Please be more specific.")
        except wikipedia.exceptions.PageError:
            speak("Sorry, I couldn't find any information on that.")

    elif "tell me a joke" in command:
        jokes = [
            "Why don't skeletons fight each other? Because they don't have the guts!",
            "Why was the math book sad? Because it had too many problems.",
            "What do you call fake spaghetti? An impasta!"
        ]
        speak(jokes[0])  

    elif "motivate me" in command or "give me a quote" in command:
        quotes = [
            "Success is not final, failure is not fatal: it is the courage to continue that counts.",
            "Believe you can, and you’re halfway there.",
            "The only way to do great work is to love what you do."
        ]
        speak(quotes[0])  

    elif "play music" in command:
        speak("Playing music from your collection.")
        music_dir = "C:\\Users\\YourUsername\\Music"  
        songs = os.listdir(music_dir)
        if songs:
            os.startfile(os.path.join(music_dir, songs[0]))  
        else:
            speak("No music files found.")

    elif "shutdown" in command:
        speak("Shutting down the computer.")
        os.system("shutdown /s /t 5")

    elif "restart" in command:
        speak("Restarting the computer.")
        os.system("shutdown /r /t 5")

    elif "take notes" in command:
        speak("What should I write down?")
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            audio = recognizer.listen(source)
            note = recognizer.recognize_google(audio)
            with open("notes.txt", "a") as file:
                file.write(note + "\n")
            speak("Note saved.")

    elif "read notes" in command:
        try:
            with open("notes.txt", "r") as file:
                notes = file.read()
            speak("Here are your notes: " + notes)
        except FileNotFoundError:
            speak("No notes found.")

    elif "play" in command and "on spotify" in command:
        song_name = command.replace("play", "").replace("on spotify", "").strip()
        speak(f"Playing {song_name} on Spotify.")
        webbrowser.open(f"https://open.spotify.com/search/{song_name.replace(' ', '%20')}")

    else:
        speak("I'm not sure how to respond to that.")

def update_chat(message):
    """Update chat window with a message."""
    chat_window.insert(tk.END, message + "\n")
    chat_window.yview(tk.END)

def start_listening():
    """Start listening manually when the button is clicked."""
    threading.Thread(target=listen_for_commands, daemon=True).start()

def clear_chat():
    """Clear chat window."""
    chat_window.delete("1.0", tk.END)

# GUI Setup
root = tk.Tk()
root.title("Friday - AI Voice Assistant")
root.geometry("500x650")
root.configure(bg="#1E1E1E")

# Header
header = Label(root, text="Friday - AI Voice Assistant", font=("Arial", 14, "bold"), bg="#1E1E1E", fg="#00FF00")
header.pack(pady=10)

# Chat window
chat_window = scrolledtext.ScrolledText(root, wrap=tk.WORD, bg="#2C2F33", fg="white", font=("Arial", 12))
chat_window.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# Buttons
button_frame = tk.Frame(root, bg="#1E1E1E")
button_frame.pack(pady=10)

listen_button = Button(button_frame, text="🎤 Listen", font=("Arial", 12), bg="#008CBA", fg="white", command=start_listening)
listen_button.pack(side=tk.LEFT, padx=5)

clear_button = Button(button_frame, text="🗑 Clear Chat", font=("Arial", 12), bg="#f39c12", fg="white", command=clear_chat)
clear_button.pack(side=tk.LEFT, padx=5)

exit_button = Button(button_frame, text="❌ Exit", font=("Arial", 12), bg="#e74c3c", fg="white", command=root.quit)
exit_button.pack(side=tk.LEFT, padx=5)

# Start background listening
threading.Thread(target=listen_in_background, daemon=True).start()

# Start GUI
root.mainloop()
