from flask import render_template, request, redirect, flash, session
from src import app
from src.models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from src.forms import *




@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
    
        username = form.username.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        email = form.email.data
        role = form.role.data


        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()

        if existing_user:
            flash("L'utilisateur avec ce username ou cet email existe déja, Veuillez choisir un autre", "error")
            return render_template("register.html", form=form)


        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password_hash=hashed_password, email=email, role=role)
        
        db.session.add(new_user)
        db.session.commit()
        
        return redirect('/')
    return render_template('register.html', form = form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        username_or_email = request.form['username_or_email']
        password = request.form['password']

        user = User.query.filter((User.username == username_or_email) | (User.email == username_or_email)).first()

        if user and check_password_hash(user.password_hash, password):
            # Logic for successful login (e.g., set session, redirect)
            return redirect('/')
        else:
            flash('Invalid credentials', 'error')
            return render_template('login.html', form = form)

    return render_template('login.html', form = form)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect('/')