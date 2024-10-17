import tkinter as tk
from tkinter import messagebox
from PIL import Image
import numpy as np
import os
import ttkbootstrap as ttkb
import threading

# Import the AI models from the ai_models directory
from ai_models.image_classification import AIModuleImageClassification
from ai_models.language_translation import AIModuleLanguageTranslation
from ai_models.sentiment_analysis import AIModuleSentimentAnalysis

# Suppress TensorFlow and HuggingFace warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TensorFlow warnings
os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Function decorator to log actions
def logging_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"Running {func.__name__}...")  # Simulate logging
        return func(*args, **kwargs)
    return wrapper

# Base class for handling common app functionality
class BaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI-Powered Desktop Application")
        self.create_widgets()

    def create_widgets(self):
        raise NotImplementedError("Subclasses should implement this!")  # Polymorphism

# Second base class showing multiple inheritance
class HelpMixin:
    def show_help(self):
        help_text = (
            "Group Members:\n\n"
            "Name: Abinash Kushwaha\n"
            "Student ID: S377464\n\n"
            "Name: Mohammed Sajid Salim\n"
            "Student ID: S372433\n\n"
            "Name: Md. Iftakharul Alam Chowdhury\n"
            "Student ID: S372376\n\n"
            "Name: Albert Osemudiamhen Agbonkhese\n"
            "Student ID: S373500\n"
        )
        messagebox.showinfo("Help - Group Members", help_text)

