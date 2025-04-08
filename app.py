from flask import Flask, render_template, redirect, url_for, request, flash, jsonify, session

app = Flask(__name__)
app.secret_key = 'your_super_secret_key_123'

# temp
users = {
    'user@example.com': 'password123'
}

@app.route('/')
def register():
    return render_template('auth/game-register.html')

@app.route('/alert_message')
def alert_message():
    message = "Invalid username or password. Please try again!'"
    return jsonify(message=message)

@app.route('/login')
def login():
    return render_template('auth/login.html')

@app.route('/register', methods=['GET', 'POST'])
def handle_register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password == confirm_password:
            users[email] = password
            flash("Registration successful! Please log in.")
            return redirect(url_for('login'))
        else:
            flash("Passwords do not match!")
            return redirect(url_for('register'))
    
    return redirect(url_for('register'))

@app.route('/login', methods=['GET', 'POST'])
def handle_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if email in users and users[email] == password:
            session['user'] = email
            return redirect(url_for('home'))
        else:
            flash("Invalid email or password.")
            return redirect(url_for('login'))

    return render_template('auth/login.html')

@app.route('/home')
def home():
    
    if 'user' not in session:
        flash("Please log in first.")
        return redirect(url_for('login'))

    return render_template('home.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("You have been logged out.")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
