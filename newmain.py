import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
import google.generativeai as genai
from langchain_ollama import OllamaLLM
import pyttsx3
import threading
import queue


# Response from local LLM
def create_chatbot(model_name):
    model = OllamaLLM(model=model_name)
    return model


# Response from Gemini API
genai.configure(api_key="")  
gemini_model = genai.GenerativeModel("gemini-1.5-flash")


def clean_response(response):
    cleaned_response = response.replace("<think>", "").strip()
    cleaned_response = " ".join(cleaned_response.split())
    return cleaned_response


def generate_response_gemini(ques):
    response = gemini_model.generate_content(ques)
    return response.text


def deepseek_local(ques):
    try:
        model_name = "deepseek-r1:1.5b"
        local_model = create_chatbot(model_name)
        response = local_model(ques)
        return clean_response(response)
    except Exception as e:
        return f"Error in DeepSeek: {str(e)}"


def llama_local(ques):
    model_name = "llama3.2"
    local_model = create_chatbot(model_name)
    response = local_model(ques)
    return response


def gemma_local(ques):
    model_name = "gemma3"
    local_model = create_chatbot(model_name)
    response = local_model(ques)
    return response


# Main application class
class ChatbotApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.tts_engine = None  # Initialize TTS engine as None
        self.tts_enabled = False
        self.tts_queue = queue.Queue()
        self.tts_thread = threading.Thread(target=self._tts_worker, daemon=True)
        self.tts_thread.start()

        # Main window
        self.title("Chatbot UI")
        self.geometry("700x600")
        self.resizable(False, False)

        # Background image
        self.background_image = Image.open(r"C:\Users\GhosT\Desktop\main files\neon1.png")
        self.background_image = self.background_image.resize((1425, 1575), Image.LANCZOS)
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        self.background_label = tk.Label(self, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.background_label.lower()

        # Chat display
        self.chat_frame = ctk.CTkFrame(self, width=680, height=500, fg_color="black")
        self.chat_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.chat_display = tk.Text(
            self.chat_frame, wrap="word", width=80, height=25, state="disabled",
            bg="black", fg="white", font=("Yu Gothic UI Semibold", 12), borderwidth=0, highlightthickness=0
        )
        self.chat_display.pack(pady=10, padx=10, fill="both", expand=True)

        self.chat_display.tag_configure("user", justify="right", foreground="white", font=("Yu Gothic UI Semibold", 22))
        self.chat_display.tag_configure("bot", justify="left", foreground="white", font=("Yu Gothic UI Semibold", 22))

        # User input
        self.input_frame = ctk.CTkFrame(self, width=680, height=50, fg_color="black")
        self.input_frame.pack(side="bottom", pady=10, padx=10, fill="x")

        self.user_input = ctk.CTkEntry(
            self.input_frame, width=550, placeholder_text="Type your query here...",
            fg_color="black", text_color="white", font=("Yu Gothic UI Semibold", 12)
        )
        self.user_input.pack(side="left", padx=10)

        self.user_input.bind("<Return>", self.handle_enter_key)

        self.send_button = ctk.CTkButton(self.input_frame, text="Send", width=100, command=self.generate_response)
        self.send_button.pack(side="right", padx=10)

        # Settings
        self.settings_frame = ctk.CTkFrame(self, width=680, height=50, fg_color="black")
        self.settings_frame.pack(pady=10, padx=10, fill="x")

        self.mode_label = ctk.CTkLabel(self.settings_frame, text="Select Mode:", text_color="white")
        self.mode_label.pack(side="left", padx=10)

        self.mode_var = ctk.StringVar(value="Gemini")
        self.mode_slider = ctk.CTkSegmentedButton(
            self.settings_frame, values=["deepseek", "llama", "gemma", "Gemini"], variable=self.mode_var,
            command=self.on_mode_change  # Add callback for mode change
        )
        self.mode_slider.pack(side="left", padx=10)

        self.clear_button = ctk.CTkButton(self.settings_frame, text="Clear", width=90, command=self.clear_chat_display)
        self.clear_button.pack(side="right", padx=10)

        self.tts_button = ctk.CTkButton(self.settings_frame, text="Enable TTS", width=120, command=self.toggle_tts)
        self.tts_button.pack(side="right", padx=10)

    def handle_enter_key(self, event):
        self.generate_response()

    def generate_response(self):
        user_message = self.user_input.get().strip()
        if user_message:
            self.chat_display.configure(state="normal")
            self.chat_display.insert("end", f" {user_message}\n", "user")
            self.chat_display.configure(state="disabled")

            selected_mode = self.mode_var.get()
            if selected_mode == "deepseek":
                response = deepseek_local(user_message)
            elif selected_mode == "llama":
                response = llama_local(user_message)
            elif selected_mode == "gemma":
                response = gemma_local(user_message)
            elif selected_mode == "Gemini":
                response = generate_response_gemini(user_message)
            else:
                response = "Invalid mode selected."

            response = clean_response(response)
            self.chat_display.configure(state="normal")
            self.chat_display.insert("end", f"RxZE: {response}\n", "bot")
            self.chat_display.configure(state="disabled")
            self.user_input.delete(0, "end")

            if self.tts_enabled:
                self.tts_queue.put(response)  # Add response to TTS queue

    def clear_chat_display(self):
        self.clear_button.configure(state="disabled")  # Disable button while clearing
        self.stop_tts()  # Stop TTS immediately
        self.chat_display.configure(state="normal")
        self.chat_display.delete("1.0", "end")
        self.chat_display.configure(state="disabled")
        self.clear_button.configure(state="normal")  # Re-enable button

    def toggle_tts(self):
        self.tts_enabled = not self.tts_enabled
        self.tts_button.configure(text="Disable TTS" if self.tts_enabled else "Enable TTS")
        if not self.tts_enabled:
            self.stop_tts()  # Stop TTS immediately

    def on_mode_change(self, *args):
        """Callback function triggered when the mode is changed."""
        self.stop_tts()  # Stop TTS immediately
        self.clear_chat_display()  # Clear the chat display when mode changes

    def stop_tts(self):
        """Stop the TTS engine and clear the queue."""
        if self.tts_engine:
            self.tts_engine.stop()  # Stop the TTS engine
            self.tts_engine = None  # Reset the TTS engine
        self.tts_queue.queue.clear()  # Clear the TTS queue

    def _tts_worker(self):
        while True:
            text = self.tts_queue.get()
            if text is not None:
                if not self.tts_engine:  # Reinitialize TTS engine if it was stopped
                    self.tts_engine = pyttsx3.init()
                    self.tts_engine.setProperty("rate", 150)
                    self.tts_engine.setProperty("volume", 1.0)
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            self.tts_queue.task_done()


if __name__ == "__main__":
    app = ChatbotApp()
    app.mainloop()
