
import librosa
import numpy as np
import os
import matplotlib.pyplot as plt
import cv2
from flask import Flask, request, url_for, Response
import simplejson as json
from sklearn.externals import joblib

import wave
import pylab
import wave
from array import array
import time
from ast import literal_eval
import subprocess
import tempfile

import skimage
from skimage.io import imread
from skimage.transform import resize

from flask_cors import CORS, cross_origin


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def get_wav_info(wav_file):
    wav = wave.open(wav_file, 'r')
    frames = wav.readframes(-1)
    sound_info = pylab.fromstring(frames, 'int16')
    frame_rate = wav.getframerate()
    wav.close()
    return sound_info, frame_rate


@app.route("/file", methods=["GET", "POST"])
@cross_origin()
def predict():
    start_time = time.time()
    file = request.files['image']
    if file:
        filename = file.filename

        file_path = os.path.join(filename)
        print("file path ",file_path)
        file.save(file_path)
    tempImageFile = tempfile.mktemp(".jpg")
    sound_info, frame_rate = get_wav_info(file_path)
    pylab.axis('off') # no axis
    pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[]) 
    pylab.specgram(sound_info, Fs=frame_rate)
    pylab.savefig(tempImageFile)
    pylab.savefig("tempImageFile.jpg")
    pylab.close()
    st = "0" * 1
    test_feat = list(st)
    img = skimage.io.imread(tempImageFile)
    img_resized = resize(img, (100,100), anti_aliasing=True, mode='reflect')
    test_feat[0] = img_resized
    test_feat = np.asarray(test_feat)

    y = clf1.predict(test_feat[0].reshape(1,-1))
    print("result   ",y)
    data = {"time": str(time.time() - start_time), "result": str(y)}
    js = json.dumps(data)
    res = Response(js, status=200, mimetype="application/json")
    return res

if __name__ == "__main__":
    filename = "PreTrained_SVM_Model.pkl"
    clf1 = joblib.load(filename)
    app.run(debug=True)