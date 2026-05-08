import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle

# Sample data
data = {
    "text": [
        # FRAUD
        "money stolen from my bank account",
        "unauthorized transaction happened in my account",
        "someone withdrew money without my permission",
        "lost money through online scam",
        "UPI fraud happened with me",
        "credit card charged without my knowledge",
        "bank account balance reduced suddenly",
        "fake payment link took my money",
        "received call asking OTP and money got deducted",
        "online shopping fraud happened",

        # PHISHING
        "got phishing email asking password",
        "received fake email from bank",
        "clicked suspicious link and entered details",
        "fake website asking login credentials",
        "email asking OTP verification looks suspicious",
        "received link for KYC update seems fake",
        "fake job email asking personal details",
        "SMS with fake link for account update",
        "fraud message asking to click link",
        "fake login page appeared",

        # HACKING
        "my facebook account hacked",
        "instagram account got hacked",
        "email account compromised",
        "someone changed my account password",
        "unauthorized login detected in my account",
        "my whatsapp account is hacked",
        "my social media account accessed by someone",
        "account logged in from unknown location",
        "hacker gained access to my system",
        "my account is not accessible anymore",

        # HARASSMENT
        "someone is threatening me online",
        "getting abusive messages repeatedly",
        "receiving unwanted calls from unknown numbers",
        "person is blackmailing me online",
        "cyber bullying happening on social media",
        "fake profile created to harass me",
        "continuous spam calls disturbing me",
        "someone sending inappropriate messages",
        "being harassed through phone calls",
        "unknown person calling me again and again"
    ],

    "label": [
        # Fraud
        "Fraud","Fraud","Fraud","Fraud","Fraud",
        "Fraud","Fraud","Fraud","Fraud","Fraud",

        # Phishing
        "Phishing","Phishing","Phishing","Phishing","Phishing",
        "Phishing","Phishing","Phishing","Phishing","Phishing",

        # Hacking
        "Hacking","Hacking","Hacking","Hacking","Hacking",
        "Hacking","Hacking","Hacking","Hacking","Hacking",

        # Harassment
        "Harassment","Harassment","Harassment","Harassment","Harassment",
        "Harassment","Harassment","Harassment","Harassment","Harassment"
    ]
}
df = pd.DataFrame(data)

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["text"])

model = MultinomialNB()
model.fit(X, df["label"])

# Save model
pickle.dump(model, open("model/model.pkl", "wb"))
pickle.dump(vectorizer, open("model/vectorizer.pkl", "wb"))