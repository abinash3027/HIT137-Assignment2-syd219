import tensorflow as tf
import numpy as np

# AI Model for Image Classification
class AIModuleImageClassification:
    def __init__(self):
        self.model = None
        self.model_loaded = False

    def load_model(self):
        self.model = tf.keras.applications.MobileNetV2(weights='imagenet')
        self.model_loaded = True
        return "Image Classification Model loaded!"

    def predict(self, image):
        if not self.model_loaded:
            raise ValueError("Model is not loaded yet!")
        image = tf.keras.applications.mobilenet_v2.preprocess_input(image)
        predictions = self.model.predict(np.expand_dims(image, axis=0))
        decoded_predictions = tf.keras.applications.mobilenet_v2.decode_predictions(predictions, top=1)
        return decoded_predictions[0][0][1]
