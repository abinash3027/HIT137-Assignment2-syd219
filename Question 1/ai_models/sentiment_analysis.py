from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# AI Model for Sentiment Analysis with detailed output
class AIModuleSentimentAnalysis:
    def __init__(self):
        self.model = None
        self.model_loaded = False

    def load_model(self):
        self.model = SentimentIntensityAnalyzer()
        self.model_loaded = True
        return "Sentiment Analysis Model loaded!"

    def predict(self, text):
        if not self.model_loaded:
            raise ValueError("Sentiment analysis model is not loaded yet!")
        return self.model.polarity_scores(text)
