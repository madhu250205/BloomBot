import os
import re
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from pymongo import MongoClient

# --- SETUP ---
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')
bcrypt = Bcrypt(app)

# Database setup
MONGO_URI = os.getenv('MONGO_URI')
client = MongoClient(MONGO_URI)
db = client['bloom_bot_db']
users_collection = db['users'] 

# --- ROUTES ---

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('home'))
    return redirect(url_for('register'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash("Passwords do not match!")
            return redirect(url_for('register'))

        # Security: Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        users_collection.insert_one({
            'name': name,
            'username': username,
            'email': email,
            'password': hashed_password
        })
        flash("Registration successful. Please log in.")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        input_email = request.form.get('email')
        input_password = request.form.get('password')

        user = users_collection.find_one({"email": input_email})
        
        if user:
            try:
                # Security: Check hashed password safely
                if bcrypt.check_password_hash(user['password'], input_password):
                    session['username'] = user['username']
                    session['name'] = user['name']
                    session['email'] = user['email']
                    return redirect(url_for('home'))
            except ValueError:
                # This catches the "Invalid salt" error from old plain-text passwords
                pass
                
        flash("Invalid credentials. Please try again.")
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('home.html', username=session['username'], name=session['name'], email=session['email'])

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    total_users_count = users_collection.count_documents({})
    
    context = {
        "total_users": total_users_count,
        "active_plants": 0,
        "needs_water": 0,
        "health_issues": 0,
        "pending_tasks": 0
    }
    return render_template('dashboard.html', username=session['username'], **context)

@app.route('/api/plant-data')
def get_plant_data():
    # Use a safety check for the collection
    if 'plant_logs' not in db.list_collection_names():
        return jsonify([])
    query_result = list(db['plant_logs'].find({}, {"_id": 0, "date": 1, "health_score": 1}))
    return jsonify(query_result)

# ... (Include your other routes like plant_health, plant_management, etc. here) ...

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/plant_health')
def plant_health():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('plant_health.html', username=session['username'])

@app.route('/plant_management')
def plant_management():
    if 'username' not in session:
        return redirect(url_for('login'))
    # Fetch plants from DB to pass to the table
    my_plants = list(db['plants'].find({'username': session['username']}))
    return render_template('plant_management.html', username=session['username'], plants=my_plants)

@app.route('/health_tracker')
def health_tracker():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('health_tracker.html', username=session['username'])

@app.route('/plant_reminder')
def plant_reminder():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('plant_reminder.html', username=session['username'])

@app.route('/watering')
def watering():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('watering.html', username=session['username'])

if __name__ == '__main__':
    app.run(debug=True)