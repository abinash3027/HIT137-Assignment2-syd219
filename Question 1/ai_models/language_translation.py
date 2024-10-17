from transformers import pipeline

# AI Model for Language Translation using HuggingFace Transformers
class AIModuleLanguageTranslation:
    def __init__(self):
        self.translation_model = None
        self.model_loaded = False

    def load_model(self, source_language, target_language):
        try:
            model_name = f'Helsinki-NLP/opus-mt-{source_language}-{target_language}'
            self.translation_model = pipeline('translation', model=model_name, framework='pt')  # Use PyTorch backend
            self.model_loaded = True
            return f"Language Translation Model loaded for {source_language} to {target_language}!"
        except Exception as e:
            return f"Error loading translation model: {str(e)}"

    def predict(self, text):
        if not self.model_loaded:
            raise ValueError("Translation model is not loaded yet!")
        try:
            return self.translation_model(text)[0]['translation_text']
        except Exception as e:
            return f"Error during translation: {str(e)}"
