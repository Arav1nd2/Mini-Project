# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 02:00:08 2020

@author: Intelligent Systems
"""

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
# import pyaudio
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

save_path = "orginal.jpg"
def get_wav_info(wav_file):
    wav = wave.open(wav_file, 'r')
    frames = wav.readframes(-1)
    sound_info = pylab.fromstring(frames, 'int16')
    frame_rate = wav.getframerate()
    wav.close()
    return sound_info, frame_rate

@app.route("/", methods=["GET", "POST"])
@cross_origin()
def asdf():
    start_time = time.time()

    # FILE_NAME="orginal.wav"
    # FILE_NAME="orginal.wav"
    # waved=FILE_NAME
    name = request.form.get("name")
    
    # file1 = request.files['image']

    # print("ddddd", name)
    # print("hii")
    name = literal_eval(name)
    # print(type(name))
    res = bytearray(name)
    # print(res)
    # with open('myfile1.wav', mode='bx') as f:
    #     f.write(res)
    tempWavFile = tempfile.mktemp(".wav")
    tempWavFile1 = tempfile.mktemp(".wav")
    tempImageFile = tempfile.mktemp(".jpg")

    with open(tempWavFile, mode="bx") as f:
        f.write(res)

    command = (

        
        "ffmpeg -y -i " + tempWavFile + " -ab 160k -ac 2 -ar 44100 -vn " + tempWavFile1
    )
    subprocess.call(command, shell=True)
    # with open('myfile.wav', mode='bx') as f:
    #     f.write(res)

    # filename = file1.filename
    # print(filename)

    # print(waved)
    sound_info, frame_rate = get_wav_info(tempWavFile1)
    pylab.axis('off') # no axis
    pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[]) 
    pylab.specgram(sound_info, Fs=frame_rate)
    pylab.savefig(tempImageFile)
    pylab.savefig("tempImageFile.jpg")
    pylab.close()
    st = "0" * 1
    test_feat = list(st)

    # im = cv2.imread(tempImageFile)
    img = skimage.io.imread(tempImageFile)
    img_resized = resize(img, (100,100), anti_aliasing=True, mode='reflect')
    # op = cv2.resize(im, (100, 100))
    # blob = cv2.dnn.blobFromImage(op)
    # b = []
    # for i in blob:
    #     for j in i:
    #         for k in j:
    #             b.extend(k)
    # b = np.asarray(b)
    test_feat[0] = img_resized
    test_feat = np.asarray(test_feat)

    y = clf1.predict(test_feat[0].reshape(1,-1))
    print("result   ",y)
    # print("--- %s seconds ---" % str(time.time() - start_time))
    # print(y)
    data = {"time": str(time.time() - start_time), "result": str(y)}
    js = json.dumps(data)
    res = Response(js, status=200, mimetype="application/json")
    return res

@app.route("/file", methods=["GET", "POST"])
@cross_origin()
def asdf1():
    start_time = time.time()
    print("asdfasfd")
    # FILE_NAME="orginal.wav"
    # FILE_NAME="orginal.wav"
    # waved=FILE_NAME
    # file = request.form.get("image")
    file = request.files['image']
    if file:
        filename = file.filename

        file_path = os.path.join(filename)
        print("file path ",file_path)
        file.save(file_path)
    
    # print("hii")
    # name = literal_eval(name)
    # # print(type(name))
    # res = bytearray(name)
    # # print(res)
    # # with open('myfile1.wav', mode='bx') as f:
    # #     f.write(res)
    # tempWavFile = tempfile.mktemp(".wav")
    # tempWavFile1 = tempfile.mktemp(".wav")
    tempImageFile = tempfile.mktemp(".jpg")

    # with open(tempWavFile, mode="bx") as f:
    #     f.write(res)

    # command = (

        
    #     "ffmpeg -y -i " + tempWavFile + " -ab 160k -ac 2 -ar 44100 -vn " + tempWavFile1
    # )
    # subprocess.call(command, shell=True)
    # with open('myfile.wav', mode='bx') as f:
    #     f.write(res)

    # filename = file1.filename
    # print(filename)

    # print(waved)
    # x, sample_rate = librosa.load(file_path)
    # fmax = sample_rate / 2

    # mel_spec_power = librosa.feature.melspectrogram(
    #     x,
    #     sr=sample_rate,
    #     n_fft=n_fft,
    #     hop_length=hop_length,
    #     n_mels=n_mels,
    #     power=2.0,
    #     fmin=fmin,
    #     fmax=fmax,
    # )
    # mel_spec_db = librosa.power_to_db(mel_spec_power, ref=np.max)
    # # print(mel_spec_db)
    # tempImageFile = tempfile.mktemp(".jpg")
    # plt.imsave(tempImageFile, mel_spec_db)
    sound_info, frame_rate = get_wav_info(file_path)
    pylab.axis('off') # no axis
    pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[]) 
    pylab.specgram(sound_info, Fs=frame_rate)
    pylab.savefig(tempImageFile)
    pylab.savefig("tempImageFile.jpg")
    pylab.close()
    st = "0" * 1
    test_feat = list(st)

    # im = cv2.imread(tempImageFile)
    img = skimage.io.imread(tempImageFile)
    img_resized = resize(img, (100,100), anti_aliasing=True, mode='reflect')
    # op = cv2.resize(im, (100, 100))
    # blob = cv2.dnn.blobFromImage(op)
    # b = []
    # for i in blob:
    #     for j in i:
    #         for k in j:
    #             b.extend(k)
    # b = np.asarray(b)
    test_feat[0] = img_resized
    test_feat = np.asarray(test_feat)

    y = clf1.predict(test_feat[0].reshape(1,-1))
    print("result   ",y)
    # print("--- %s seconds ---" % str(time.time() - start_time))
    # print(y)
    data = {"time": str(time.time() - start_time), "result": str(y)}
    js = json.dumps(data)
    res = Response(js, status=200, mimetype="application/json")
    return res


if __name__ == "__main__":
    filename = "100Spect_97_compress.pkl"
    clf1 = joblib.load(filename)
    n_fft = 1024
    hop_length = 256
    n_mels = 40
    fmin = 20

    app.run(debug=True)