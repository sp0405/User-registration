from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
import re

app = Flask(__name__)
app.secret_key = "your_secret_key"

# In-memory user storage (for demo)
users = {}

# Email validation regex
email_regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'

@app.route('/')
def index():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    # Validation
    if not username or not email or not password or not confirm_password:
        flash("All fields are required!", "error")
        return redirect(url_for('index'))

    if not re.match(email_regex, email):
        flash("Invalid email format!", "error")
        return redirect(url_for('index'))

    if len(password) < 6:
        flash("Password must be at least 6 characters!", "error")
        return redirect(url_for('index'))

    if password != confirm_password:
        flash("Passwords do not match!", "error")
        return redirect(url_for('index'))

    if email in users:
        flash("Email already registered!", "error")
        return redirect(url_for('index'))

    # Save user with hashed password
    hashed_password = generate_password_hash(password)
    users[email] = {'username': username, 'password': hashed_password}

    flash("Registration successful!", "success")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
