import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle
import os

# Load dataset
df = pd.read_csv("cybercrime_final_dataset.csv")

# Features and labels
X_text = df["text"]
y = df["label"]

# TF-IDF Vectorization
vectorizer = TfidfVectorizer(stop_words='english')

X = vectorizer.fit_transform(X_text)

# Train Model
model = MultinomialNB()
model.fit(X, y)

# Create model folder if not exists
os.makedirs("model", exist_ok=True)

# Save model and vectorizer
pickle.dump(model, open("model/model.pkl", "wb"))
pickle.dump(vectorizer, open("model/vectorizer.pkl", "wb"))

print("Model trained and saved successfully!")
