import os
import wave
import pickle
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from tensorflow.keras.models import load_model
from pathlib import Path
from PIL import Image

with open('modelo_random_forest.pkl', 'rb') as file:
    modeloRandomForest = pickle.load(file)

modeloCNN = load_model("modeloOptimizadoCNN.h5")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class PredictionResult(BaseModel):
    prediction: str
    probability: float

@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

def read_audio_rf(file: UploadFile):
    try:
        with wave.open(file.file, 'rb') as audioFile:
            amountFrames = audioFile.getnframes()
            datosAudio = audioFile.readframes(amountFrames)
            audioData = np.frombuffer(datosAudio, dtype=np.int16).astype(np.float32) / 32767.0
        return audioData
    except Exception as e:
        raise ValueError("Error al leer el archivo de audio") from e

def normalize_audio_rf(audio_data, duration_frames):
    if len(audio_data) > duration_frames:
        audio_data = audio_data[:duration_frames]
    else:
        audio_data = np.pad(audio_data, (0, duration_frames - len(audio_data)), 'constant')
    return audio_data

def predict_random_forest(file: UploadFile):
    audio_data = read_audio_rf(file)
    duration_frames = 57170 
    audio_data = normalize_audio_rf(audio_data, duration_frames)
    features = audio_data.reshape(1, -1)
    prediction = modeloRandomForest.predict(features)[0]
    probability = max(modeloRandomForest.predict_proba(features)[0])
    return prediction, probability

def extract_spectrogram(file, filename):
    audio, sr = librosa.load(file)
    spectrogram = librosa.stft(audio) 
    spectrogram_db = librosa.amplitude_to_db(abs(spectrogram))

    plt.figure(figsize=(10, 4))
    librosa.display.specshow(spectrogram_db, sr=sr, x_axis='time', y_axis='log')
    plt.axis('off')
    plt.savefig(f'./uploads/{filename}.png', bbox_inches='tight', pad_inches=0.0)
    plt.close()

def load_image_from_folder(filename):
    img_path = './uploads/' + filename + '.png'

    if img_path.endswith(('.png', '.jpg', '.jpeg')):
        img = Image.open(img_path)
    
    return np.array(img)

def predict_cnn(file: UploadFile):
    extract_spectrogram(file.file, file.filename)
    imgData = load_image_from_folder(file.filename)
    image = imgData / 255.0
    image = np.expand_dims(image, axis=0)
    prediction = modeloCNN.predict(image)[0]
    probability = max(prediction)
    prediction = np.argmax(prediction)
    threshold = 0.99
    prediction = "1 | Patologíca" if probability > threshold else "0 | Normal"
    return prediction, probability

@app.post("/predict")
async def predict(request: Request, model_type: str = Form(...), file: UploadFile = File(...)):
    if model_type == 'random_forest':
        prediction, probability = predict_random_forest(file)
    else:
        prediction, probability = predict_cnn(file)
        
    return templates.TemplateResponse("result.html", {
        "request": request,
        "prediction": prediction,
        "probability": probability
    })