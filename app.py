
from flask import Flask, request, jsonify
import base64
import io
import scipy.io.wavfile as wav
import pickle
import hashlib
from pydub import AudioSegment
import os
import threading
from sajesh_model import db, features
import threshold
import multiprocessing as mp
from features_extract import mfcc_delta
app = Flask(__name__)
pickleFilePath = os.path.join(os.getcwd(), 'pickleFile')
# {'data':"encode base64 string",'contact_name':"asdf",'contact_number':345345}
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:0@172.17.0.2:5432/sajesh'
db.init_app(app)
cpu = mp.cpu_count()
pool = mp.Pool(cpu)


def saveToDB(data, pickleFilePath, vector):
    user_hash = hashlib.sha1("{}_{}".format(
        data['contact_name'], data['contact_number']).encode())
    pickleFilePath = os.path.join(pickleFilePath, '{}'.format(user_hash))

    with open(pickleFilePath, 'wb') as fp:
        pickle.dump(vector, fp)
    newFeatures = features(contact_name=data['contact_name'],
                           contact_number=data['contact_number'], mfcc_path=pickleFilePath)
    db.session.add(newFeatures)
    db.session.commit()


def feature_match_worker(vector, row):
    path = row.mfcc_path
    with open(path, 'rb') as f:
        file = pickle.load(f)
    match = threshold.threshold(file, vector)
    if match:
        return row
    return match


def mfcc(vector, data):
    vector = mfcc_delta(vector)

    iterator = pool.imap_unordered(feature_match_worker, zip(
        [vector] * features.query.count(), features.query))

    while True:

        try:
            match = iterator.next()
        except mp.TimeoutError:
            continue
        except StopIteration:
            break
        except:
            print("Failed feature matching")
        else:
            if match:
                pool.terminate()
                break
    pool.close()
    pool.join()

    if match:
            # already on the databse so no need to add
        return jsonify(status='Found', contact_name=match.contact_name, contact_number=match.contact_number,)

    t = threading.Thread(target=saveToDB, args=(data, pickleFilePath, vector))
    t.start()

    return jsonify(status='notFound')


@app.route('/', methods=["POST"])
def serve():
    data = request.get_json()

    a = base64.b64decode(data['data'].encode())

    stream_obj = io.BytesIO(a)
    (frame_rate, vector) = wav.read(stream_obj)
    return mfcc(vector, data)


app.run(debug=True, host='0.0.0.0', port=8000)
