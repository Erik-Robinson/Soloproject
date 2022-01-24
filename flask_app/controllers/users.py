from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.event import Event
from flask import flash
from flask_bcrypt import Bcrypt
import re
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('/index.html')

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/')
    data = {
        "username": request.form['username'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form["password"])
    }
    id = User.save(data)
    session['user_id'] = id
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    user = User.get_by_email(request.form)
    if not user:
        flash("Invalid Email", 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(user.password,request.form['password']):
        flash("Invalid Email/Password","login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/dashboard')
def home_page():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id": session['user_id']
    }
    user = User.get_one(data)
    events = Event.get_all_with_creator()
    users = User.get_all()
    return render_template("dashboard.html", user=user, users=users,all_events=events)

@app.route('/logout')
def log_out():
    session.clear()
    return redirect('/')