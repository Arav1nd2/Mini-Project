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
import numpy as np
mport pandas as pd
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


from sklearn.decomposition import PCA
def getPCA(glottalFileName):
    # Extract DataFrame from Glottal CSV
    df=pd.read_csv(glottalFileName)
    df=d1.replace(np.nan,0,regex=True)

    X_std=StandardScaler().fit_transform(df)

    # PCA 
    pca=PCA(n_components=30)
    pca.fit_transform(X_std)
    X_pca=pca.transform(X_std
    a = numpy.asarray(X_pca)
    # Save in PCA.csv
    np.savetxt("./output/D/pca.csv", a, delimiter=",")

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

    # Generate Acoustice feature form Aparat tool save in to acoustic.csv
    acoustic_feature = os.system("./SMILExtract -C ./config/IS09_emotion.conf -I ${filename} -csvoutput ./output/D/$acoustic.csv")

    # Generate Glottal feature from QCP tool save in to glottal.csv
    glottal_feature = os.system("./SMILExtract -C ./config/IS09_emotion.conf -I ${filename} -csvoutput ./output/D/$glottal.csv")

    # Perform PCA on glottal feature
    getPCA("./output/D/glottal.csv")

    # Get DataFrame for all features
    df_acoustic = pd.read_csv("./output/D/acoustic.csv")
    df_glottal = pd.read_csv("./output/D/glottal.csv")
    df_pca = pd.read_csv("./output/D/pca.csv")

    # combine all dataframe
    df = df_acoustic + df_glottal + df_pca

    # Feature obtained from Sequential Forward Selector

    data_frame =  df['pcm_RMSenergy_sma_min', 'pcm_RMSenergy_sma_linregc1',
       'pcm_RMSenergy_sma_linregc2', 'pcm_RMSenergy_sma_linregerrQ',
       'pcm_fftMag_mfcc_sma[5]_linregc1', 'pcm_zcr_sma_linregc1',
       'voiceProb_sma_linregc1', 'F0_sma_min', 'F0_sma_minPos',
       'pcm_RMSenergy_sma_de_amean', 'pcm_RMSenergy_sma_de_linregc1',
       'pcm_RMSenergy_sma_de_linregc2', 'pcm_RMSenergy_sma_de_linregerrQ',
       'pcm_RMSenergy_sma_de_stddev', 'pcm_fftMag_mfcc_sma_de[1]_linregc1',
       'pcm_fftMag_mfcc_sma_de[2]_linregc1',
       'pcm_fftMag_mfcc_sma_de[6]_linregc1',
       'pcm_fftMag_mfcc_sma_de[9]_linregc1',
       'pcm_fftMag_mfcc_sma_de[10]_linregc1',
       'pcm_fftMag_mfcc_sma_de[12]_linregc1']

    y_predict = classifier.predict(data_frame)

    print("result   ",y_predict)
    data = {"time": str(time.time() - start_time), "result": str(y_predict)}
    js = json.dumps(data)
    res = Response(js, status=200, mimetype="application/json")
    return res

if __name__ == "__main__":
    filename = "PreTrained_SVM_Model.pkl"
    classifier = joblib.load(filename)
    app.run(debug=True)