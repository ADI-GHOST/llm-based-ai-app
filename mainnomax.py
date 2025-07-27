import os
import pyttsx3
import speech_recognition as sr
import pyaudio
import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import subprocess
from threading import Thread
import time

# Voice functions
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    while True:  
        try:
            with sr.Microphone() as source:
                display_message("Listening...")
                speak("I am listening. Please speak your command.")
                audio = recognizer.listen(source)
                command = recognizer.recognize_google(audio).strip().lower()
                display_message(f"You said: {command}")
                return command 
        except sr.UnknownValueError:
            display_message("Sorry, I didn't catch that. Listening again...")
            speak("Sorry, I didn't catch that. Could you please repeat?")
        except sr.RequestError:
            display_message("Voice recognition service is unavailable. Listening again...")
            speak("Voice recognition service is unavailable. Please try again.")

def open_app(command):
    if "open notepad" in command:
        speak("Opening Notepad.")
        display_message("Opening Notepad...")
        os.system("notepad")
    elif "open calculator" in command:
        speak("Opening Calculator.")
        display_message("Opening Calculator...")
        os.system("calc")
    elif "open paint" in command:
        speak("Opening Paint.")
        display_message("Opening Paint...")
        os.system("mspaint")
    elif "open chrome" in command:
        speak("Opening Chrome.")
        display_message("Opening Chrome...")
        os.system(r'"C:\Program Files\Google\Chrome\Application\chrome.exe"')
    elif "open github" in command:
        speak("Opening GitHub.")
        display_message("Opening GitHub...")
        os.system(r"C:\Users\GhosT\AppData\Local\GitHubDesktop\GitHubDesktop.exe")
    elif "open steam" in command:
        speak("Opening Steam.")
        display_message("Opening Steam...")
        os.system(r"C:\Users\Public\Desktop\Steam.lnk")
    elif "open epicgames" in command:
        speak("Opening Epic Games Launcher.")
        display_message("Opening Epic Games Launcher...")
        os.system(r"C:\Users\Public\Desktop\Epic Games Launcher.lnk")
    elif "open edge" in command:
        speak("Opening Microsoft Edge.")
        display_message("Opening Microsoft Edge...")
        os.system(r"C:\Users\GhosT\Desktop\Edge.lnk")
    elif "open nvidia" in command:
        speak("Opening NVIDIA...")
        display_message("Opening NVIDIA...")
        os.system(r"C:\Users\Public\Desktop\Nvidia.lnk")
    elif "open amd" in command:
        speak("Opening AMD Adrenalin.")
        display_message("Opening AMD Adrenalin...")
        os.system(r"C:\Users\GhosT\Desktop\adrenaline.lnk")
    elif "open spotify" in command:
        speak("Opening Spotify.")
        display_message("Opening Spotify...")
        os.system(r"C:\Users\GhosT\Desktop\Spotify.lnk")
    elif "exit" in command:
        speak("Exiting program. Goodbye!")
        display_message("Exiting program. Goodbye!")
        return False
    else:
        display_message("Invalid command. Please try again.")
        speak("Invalid command. Please try again.")
    return True

# GUI functions
def execute_command(command):
    if command:
        open_app(command)

def button_assistant_click():
    assistant_thread = Thread(target=handle_voice_command)
    assistant_thread.start()

def handle_voice_command():
    display_message("Listening...")
    command = listen()
    if command:
        open_app(command)

def display_message(message):
    message_label.configure(text=message)
    app.after(5000, lambda: message_label.configure(text=""))

# Function to update the clock
def update_clock():
    current_time = time.strftime("%H:%M:%S")  # Format as HH:MM:SS
    clock_label.configure(text=current_time)
    app.after(1000, update_clock)  # Refresh every second

# GUI setup
class AnimatedGIF(tk.Label):
    def __init__(self, master, path):
        self.im = Image.open(path)
        self.seq = [ImageTk.PhotoImage(frame.resize((800, 600), Image.LANCZOS))
                    for frame in ImageSequence.Iterator(self.im)]
        self.current_frame = 0
        super().__init__(master, image=self.seq[0])
        self.animate()

    def animate(self):
        self.config(image=self.seq[self.current_frame])
        self.current_frame = (self.current_frame + 1) % len(self.seq)
        self.after(50, self.animate)

app = ctk.CTk()
app.geometry("500x400")
app.title("RxZE AI-the ultimate AI partner")
app.resizable(False, False)

background_frame = tk.Frame(app, bg="black")
background_frame.place(x=0, y=0, relwidth=1, relheight=1)

gif_label = AnimatedGIF(background_frame, r"C:\Users\GhosT\Desktop\main files\a94aee835e16cff4f14c83dac8ffbe10.gif")
gif_label.place(x=0, y=0, relwidth=1, relheight=1)

title_label = ctk.CTkLabel(app, text="Hey, how can I assist you?", font=("Cascadia Code SemiBold", 24), bg_color="black")
title_label.place(x=0, y=0)

message_label = ctk.CTkLabel(app, text="", font=("Cascadia Code SemiBold", 14))
message_label.place(x=10, y=300)

button1 = ctk.CTkButton(app, text="GenAI", command=lambda: subprocess.run(["python", r"C:\Users\GhosT\Desktop\main files\newmain.py"]),
                        width=130, height=50, fg_color="red", hover_color="dark red")
button1.place(x=10, y=55)

# Clock widget next to GenAI button
# Clock widget next to GenAI button with black background
clock_label = ctk.CTkLabel(app, text="", font=("Calibri Light (Headings)", 35), bg_color="black")
clock_label.place(x=350, y=55)  # Position adjusted for alignment
update_clock()  # Start the clock # Start the clock

button2 = ctk.CTkButton(app, text="Assistant", command=button_assistant_click, width=130, height=50, fg_color="green", hover_color="dark green")
button2.place(x=10, y=330)

button3 = ctk.CTkButton(app, text="Comparator", command=lambda: subprocess.run(["python", r"C:\Users\GhosT\Desktop\main files\comparator.py"]),
                        width=130, height=50, fg_color="blue", hover_color="dark blue")
button3.place(x=10, y=140)

button4 = ctk.CTkButton(app, text="Image Generation", command=lambda:subprocess.run(["python", r"C:\Users\GhosT\Desktop\main files\imggen.py"]) , width=130, height=50, fg_color="grey", hover_color="black")
button4.place(x=10, y=230)

app.mainloop()