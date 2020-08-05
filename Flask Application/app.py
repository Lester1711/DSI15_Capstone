from __future__ import division, print_function

# coding=utf-8
import sys
import os
import numpy as np
import cv2

# Keras
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from tensorflow.keras.models import load_model
from keras.preprocessing.image import image

# Flask utils
import time
from flask import Flask, redirect, url_for, request, render_template,jsonify
from werkzeug.utils import secure_filename
from PIL import Image

# Define a flask app
app = Flask(__name__)

# Model saved with Keras model.save()
NBRS_PATH = 'model/nbrs_model.sav'
MODEL_PATH= "model/lenet_features_extractor.h5"


model=load_model(MODEL_PATH)
import joblib
import shutil
nbrs = joblib.load(NBRS_PATH)
train = joblib.load("model/xtrain.sav")
print('Model loaded. Check http://127.0.0.1:5000/ or http://localhost:5000/')

def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(128, 128))

    # Preprocessing the image
    x = image.img_to_array(img)
    x = x/255
    x = np.expand_dims(x, axis=0)
    
    predictions = model.predict(x)
    print(predictions.shape)
    indecis = nbrs.kneighbors(predictions,3,return_distance=False)
    return indecis


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path, model)
        dir="static/recommended"
        if os.path.exists(dir):
            shutil.rmtree(dir)
        os.makedirs(dir)
        data = preds[0,:]
        for x in data:
            im = Image.fromarray((train[x] * 255).astype(np.uint8))
            files=os.path.join(basepath,'static/recommended',secure_filename("rec_"+str(x)+ str(int(time.time()))+".jpeg"))
            im.save(files,'JPEG') 
            print(x)
           
        hists = os.listdir('static/recommended')
        hists = ['recommended/' + file for file in hists]
        return jsonify(hists)
    return None
    


if __name__ == '__main__':

    app.run(host='0.0.0.0',port=5000,debug=True)
