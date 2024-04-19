import pickle
import os
from pathlib import Path
import pandas as pd
# from utils import data_pipline
from .utils import data_pipline

# Load Model
path_to_model = os.path.join(Path(__file__).parent, 'water_quality.pkl')
# Loading using pickle (if model was saved with pickle):
with open(path_to_model, 'rb') as f:
    model = pickle.load(f)
    
def load_the_model():
    with open(path_to_model, 'rb') as f:
        model = pickle.load(f)
    return model
def predict_water_qaulity(feature, model):
    data = data_pipline(feature)
    pred = model.predict(data)
    return pred