import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load data from the CSV
data = pd.read_csv(r"C:\Users\Gowtham Reddy\Desktop\ePharma\model\symptoms_medicine.csv")

# Vectorize the symptoms column
vectorizer = TfidfVectorizer()
X_train = data["symptom"]  # Column containing symptoms
y_train = data["medication"]  # Column containing medications
X_train_tfidf = vectorizer.fit_transform(X_train)

# Train the model
model = RandomForestClassifier()
model.fit(X_train_tfidf, y_train)

# Save the vectorizer and model to a pickle file
with open('model/model.pkl', 'wb') as f:
    pickle.dump((vectorizer, model), f)
