
from flask import Flask, render_template, redirect, url_for, request , flash , jsonify

app = Flask(__name__)
app.secret_key = 'your_super_secret_key_123'

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
            return redirect(url_for('login'))
        else :
            flash("Passwords do not match!")
            return redirect(url_for('register'))
    
    return redirect(url_for('register'))

def handle_login():
    print("g maraye maitri")


if __name__ == '__main__':
    app.run(debug=True)
