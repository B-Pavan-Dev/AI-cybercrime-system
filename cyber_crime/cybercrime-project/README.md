# Cyber Crime Complaint Classifier

A Flask-based web application for submitting cybercrime complaints, classifying them into categories (Fraud, Phishing, Hacking, Harassment), assigning priorities, and displaying admin dashboards.

## Features

- User registration and login
- Complaint submission with ML classification
- Complaint priority ranking
- Admin dashboard for complaint review
- SQLite database storage (`database.db`)
- Simple OTP flow for registration and password recovery (console demo)

## Project structure

- `app.py` - Flask application and web routes
- `model/train_model.py` - script for training and saving the classifier and vectorizer
- `model/model.pkl` - saved trained classifier model
- `model/vectorizer.pkl` - saved TF-IDF vectorizer
- `static/` - CSS and static assets
- `templates/` - HTML templates for login, registration, dashboard, priority, and main views
- `database.db` - SQLite database file created automatically

## Requirements

- Python 3.8+
- Flask
- scikit-learn
- pandas
- flask-mail

## Setup

1. Open a terminal in the project root.
2. Install required packages:

```powershell
pip install flask scikit-learn pandas flask-mail
```

3. If the model files are missing, generate them by running:

```powershell
python model/train_model.py
```

4. Run the app:

```powershell
python app.py
```

5. Open the browser at:

```text
http://127.0.0.1:5001
```

## Default admin login

- Username: `admin`
- Password: `admin123`

## Notes

- The application uses `database.db` and initializes tables automatically.
- OTPs are printed to the console for demo purposes. In production, replace this with a real email provider.
- Complaint categories and response text are defined in `app.py`.

## Training the model

The `model/train_model.py` script builds a simple `MultinomialNB` classifier from sample complaint text and saves:

- `model/model.pkl`
- `model/vectorizer.pkl`

Run this script if you need to regenerate the model.
