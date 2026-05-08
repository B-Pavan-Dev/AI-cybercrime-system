from flask import Flask, render_template, request, jsonify, render_template_string
import pickle
import sqlite3
from datetime import datetime
from flask import session, redirect, url_for
import os

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))
app.secret_key = "secret123"
def extract_keywords(text):
    keywords = []

    important_words = ["bank", "money", "otp", "link", "call", "hacked", "threat"]

    for word in important_words:
        if word in text.lower():
            keywords.append(word)

    return keywords
# Load model - with error handling
try:
    model = pickle.load(open("model/model.pkl", "rb"))
    vectorizer = pickle.load(open("model/vectorizer.pkl", "rb"))
except Exception as e:
    print(f"Error loading model: {e}")
    model = None
    vectorizer = None

# Database setup
def init_db():
    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        # Create Users Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT,
                role TEXT,
                email TEXT,
                phone TEXT
            )
        ''')

        # Add columns if they don't exist (for existing databases)
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN email TEXT")
        except sqlite3.OperationalError:
            pass  # Column already exists
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN phone TEXT")
        except sqlite3.OperationalError:
            pass  # Column already exists

        # Create Complaints Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS complaints (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                text TEXT,
                category TEXT,
                priority TEXT,
                date TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')

        # Insert Default Admin (only if not exists)
        try:
            cursor.execute(
                "INSERT INTO users (username, password, role, email, phone) VALUES (?, ?, ?, ?, ?)",
                ("admin", "admin123", "admin", "admin@example.com", "1234567890")
            )
        except sqlite3.IntegrityError:
            # Update existing admin with email and phone if missing
            cursor.execute(
                "UPDATE users SET email = 'admin@example.com', phone = '1234567890' WHERE username = 'admin' AND (email IS NULL OR phone IS NULL)"
            )

        conn.commit()
        conn.close()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {e}")

init_db()

def get_priority(category):
    if category in ["Fraud", "Hacking"]:
        return "High"
    elif category == "Phishing":
        return "Medium"
    else:
        return "Low"

def generate_response(category):
    responses = {
        "Fraud": {
            "problem": "Your complaint indicates a financial fraud incident.",
            "immediate": [
                "Contact your bank immediately",
                "Block your card/account",
                "Check recent transactions"
            ],
            "next_steps": [
                "Report on National Cyber Crime Portal",
                "File FIR if amount is high"
            ],
            "prevention": [
                "Never share OTP or PIN",
                "Avoid unknown calls and links"
            ]
        },

        "Phishing": {
            "problem": "This appears to be a phishing attempt.",
            "immediate": [
                "Do not click the link again",
                "Change your passwords immediately"
            ],
            "next_steps": [
                "Enable 2-factor authentication",
                "Report the phishing website"
            ],
            "prevention": [
                "Check URLs carefully",
                "Avoid suspicious emails"
            ]
        },

        "Hacking": {
            "problem": "Your account seems to be compromised (hacked).",
            "immediate": [
                "Change all passwords immediately",
                "Logout from all devices"
            ],
            "next_steps": [
                "Enable 2-factor authentication",
                "Scan your device for malware"
            ],
            "prevention": [
                "Use strong passwords",
                "Avoid public Wi-Fi for sensitive logins"
            ]
        },

        "Harassment": {
            "problem": "You are experiencing online harassment.",
            "immediate": [
                "Block the user",
                "Save evidence (screenshots)"
            ],
            "next_steps": [
                "Report on platform",
                "File complaint if serious"
            ],
            "prevention": [
                "Do not share personal info",
                "Use privacy settings"
            ]
        }
    }

    return responses.get(category)
@app.route("/")
def home():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")
    if session.get("role") != "admin":
        return "Access Denied"

    conn = sqlite3.connect("database.db")
    rows = conn.execute("""
        SELECT c.id, c.user_id, u.username, u.email, c.text, c.category, c.priority, c.date
        FROM complaints c
        JOIN users u ON c.user_id = u.id
    """).fetchall()
    conn.close()

    priorities = {"High": [], "Medium": [], "Low": []}
    for row in rows:
        priority = row[6] if row[6] else "Low"
        if priority not in priorities:
            priorities[priority] = []
        priorities[priority].append(row)

    counts = {key: len(value) for key, value in priorities.items()}
    counts["Total"] = len(rows)

    return render_template(
        "dashboard.html",
        data=rows,
        priorities=priorities,
        counts=counts
    )

def extract_keywords(text):
    important_words = ["bank", "money", "otp", "link", "call", "hacked", "threat"]
    return [word for word in important_words if word in text.lower()]


def get_priority(category, text):
    text = text.lower()

    if category == "Fraud":
        return "High"
    elif category == "Hacking":
        return "High"
    elif category == "Phishing":
        return "Medium"
    elif category == "Harassment":
        if "threat" in text:
            return "Medium"
        return "Low"
    return "Low"


def generate_response(category):
    responses = {

        "Fraud": {
            "problem": "Your complaint indicates a financial fraud incident.",
            "immediate": [
                "Contact your bank immediately",
                "Block your card/account",
                "Check recent transactions"
            ],
            "next_steps": [
                "Report on cybercrime portal",
                "File FIR if amount is high"
            ],
            "prevention": [
                "Never share OTP or PIN",
                "Avoid unknown calls and links"
            ]
        },

        "Phishing": {
            "problem": "This appears to be a phishing attempt.",
            "immediate": [
                "Do not click suspicious links",
                "Change your passwords immediately"
            ],
            "next_steps": [
                "Enable 2-factor authentication",
                "Report the phishing website"
            ],
            "prevention": [
                "Check URLs carefully",
                "Avoid suspicious emails"
            ]
        },

        "Hacking": {
            "problem": "Your account seems to be compromised (hacked).",
            "immediate": [
                "Change all passwords immediately",
                "Logout from all devices"
            ],
            "next_steps": [
                "Enable 2-factor authentication",
                "Scan your device for malware"
            ],
            "prevention": [
                "Use strong passwords",
                "Avoid public Wi-Fi"
            ]
        },

        "Harassment": {
            "problem": "You are receiving suspicious or unwanted calls.",
            "immediate": [
                "Do not answer unknown numbers",
                "Block the suspicious numbers"
            ],
            "next_steps": [
                "Report the number as spam",
                "Contact your telecom provider if needed"
            ],
            "prevention": [
                "Do not share personal information",
                "Enable spam filters"
            ]
        }
    }

    # ✅ fallback to avoid crash
    return responses.get(category, {
        "problem": "Unable to classify complaint clearly.",
        "immediate": ["Provide more details"],
        "next_steps": ["Try submitting again"],
        "prevention": ["Stay cautious online"]
    })
@app.route("/submit", methods=["POST"])
def submit():
    try:
        if "user_id" not in session:
            return jsonify({"error": "Unauthorized"}), 401

        text = request.form["complaint"]

        # 🔹 Prediction
        X = vectorizer.transform([text])
        category = model.predict(X)[0]

        # 🔹 Confidence
        probs = model.predict_proba(X)
        confidence = round(max(probs[0]) * 100, 2)

        # 🔹 Keywords
        keywords = extract_keywords(text)

        # 🔥 Rule-based correction
        text_lower = text.lower()
        if "call" in text_lower or "unknown number" in text_lower:
            if "bank" not in text_lower and "money" not in text_lower:
                category = "Harassment"

        # 🔹 Debug
        print("INPUT:", text)
        print("CATEGORY:", category)
        print("CONFIDENCE:", confidence)
        print("KEYWORDS:", keywords)

        # 🔹 Priority
        priority = get_priority(category, text)

        # 🔹 Response
        response_data = generate_response(category)

        # 🔹 Store in DB
        conn = sqlite3.connect("database.db")
        conn.execute(
            "INSERT INTO complaints (user_id, text, category, priority, date) VALUES (?, ?, ?, ?, ?)",
            (session["user_id"], text, category, priority, str(datetime.now()))
        )
        conn.commit()
        conn.close()

        # 🔥 FINAL RESPONSE
        return jsonify({
            "category": category,
            "priority": priority,
            "confidence": confidence,
            "keywords": keywords,
            "response": response_data
        })

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": "Server error"})

@app.route("/login", methods=["GET", "POST"])
def login():
    message = request.args.get("message")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        user = conn.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        ).fetchone()
        conn.close()

        if user:
            session["user_id"] = user[0]
            session["role"] = user[3]
            if user[3] == "admin":
                return redirect("/dashboard")
            else:
                return redirect("/")
        else:
            return render_template("login.html", message="Invalid username or password", username=username)

    return render_template("login.html", message=message)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/send_otp", methods=["POST"])
def send_otp():
    email = request.form["email"]

    conn = sqlite3.connect("database.db")
    user = conn.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
    conn.close()
    if not user:
        return render_template("login.html", message="Email not registered", email=email)

    import random
    otp = str(random.randint(100000, 999999))
    session['otp'] = otp
    session['email'] = email
    print(f"OTP for {email}: {otp}")  # In production, send email
    return render_template("login.html", message="OTP sent to your email (check console for demo)", email=email)

@app.route("/send_register_otp", methods=["POST"])
def send_register_otp():
    email = request.form["email"]

    conn = sqlite3.connect("database.db")
    existing = conn.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
    conn.close()
    if existing:
        return jsonify({"success": False, "message": "Email already registered"})

    import random
    otp = str(random.randint(100000, 999999))
    session['register_otp'] = otp
    session['register_email'] = email
    print(f"Registration OTP for {email}: {otp}")  # In production, send email
    return jsonify({"success": True, "message": "OTP sent to your email (check console for demo)", "otp": otp})
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]
        email = request.form["email"]
        phone = request.form["phone"]
        otp = request.form["otp"]

        if session.get('register_otp') != otp or session.get('register_email') != email:
            return render_template(
                "register.html",
                register_message="Invalid or missing registration OTP",
                username=username,
                email=email,
                phone=phone,
                role=role
            )

        conn = sqlite3.connect("database.db")
        existing_username = conn.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
        existing_email = conn.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
        if existing_username or existing_email:
            conn.close()
            return render_template(
                "register.html",
                register_message="Username or email already exists",
                username=username,
                email=email,
                phone=phone,
                role=role
            )

        conn.execute("INSERT INTO users (username, password, role, email, phone) VALUES (?, ?, ?, ?, ?)",
                     (username, password, role, email, phone))
        conn.commit()
        conn.close()

        session.pop('register_otp', None)
        session.pop('register_email', None)

        return redirect("/login?message=Registration successful. Please login.")

    return render_template("register.html")

@app.route("/hello")
def hello():
    return "Hello World"

@app.route("/test")
def test():
    return jsonify({
        "message": "Flask app is running",
        "model_loaded": model is not None,
        "vectorizer_loaded": vectorizer is not None
    })

if __name__ == "__main__":
    print("Starting Flask app on http://127.0.0.1:5001")
    app.run(debug=True, port=5001)
    
    
    
from flask_mail import Mail, Message
import random

app.secret_key = "secret123"

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your_app_password'

@app.route("/priority")
def priority():
    if "role" not in session or session["role"] != "admin":
        return "Access Denied"

    conn = sqlite3.connect("database.db")

    data = conn.execute("""
        SELECT id, text, category, priority, date
        FROM complaints
        ORDER BY 
            CASE 
                WHEN priority = 'High' THEN 1
                WHEN priority = 'Medium' THEN 2
                ELSE 3
            END
    """).fetchall()

    conn.close()

    return render_template("priority.html", data=data)