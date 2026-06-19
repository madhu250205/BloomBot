import re
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key_keep_it_safe'

# In-memory database mock (Resets when server restarts)
users = []

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

        # Validation
        if password != confirm_password:
            flash("Passwords do not match!")
            return redirect(url_for('register'))

        if not re.match(r"^[A-Za-z0-9_]+$", username):
            flash("Username must contain only alphanumeric characters and underscores.")
            return redirect(url_for('register'))

        if len(password) < 6:
            flash("Password must be at least 6 characters long.")
            return redirect(url_for('register'))

        # Check if email or username already exists
        for user in users:
            if user['email'] == email:
                flash("Email already registered.")
                return redirect(url_for('register'))
            if user['username'] == username:
                flash("Username already taken.")
                return redirect(url_for('register'))

        # Append user dictionary to mock database
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
    
    # Mock data to feed into Dashboard counters
    context = {
        "total_users": len(users) if len(users) > 0 else 1240,
        "active_plants": 856,
        "needs_water": 127,
        "health_issues": 42,
        "pending_tasks": 18
    }
    return render_template('dashboard.html', username=session['username'], **context)

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