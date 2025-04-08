# Game Nexus - Web Application Repository

## Overview

Game Nexus is a Flask-based web application that serves as a gaming community platform. It provides user authentication functionality and a visually appealing interface with a gaming-focused theme. The application features a purple and green color scheme with a modern, glassmorphic UI design.


## Repository Structure

The repository contains a Flask application with the following components:

- **app.py**: The main Flask application file that handles routes, authentication logic, and database interactions
- **templates/**: Directory containing HTML templates
    - **auth/**: Authentication-related templates
        - **login.html**: User login page with email and password fields
        - **register.html**: User registration page for creating new accounts
    - **home.html**: Dashboard/homepage displayed after successful login


### Prerequisites 
```sh
pip install Flask Werkzeug pymongo
```

### Flask and its Components

- **Flask**: The core web framework used to build the application
- **render_template**: Used to render HTML templates with Jinja2
- **request**: Handles HTTP requests from clients
- **redirect**: Redirects the user to a different endpoint
- **url_for**: Generates URLs for Flask routes
- **flash**: Provides flash message functionality (temporary messages between requests)
- **session**: Manages user sessions using cookies

### Security Components

- **werkzeug.security.generate_password_hash**: Creates a secure hash of passwords
- **werkzeug.security.check_password_hash**: Verifies password hashes during login

### Database Component

- **pymongo.MongoClient**: Python driver for MongoDB database

