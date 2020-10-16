## Dysarthric Speech Classification

The above project is an implementation of [https://doi.org/10.1016/j.specom.2019.04.003](https://doi.org/10.1016/j.specom.2019.04.003)

Note: This code is responsible only for the feature extraction part. SVM are not built yet!

## Dataset Used:

This repository used 100 random samples of Dysarthric and Non-Dysarthric speech samples each taken from TORGO Database

You can find the 100 samples in `/Data/`

Link to the database : [http://www.cs.toronto.edu/~complingweb/data/TORGO/torgo.html](http://www.cs.toronto.edu/~complingweb/data/TORGO/torgo.html)

## Requirements

- Python3
- Docker
- Matlab
- OSx / Linux

This above repository doesn't contain a list of dependencies

Majority of dependecies required are

- Docker SDK for python
- numpy
- pandas

### How to install and get started

1. Clone the repository
2. Make sure you satisfy all the requirements
3. Install the dependencies using `pip install` command
4. Run `python app.py`
5. You can find the extracted Glottal and Acoustic features in the root of the folder.

Any issues or queries feel free to add them to Github issues

Happy Open Sourcing! 🎉🥳 🤖