# Main app class (inherits from BaseApp and HelpMixin)
class AIApp(BaseApp, HelpMixin):
    def __init__(self, root):
        # Initialize the necessary attributes first
        self.source_language = tk.StringVar()
        self.target_language = tk.StringVar()
        self.current_model = None  # To store the selected model instance
        self.translation_thread = None  # Thread for loading the translation model
        self.loading_label = None  # For showing loading message

        # Define the language options before calling the parent class initializer
        self.language_options = {
            'en': 'English',
            'fr': 'French',
            'es': 'Spanish',
            'de': 'German'
        }

        # Initialize the parent class
        super().__init__(root)

    # Overriding the base class method (polymorphism)
    def create_widgets(self):
        # Create a main frame to hold everything
        self.main_frame = ttkb.Frame(self.root, padding=20)
        self.main_frame.pack(fill='both', expand=True)

        # Assignment and Group Info
        self.assignment_info = ttkb.Label(self.main_frame, text="HIT137 - Software Now (Assignment 3)\nGroup - SYD_219",
                                          font=("Helvetica", 16), bootstyle="info")
        self.assignment_info.pack(pady=10)

        # Title
        self.label = ttkb.Label(self.main_frame, text="AI-Powered Application", font=("Helvetica", 22),
                                bootstyle="primary")
        self.label.pack(pady=10)

        # Model selection section
        model_frame = ttkb.Frame(self.main_frame)
        model_frame.pack(fill='x', pady=10)

        self.model_var = tk.StringVar(value="Select a model")
        model_options = ["Image Classification", "Language Translation", "Sentiment Analysis"]
        self.model_dropdown = ttkb.Combobox(model_frame, textvariable=self.model_var, values=model_options,
                                            state="readonly", font=("Arial", 12))
        self.model_dropdown.grid(row=0, column=0, padx=10)

        self.load_model_button = ttkb.Button(model_frame, text="Load Model", command=self.load_ai_model,
                                             bootstyle="success")
        self.load_model_button.grid(row=0, column=1, padx=10)

        # Input field for text or image paths
        input_frame = ttkb.Frame(self.main_frame)
        input_frame.pack(fill='x', pady=10)

        self.input_label = ttkb.Label(input_frame, text="Input (Text or Image):", font=("Arial", 12))
        self.input_label.grid(row=0, column=0, padx=10)

        self.input_field = ttkb.Entry(input_frame, font=("Arial", 12), width=50)
        self.input_field.grid(row=0, column=1, padx=10)

        # Run model button
        self.classify_button = ttkb.Button(self.main_frame, text="Run Model", command=self.run_model,
                                           bootstyle="warning")
        self.classify_button.pack(pady=20)

        # Output display
        self.output_label = ttkb.Label(self.main_frame, text="Prediction: ", font=("Arial", 14), bootstyle="inverse")
        self.output_label.pack(pady=10)

        # Translation-specific widgets (hidden by default)
        translation_frame = ttkb.Frame(self.main_frame)
        self.source_lang_label = ttkb.Label(translation_frame, text="Source Language", font=("Arial", 12))
        self.target_lang_label = ttkb.Label(translation_frame, text="Target Language", font=("Arial", 12))
        self.source_lang_dropdown = ttkb.Combobox(translation_frame, textvariable=self.source_language,
                                                  values=list(self.language_options.values()), state="readonly")
        self.target_lang_dropdown = ttkb.Combobox(translation_frame, textvariable=self.target_language,
                                                  values=list(self.language_options.values()), state="readonly")

        # Pack translation widgets
        self.source_lang_label.grid(row=0, column=0, padx=10, pady=5)
        self.source_lang_dropdown.grid(row=0, column=1, padx=10, pady=5)
        self.target_lang_label.grid(row=1, column=0, padx=10, pady=5)
        self.target_lang_dropdown.grid(row=1, column=1, padx=10, pady=5)
        translation_frame.pack_forget()  # Initially hide

        self.translation_frame = translation_frame  # Save the frame reference for show/hide logic

        # Help button
        self.help_button = ttkb.Button(self.main_frame, text="Help", command=self.show_help, bootstyle="danger")
        self.help_button.pack(pady=10)

    # Load the selected AI model with threading for background loading
    @logging_decorator
    def load_ai_model(self):
        model_choice = self.model_var.get()

        # Reset input fields and hide translation widgets
        self.hide_translation_options()

        if model_choice == "Image Classification":
            self.current_model = AIModuleImageClassification()
            result = self.current_model.load_model()
            messagebox.showinfo("Model Status", result)

        elif model_choice == "Language Translation":
            self.translation_frame.pack(pady=10)  # Show translation options for source and target languages
            # Validate that source and target languages are selected
            if not self.source_language.get() or not self.target_language.get():
                messagebox.showwarning("Warning",
                                       "Please select both source and target languages before loading the model.")
                return
            # Start a thread to load the model in the background
            self.translation_thread = threading.Thread(target=self.load_translation_model)
            self.translation_thread.start()

        elif model_choice == "Sentiment Analysis":
            self.current_model = AIModuleSentimentAnalysis()
            result = self.current_model.load_model()
            messagebox.showinfo("Model Status", result)

    def load_translation_model(self):
        source_lang = list(self.language_options.keys())[
            list(self.language_options.values()).index(self.source_language.get())]
        target_lang = list(self.language_options.keys())[
            list(self.language_options.values()).index(self.target_language.get())]

        self.show_loading_message("Loading language translation model...")
        self.current_model = AIModuleLanguageTranslation()
        result = self.current_model.load_model(source_lang, target_lang)
        self.hide_loading_message()
        messagebox.showinfo("Model Status", result)

    def show_loading_message(self, message):
        if not self.loading_label:
            self.loading_label = ttkb.Label(self.main_frame, text=message, bootstyle="info")
            self.loading_label.pack(pady=10)

    def hide_loading_message(self):
        if self.loading_label:
            self.loading_label.pack_forget()
            self.loading_label = None

    def hide_translation_options(self):
        self.translation_frame.pack_forget()

    # Run the selected model on the input
    @logging_decorator
    def run_model(self):
        model_choice = self.model_var.get()

        if model_choice == "Language Translation":
            if not self.translation_thread or not self.translation_thread.is_alive():
                input_data = self.input_field.get()
                if not input_data:
                    messagebox.showwarning("Warning", "Please enter text input for language translation!")
                    return
                prediction = self.current_model.predict(input_data)
                self.output_label.config(text=f"Prediction: {prediction}")
            else:
                messagebox.showwarning("Warning", "Please wait, the translation model is still loading!")

        elif model_choice == "Sentiment Analysis":
            input_data = self.input_field.get()
            if not input_data:
                messagebox.showwarning("Warning", "Please enter text input for sentiment analysis!")
                return

            sentiment_scores = self.current_model.predict(input_data)
            self.display_sentiment_scores(sentiment_scores)

        elif self.current_model is None:
            messagebox.showwarning("Warning", "Please select and load a model first!")
            return

        elif isinstance(self.current_model, AIModuleImageClassification):
            if not self.input_field.get():
                messagebox.showwarning("Warning", "Please provide an image file path!")
                return
            image_path = self.input_field.get()
            try:
                image = Image.open(image_path).resize((224, 224))
                image_array = np.array(image)
                prediction = self.current_model.predict(image_array)
                self.output_label.config(text=f"Prediction: {prediction}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to process image: {e}")

    def display_sentiment_scores(self, sentiment_scores):
        """Display detailed sentiment scores as text."""
        # Show detailed scores in a label
        details = f"Positive: {sentiment_scores['pos'] * 100:.2f}%\n"
        details += f"Neutral: {sentiment_scores['neu'] * 100:.2f}%\n"
        details += f"Negative: {sentiment_scores['neg'] * 100:.2f}%\n"
        details += f"Compound: {sentiment_scores['compound']:.2f}"
        self.output_label.config(text=details)


# Main application runner
if __name__ == "__main__":
    root = ttkb.Window("AI Desktop Application", themename="darkly")
    root.geometry("700x800")  # Increased size to ensure the text fits well
    app = AIApp(root)
    root.mainloop()
