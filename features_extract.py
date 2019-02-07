
from python_speech_features import mfcc
from python_speech_features import delta
from sklearn import preprocessing
import numpy as np
import scipy.io.wavfile as wav
from scipy import signal
from pydub import AudioSegment
import array




#      mfcc (signal,samplerate=16000,winlen=0.025,winstep=0.01,numcep=13,
#            nfilt=26,nfft=512,lowfreq=0,highfreq=None,preemph=0.97,
#            ceplifter=22,appendEnergy=True)

      
#      delta (feat, N-> For each frame, calculate delta features based on preceding and following N frames)



# def noise_filter(audio, rate):
#   # reduce low freq noises
#   #edge frequencies in hz and no of taps length of filter
#   filter_stop_freq = 70  
#   filter_pass_freq = 100  
#   filter_order = 1001

#   nyquist_rate = rate / 2.
#   desired = (0, 0, 1, 1) #desired gain
#   bands = (0, filter_stop_freq, filter_pass_freq, nyquist_rate)
#   filter_coefs = signal.firls(filter_order, bands, desired, nyq=nyquist_rate)

#   #High Pass Filter
#   filtered_audio = signal.filtfilt(filter_coefs, [1], audio)
#   # wav.write('wavefile', rate, filtered_audio)
#   return filtered_audio


def delete_silence(audio, silence_threshold=-40.0, size=10):

	#return AudioSegment after trimming silence

# return librosa.effects.remix(audio, librosa.effects.split(audio, top_db=60,frame_length=2048, hop_length=512), align_zeros=True)
	# print(audio)
	no_silence = AudioSegment.empty()
	duration = audio.__len__()
	position = 0 # ms
	assert size > 0 # Avoid infinite loop
	for i in range(0, duration, 10):
		if audio[position:position+size].dBFS > silence_threshold and position < duration:
			no_silence = no_silence + audio[position: position + size]
			position += size
			# print(position, end="\r")
		else:
			position += size

	return no_silence


	# return librosa.effects.remix(audio, librosa.effects.split(audio, top_db=60,frame_length=2048, hop_length=512), align_zeros=True)

	# rate=audio.frame_rate

	# no_silence=AudioSegment.empty()
	# duration = len(audio)
	# position = 0 # ms
	# assert size > 0 # Avoid infinite loop
	# while audio[position:position+size].dBFS > silence_threshold and position < duration :
		# no_silence=no_silence+audio[position:position+size]
		# position += size
		# return no_silence


	# samples=no_silence.get_array_of_samples()
	# shifted_samples = np.right_shift(samples, 1)
	# shifted_samples_array= array.array(audio.array_type, shifted_samples)
	# return shifted_samples_array





def mfcc_delta(wavfile):
    (rate,audio)=wav.read(wavfile)
    # audio= noise_filter(audio,rate)
    audio=AudioSegment.from_wav(wavfile)
    audio=delete_silence(audio)
    samples=audio.get_array_of_samples()
    samples_array= array.array(audio.array_type, samples)
    audio = audio._spawn(samples_array)
    audio=np.frombuffer( audio._data,dtype=np.int16)
    # name=str('modified_{}'.format(wavfile))
    # wav.write(name,rate,audio)
    mfcc_feat=mfcc(audio,rate,numcep=13,nfft=2048)
    mfcc_feat = preprocessing.scale(mfcc_feat)
    mfcc_delta1= delta(mfcc_feat, 2)
    mfcc_delta2= delta(mfcc_delta1, 2)
    combo=np.hstack((mfcc_feat,mfcc_delta1,mfcc_delta2))
    return combo



