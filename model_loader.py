import os
import tensorflow as tf

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'best_model.h5')

def load_model():
    model = tf.keras.models.load_model(MODEL_PATH)
    return model