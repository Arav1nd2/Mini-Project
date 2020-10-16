#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 12:38:08 2020

@author: aravind
"""

from glottal_extract import glottal_features
from acoustic_extract import acoustic_features
import argparse
import sys
import shutil
import os
import pandas as pd

# Initiate the parser
parser = argparse.ArgumentParser()

# Add long and short argument
parser.add_argument("--version", "-v",
                    help="Shows the active version of the library", action="store_true")
parser.add_argument('--input', '-i', help="Sets the path to input dataset")
parser.add_argument(
    "--output", '-o', help="Sets the ouput for the resultant feature set")


# Read arguments from the command line
args = parser.parse_args()

input_path = './Data'
output_path = '.'

if args.version:
    print("Version v1.0.0")
    sys.exit()
elif args.input:
    input_path = args.input
elif args.output:
    output_path = args.output

print("Starting to extract glottal features.....")
if os.path.isdir('./Glottal/Audio'):
    shutil.rmtree('./Glottal/Audio')
if os.path.isdir('./Glottal/Output'):
    shutil.rmtree('./Glottal/Output')
shutil.copytree(input_path, './Glottal/Audio')
glottal = glottal_features(output_path)
if os.path.isdir('./Glottal/Audio'):
    shutil.rmtree('./Glottal/Audio')
if os.path.isdir('./Glottal/Output'):
    shutil.rmtree('./Glottal/Output')
print("Glottal features extracted and saved in respective file")

print("Preparing for Acoustic feature extraction")
if os.path.isdir('./Acoustic/Audio'):
    shutil.rmtree('./Acoustic/Audio')
shutil.copytree(input_path, './Acoustic/Audio')
acoustic = acoustic_features()
if os.path.isdir('./Acoustic/Audio'):
    shutil.rmtree('./Acoustic/Audio')
print("Acoustic features extracted and saved in respective file")

merged = pd.merge(acoustic, glottal, on="filename")

merged.to_csv("./final.csv")
