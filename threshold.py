from features_extract import mfcc_delta
from python_speech_features import delta
import scipy.io.wavfile as wav
import numpy as np
from sklearn.mixture import GaussianMixture
from scipy.spatial.distance import euclidean
from scipy.spatial.distance import cosine
from fastdtw import fastdtw

def euclidean_calc(a,b):
    b=np.reshape(b,-1)
    b=np.squeeze(b)
#     b=(b - np.min(b))/np.ptp(b)
    a=np.reshape(a,-1)
    a=np.squeeze(a)
#     a=(a - np.min(a))/np.ptp(a)
    row1=a.shape
    row2=b.shape
    if row1<row2:
        padded=(np.pad(a, (0,row2[0]-row1[0]), 'constant', constant_values=(0)))
        return round(euclidean(padded,b),5)/100
        
    else:
        padded=(np.pad(b, (0,row1[0]-row2[0]), 'constant', constant_values=(0)))
        return round(euclidean(a,padded),5)/100

def fastdtw_calc(a,b):
    b=np.reshape(b,-1)
    b=np.squeeze(b)
#     b=(b - np.min(b))/np.ptp(b)
    a=np.reshape(a,-1)
    a=np.squeeze(a)
#     a=(a - np.min(a))/np.ptp(a)
    row1=a.shape
    row2=b.shape
    if row1<row2:
        padded=(np.pad(a, (0,row2[0]-row1[0]), 'constant', constant_values=(0)))
        distance, path = fastdtw(padded, b, dist=euclidean)
        return distance
        
    else:
        padded=(np.pad(b, (0,row1[0]-row2[0]), 'constant', constant_values=(0)))
        distance, path = fastdtw(a, padded, dist=euclidean)
        return distance

def cosine_calc(a,b):
    b=np.reshape(b,-1)
    b=np.squeeze(b)
#     b=(b - np.min(b))/np.ptp(b)
    a=np.reshape(a,-1)
    a=np.squeeze(a)
#     a=(a - np.min(a))/np.ptp(a)
    row1=a.shape
    row2=b.shape
    if row1<row2:
        padded=(np.pad(a, (0,row2[0]-row1[0]), 'constant', constant_values=(0)))
        return round((1-cosine(padded,b)),5)
        
    else:
        padded=(np.pad(b, (0,row1[0]-row2[0]), 'constant', constant_values=(0)))
        return round((1-cosine(a,padded)),5)



def sapsan(vector3,vector1):
    SAP =np.mean([cosine(u, v) for (u, v) in zip(vector1[:-1], vector1[1:])])
    SAN = np.mean([cosine(u, v) for (u, v) in zip(vector1, vector3)])
    return SAN-SAP


def threshold(vector2,vector1):
	match=False
	result=euclidean_calc(vector2,vector1)*cosine_calc(vector2,vector1)*fastdtw_calc(vector2[:9,:9],vector1[:9,:9])
	print(result)
	out=sapsan(vector2,vector1)
	print(out)

	
	if (result>6.0 and result<9.0) or result==0:
	    match=False
	    return True
	elif(out<0.8):
	        if(result>=5.0 and result<=6.0) or (result>=10.0 and result<=9.0):
	            match=True
	            return True
	        
	else:
		match=False
		
	
	return match





