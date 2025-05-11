import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn_crfsuite import CRF, metrics
from sklearn_crfsuite.metrics import flat_classification_report

# Load dataset
df = pd.read_csv("ner_dataset.csv", encoding="latin1")

# Fill sentence IDs forward
df["Sentence #"] = df["Sentence #"].ffill()

# Drop rows where Word or Tag is NaN (fixes AttributeError)
df = df.dropna(subset=["Word", "Tag"])

# Drop POS tag (not used)
df = df[["Sentence #", "Word", "Tag"]]


# Group by sentences
class SentenceGetter:
    def __init__(self, data):
        self.grouped = data.groupby("Sentence #")[["Word", "Tag"]].apply(lambda s: list(zip(s["Word"], s["Tag"])))
        self.sentences = [s for s in self.grouped]


getter = SentenceGetter(df)
sentences = getter.sentences

# Feature extraction
def word2features(sent, i):
    word = sent[i][0]
    features = {
        'bias': 1.0,
        'word.lower()': word.lower(),
        'word[-3:]': word[-3:],
        'word[-2:]': word[-2:],
        'word.isupper()': word.isupper(),
        'word.istitle()': word.istitle(),
        'word.isdigit()': word.isdigit(),
    }
    if i > 0:
        word1 = sent[i-1][0]
        features.update({
            '-1:word.lower()': word1.lower(),
            '-1:word.istitle()': word1.istitle(),
            '-1:word.isupper()': word1.isupper(),
        })
    else:
        features['BOS'] = True  # Beginning of sentence

    if i < len(sent)-1:
        word1 = sent[i+1][0]
        features.update({
            '+1:word.lower()': word1.lower(),
            '+1:word.istitle()': word1.istitle(),
            '+1:word.isupper()': word1.isupper(),
        })
    else:
        features['EOS'] = True  # End of sentence

    return features

def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]

def sent2labels(sent):
    return [label for token, label in sent]

def sent2tokens(sent):
    return [token for token, label in sent]

# Extract features and labels
X = [sent2features(s) for s in sentences]
y = [sent2labels(s) for s in sentences]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train CRF model
crf = CRF(algorithm='lbfgs',
          c1=0.1,
          c2=0.1,
          max_iterations=100,
          all_possible_transitions=True)

crf.fit(X_train, y_train)

# Predict
y_pred = crf.predict(X_test)

# Evaluation
print(flat_classification_report(y_test, y_pred))
