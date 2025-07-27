from openai import OpenAI
import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk  # Import Pillow for image handling
import google.generativeai as genai
import asyncio
from langchain_ollama import OllamaLLM

# Response from local LLM
def create_chatbot(model_name):
    model = OllamaLLM(model=model_name)
    return model

def deepseek_local(ques):
    try:
        model_name = "deepseek-r1:1.5b"
        local_model = create_chatbot(model_name)
        response = local_model(ques)
        return response
    except Exception as e:
        return f"Error in DeepSeek: {str(e)}"

# Initialize OpenAI client
client = OpenAI(
    api_key=""  # Replace with your OpenAI API key
)

# Initialize Gemini client
genai.configure(api_key="")  # Replace with your Gemini API key
gemini_model = genai.GenerativeModel("gemini-1.5-flash")

# Function for generating Gemini responses
def generate_response_gemini(ques):
    response = gemini_model.generate_content(ques)
    return response.text

class TripleOutputUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Main window setup
        self.title("Triple Output UI")
        self.geometry("800x700")
        self.resizable(False, False)

        # Set appearance mode and background color
        ctk.set_appearance_mode("dark")
        self.configure(fg_color="black")  # Set entire background to black

        # Load and set the background image using Pillow
        self.background_image = Image.open(r"C:\Users\GhosT\Desktop\main files\neon1.png")  # Replace with your image file path
        self.background_image = self.background_image.resize((3000, 1700), Image.LANCZOS)
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        self.background_label = tk.Label(self, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Output frame section
        output_frame = ctk.CTkFrame(self, fg_color="black")  # Separate frame for output
        output_frame.pack(fill="both", expand=True, pady=(10, 20))  # Spacing around output frame

        output_frame.grid_columnconfigure(0, weight=1)
        output_frame.grid_columnconfigure(1, minsize=1)  # Divider
        output_frame.grid_columnconfigure(2, weight=1)
        output_frame.grid_columnconfigure(3, minsize=1)  # Divider
        output_frame.grid_columnconfigure(4, weight=1)
        output_frame.grid_rowconfigure(0, weight=1)

        # Create 3 divided output boxes for responses
        self.output1 = self.create_output_box(output_frame, 0, 0, font_size=16)
        ctk.CTkFrame(output_frame, fg_color="white", width=1).grid(row=0, column=1, sticky="ns", padx=2)  # Divider is white
        self.output2 = self.create_output_box(output_frame, 0, 2, font_size=16)
        ctk.CTkFrame(output_frame, fg_color="white", width=1).grid(row=0, column=3, sticky="ns", padx=2)  # Divider is white
        self.output3 = self.create_output_box(output_frame, 0, 4, font_size=16)

        # Input frame section
        input_frame = ctk.CTkFrame(self, fg_color="black")  # Separate frame for input
        input_frame.pack(fill="x", pady=(20, 0))  # Padding above the input frame for spacing

        self.user_input = ctk.CTkEntry(
            input_frame,
            width=550,
            placeholder_text="Type your query here...",
            fg_color="black",
            text_color="white",
            font=("Consolas", 16),
        )
        self.user_input.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.send_button = ctk.CTkButton(
            input_frame, text="Send", width=100, fg_color="black",
            hover_color="gray", font=("Consolas", 12), command=self.handle_query
        )
        self.send_button.pack(side="right", padx=10)

    def create_output_box(self, parent, row, column, font_size=16):
        frame = ctk.CTkFrame(parent, fg_color="black", corner_radius=4)
        frame.grid(row=row, column=column, sticky="nsew", padx=(0, 2))

        text_widget = tk.Text(
            frame, wrap="word", bg="black", fg="white", font=("Consolas", font_size),
            borderwidth=0, highlightthickness=0, insertbackground="white", padx=10, pady=10
        )
        text_widget.config(state="disabled")
        text_widget.pack(fill="both", expand=True)
        return text_widget

    def handle_query(self):
        query = self.user_input.get().strip()
        if not query:
            return

        # OpenAI response
        try:
            openai_completion = client.chat.completions.create(
                model="gpt-4o-mini",
                store=True,
                messages=[{"role": "user", "content": query}]
            )
            openai_response = openai_completion.choices[0].message.content.strip()
        except Exception as e:
            openai_response = f"Error with OpenAI API: {str(e)}"

        # Gemini response
        try: 
            gemini_response = generate_response_gemini(query)
        except Exception as e:
            gemini_response = f"Error with Gemini API: {str(e)}"
        deepseek_response= deepseek_local(query)
        # Insert responses into separate boxes
        self.insert_response_box1(query, openai_response)
        self.insert_response_box2(query, gemini_response)
        self.insert_response_box3(query,deepseek_local)

        # Clear user input
        self.user_input.delete(0, "end")

    def insert_response_box1(self, query, response):
        self.output1.config(state="normal")
        self.output1.delete("1.0", "end")
        self.output1.tag_configure("right", justify="right")
        self.output1.insert("end", f"{query}\n\n", "right")
        self.output1.insert("end", f"OpenAI: {response}")
        self.output1.config(state="disabled")

    def insert_response_box2(self, query, response):
        self.output2.config(state="normal")
        self.output2.delete("1.0", "end")
        self.output2.tag_configure("right", justify="right")
        self.output2.insert("end", f"{query}\n\n", "right")
        self.output2.insert("end", f"Gemini: {response}")
        self.output2.config(state="disabled")

    def insert_response_box3(self, query, response):
        self.output3.config(state="normal")
        self.output3.delete("1.0", "end")
        self.output3.tag_configure("right", justify="right")
        self.output3.insert("end", f"{query}\n\n", "right")
        self.output3.insert("end", f"deepseek:{deepseek_local(query)}")
        self.output3.config(state="disabled")


if __name__ == "__main__":
    app = TripleOutputUI()
    app.mainloop()
