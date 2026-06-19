import re
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify

app = Flask(__name__)
app.secret_key = 'your_secret_key_keep_it_safe'

# --- DATABASE SETUP ---
# In a real app, initialize your database here (e.g., SQLAlchemy)
# For now, we keep the mock list for users
users = []
# db = ... (Your database connection object goes here)

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

        if not re.match(r"^[A-Za-z0-9_]+$", username):
            flash("Username must contain only alphanumeric characters and underscores.")
            return redirect(url_for('register'))

        if len(password) < 6:
            flash("Password must be at least 6 characters long.")
            return redirect(url_for('register'))

        for user in users:
            if user['email'] == email:
                flash("Email already registered.")
                return redirect(url_for('register'))
            if user['username'] == username:
                flash("Username already taken.")
                return redirect(url_for('register'))

        users.append({
            'name': name,
            'username': username,
            'email': email,
            'password': password
        })
        flash("Registration successful. Please log in.")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        input_username = request.form.get('username')
        input_email = request.form.get('email')
        input_password = request.form.get('password')

        for user in users:
            if user['email'] == input_email and user['password'] == input_password:
                session['username'] = user['username']
                session['name'] = user['name']
                session['email'] = user['email']
                return redirect(url_for('home'))
                
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
    
    context = {
        "total_users": len(users) if len(users) > 0 else 1240,
        "active_plants": 856,
        "needs_water": 127,
        "health_issues": 42,
        "pending_tasks": 18
    }
    return render_template('dashboard.html', username=session['username'], **context)

# --- NEW API ROUTE ---
@app.route('/api/plant-data')
def get_plant_data():
    # Ensure 'db' is your actual database connection object
    # fetchall() is usually required if using standard SQL connectors
    query_result = db.execute("SELECT date, health_score FROM plant_logs").fetchall()
    
    # Format the data into a list of dictionaries for JSON compatibility
    data = [{'date': row[0], 'health_score': row[1]} for row in query_result]
    return jsonify(data)

@app.route('/plant_health')
def plant_health():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('plant_health.html', username=session['username'])

@app.route('/plant_management')
def plant_management():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('plant_management.html', username=session['username'])

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

@app.route('/logout')
def logout():
    session.clear()
    return render_template('logout.html')

if __name__ == '__main__':
    app.run(debug=True)