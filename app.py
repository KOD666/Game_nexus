from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
import os


app = Flask(__name__)
app.secret_key = 'supersecretkey'


client = MongoClient("mongodb://localhost:27017/")
db = client['gamezone']
users_collection = db['users']


def create_user(name, email, password):
    hashed_password = generate_password_hash(password)
    users_collection.insert_one({
        'name': name,
        'email': email,
        'password': hashed_password
    })

def find_user_by_email(email):
    return users_collection.find_one({'email': email})


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = find_user_by_email(email)

        if user and check_password_hash(user['password'], password):
            session['user'] = user['name']
            session['email'] = user['email']
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password')

    return render_template('auth/login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm_password']

        if password != confirm:
            flash('Passwords do not match')
            return redirect(url_for('register'))

        if find_user_by_email(email):
            flash('Email already registered')
            return redirect(url_for('register'))

        create_user(name, email, password)
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))

    return render_template('auth/register.html')

@app.route('/home')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('home.html', username=session['user'])

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)