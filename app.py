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

@app.route('/game_desc')
def game_desc():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    # Static game data
    games = [
        {
            'id': 1,
            'title': 'Cybernetic Odyssey',
            'genre': 'RPG, Open World',
            'developer': 'Quantum Studios',
            'release_date': 'March 15, 2025',
            'description': 'An immersive open-world RPG set in a dystopian future where humans and machines are increasingly integrated. Play as a customizable protagonist with unique cybernetic enhancements and navigate a complex narrative with multiple endings.',
            'rating': 4.8,
            'image_class': 'cyberpunk-game',
            'features': ['Extensive character customization', 'Dynamic weather system', 'Multiple storyline branches', 'Advanced AI companions']
        },
        {
            'id': 2,
            'title': 'Stellar Conquest',
            'genre': 'Strategy, Space Simulation',
            'developer': 'Cosmic Games',
            'release_date': 'January 5, 2025',
            'description': 'Build your interstellar empire in this grand strategy game. Manage resources, research technologies, build fleets, and engage in diplomatic relations or warfare with other species across the galaxy.',
            'rating': 4.5,
            'image_class': 'space-game',
            'features': ['Procedurally generated galaxies', 'Complex diplomatic system', 'Real-time space battles', 'Alliance and federation mechanics']
        },
        {
            'id': 3,
            'title': 'Shadow Legends',
            'genre': 'Action, Adventure',
            'developer': 'Mystic Entertainment',
            'release_date': 'April 22, 2025',
            'description': 'A dark fantasy action-adventure where you play as a legendary assassin with supernatural abilities. Master the arts of stealth, parkour, and combat as you unravel a conspiracy that threatens to plunge the world into chaos.',
            'rating': 4.7,
            'image_class': 'fantasy-game',
            'features': ['Advanced stealth mechanics', 'Dynamic day-night cycle', 'Skill progression system', 'Responsive combat system']
        }
    ]
    
    return render_template('game_desc.html', username=session['user'], games=games)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)