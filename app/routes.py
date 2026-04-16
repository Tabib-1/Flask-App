from flask import Blueprint, render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .db import get_db

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    if 'user' in session:
        return redirect('/dashboard')
    return redirect('/login')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm_password']

        if len(password) < 6:
            flash("Password must be at least 6 characters")
            return redirect('/register')

        if password != confirm:
            flash("Passwords do not match")
            return redirect('/register')

        db = get_db()
        try:
            db.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                       (username, generate_password_hash(password)))
            db.commit()
            flash("Account created! Please login.")
            return redirect('/login')
        except:
            flash("Username already exists!")
            return redirect('/register')

    return render_template('register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()

        if user and check_password_hash(user['password'], password):
            session['user'] = username
            return redirect('/dashboard')
        else:
            flash("Invalid username or password")

    return render_template('login.html')

@bp.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')
    return render_template('dashboard.html', user=session['user'])

@bp.route('/logout')
def logout():
    session.clear()
    return redirect('/login')