import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from matplotlib import*
import matplotlib.pyplot as plt
from matplotlib import cm 
from scipy import stats
from sklearn.decomposition import PCA as sklearnPCA
import seaborn
import io
from sklearn.decomposition import PCA



def pca_ext(acoustic, op_path='.'):
    filename = acoustic['filename'].tolist()
    d1 = acoustic.drop(['filename'], axis=1)
    
    df1=d1.replace(np.nan,0,regex=True)
    
    X_std=StandardScaler().fit_transform(df1)
    
    mean_vec=np.mean(X_std,axis=0)
    cov_mat=(X_std-mean_vec).T.dot((X_std-mean_vec)/(X_std.shape[0]-1))
    
    cov_mat=np.cov(X_std.T)
    eig_vals,eig_vect=np.linalg.eig(cov_mat)

    eig_pairs=[(np.abs(eig_vals[i],eig_vect[1,i]) for i in range(len(eig_vals)))]

    pca=PCA(n_components=30)
    pca.fit_transform(X_std)

    X_pca=pca.transform(X_std)

    
    a = numpy.asarray(X_pca)
    column_names = ['PCA' + str(x) for x in range(30)]
    pca_df = pd.DataFrame(data=a, columns=column_names)
    pca_df['filename'] = filename
    pca_df.to_csv(op_path + '/PCA.csv')
    return pca_df