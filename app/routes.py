from flask import Blueprint, render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .db import get_db

bp = Blueprint('main', __name__)

# HOME
@bp.route('/')
def home():
    if 'user' in session:
        return redirect('/dashboard')
    return redirect('/login')


# REGISTER
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm = request.form.get('confirm_password')

        if not username or not password or not confirm:
            flash("Please fill all fields")
            return redirect('/register')

        if len(password) < 6:
            flash("Password must be at least 6 characters")
            return redirect('/register')

        if password != confirm:
            flash("Passwords do not match")
            return redirect('/register')

        db = get_db()
        try:
            db.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, generate_password_hash(password))
            )
            db.commit()
            flash("Account created! Please login.")
            return redirect('/login')
        except:
            flash("Username already exists!")
            return redirect('/register')

    return render_template('register.html')


# LOGIN
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # debug (optional)
        print("USERNAME:", username)
        print("PASSWORD:", password)

        if not username or not password:
            flash("Please fill all fields")
            return redirect('/login')

        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE username=?",
            (username,)
        ).fetchone()

        if user and check_password_hash(user['password'], password):
            session['user'] = username
            return redirect('/dashboard')
        else:
            flash("Invalid username or password")
            return redirect('/login')

    return render_template('login.html')


# DASHBOARD
@bp.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')
    return render_template('dashboard.html', user=session['user'])


# LOGOUT
@bp.route('/logout')
def logout():
    session.clear()
    return redirect('/login')