from flask import render_template, request, redirect
from src import app
from src.models import db, User
from werkzeug.security import generate_password_hash



@app.route('/')
def index():
    return render_template('index.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        role = request.form.get('role')
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password_hash=hashed_password, email=email, role=role)
        
        db.session.add(new_user)
        db.session.commit()
        
        return redirect('/')