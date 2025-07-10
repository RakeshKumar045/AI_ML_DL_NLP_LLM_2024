import numpy as np
import pandas as pd
import pickle
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from flask import Flask,request,app,jsonify,url_for,render_template

from tensorflow.keras.models import load_model

model = load_model("my_model")


app=Flask(__name__)
# loading the model
tokenizer = pickle.load(open('tokenizer.pkl', 'rb'))
word_index = tokenizer.word_index
word2id = word_index
id2word = {}
for key, value in word2id.items():
    id2word[value] = key
# tag_2_num = {'O': 9,
#  'B-geo': 16,
#  'B-gpe': 5,
#  'B-per': 8,
#  'I-geo': 2,
#  'B-org': 3,
#  'I-org': 0,
#  'B-tim': 10,
#  'B-art': 12,
#  'I-art': 4,
#  'I-per': 11,
#  'I-gpe': 13,
#  'I-tim': 14,
#  'B-nat': 15,
#  'B-eve': 7,
#  'I-eve': 6,
#  'I-nat': 1}

tag_2_num = {'O': 0,
 'B-geo': 1,
 'B-gpe': 2,
 'B-per': 3,
 'I-geo': 4,
 'B-org': 5,
 'I-org': 6,
 'B-tim': 7,
 'B-art': 8,
 'I-art': 9,
 'I-per': 10,
 'I-gpe': 11,
 'I-tim': 12,
 'B-nat': 13,
 'B-eve': 14,
 'I-eve': 15,
 'I-nat': 16}

# tag_2_num = {'I-org': 0,
#  'I-nat': 1,
#  'I-geo': 2,
#  'B-org': 3,
#  'I-art': 4,
#  'B-gpe': 5,
#  'I-eve': 6,
#  'B-eve': 7,
#  'B-per': 8,
#  'O': 9,
#  'B-tim': 10,
#  'I-per': 11,
#  'B-art': 12,
#  'I-gpe': 13,
#  'I-tim': 14,
#  'B-nat': 15,
#  'B-geo': 16}

id2tag = {}
for key, value in tag_2_num.items():
    id2tag[value] = key
    

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict_api', methods =['POST'])
def predict__api():
    data = request.form['data']
    new_data = tokenizer.texts_to_sequences([data])
    new_data = pad_sequences(new_data, maxlen=75, padding='post', truncating='post')
    new_data = new_data.reshape((1, 75))
    
    output = model.predict(new_data)
    output = np.argmax(output, axis=2)[0]
    prediction = [int(val) for val in output]
    pred_tag_list = [id2tag[tag_id] for tag_id in prediction]
    
    result = [{"word": word, "tag": tag} for word, tag in zip(data.split(), pred_tag_list) if tag != 'O']
    result_text = " ".join([item['word'] for item in result])
    return render_template('result.html',result_text=data, result=result)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
    