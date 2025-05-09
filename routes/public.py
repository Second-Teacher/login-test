from flask import Blueprint, render_template, session, redirect, url_for, make_response

public_bp = Blueprint('public', __name__)

@public_bp.route('/')
def home():
    return render_template('home.html')

@public_bp.route('/login')
def login():
    if 'user' in session:
        return redirect(url_for('dashboard.dashboard'))
    return render_template('login.html')

@public_bp.route('/signup')
def signup():
    if 'user' in session:
        return redirect(url_for('dashboard.dashboard'))
    return render_template('signup.html')

@public_bp.route('/logout')
def logout():
    session.pop('user', None)
    response = make_response(redirect(url_for('public.login')))
    response.set_cookie('session', '', expires=0)
    return response