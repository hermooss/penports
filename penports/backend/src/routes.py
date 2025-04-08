from flask import render_template, request, redirect, flash, session, url_for, send_from_directory, send_file
from src import app
from src.models import db, User, Report
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from src.forms import *
from datetime import datetime
import os

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc', 'txt'}

def allowed_file(filename):
    """ Vérifier si l'extension du fichier est autorisée """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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

        if password==confirm_password:
        
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, password_hash=hashed_password, email=email, role=role)
        
            db.session.add(new_user)
            db.session.commit()
        else:
            flash("Les deux mots de passe ne sont pas identique", "error")
            return render_template("register.html", form=form)

        
        return redirect('/')
    return render_template('register.html', form = form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        username_or_email = form.username_or_email.data
        password = form.password.data

        user = User.query.filter((User.email == username_or_email) |(User.username == username_or_email) | (User.email == username_or_email)).first()

        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect('/home')
        else:
            flash('Invalid credentials', 'error')
            return render_template('login.html', form = form)

    return render_template('login.html', form = form)




@app.route("/home")
def home():
    if 'user_id' not in session:
        flash("Veuillez vous connecter.", "warning")
        return redirect(url_for('login'))

    user = User.query.filter(User.id == session['user_id']).first()
    

    if user.role == 'pentester':
        return redirect(url_for('pentester'))
    elif user.role == 'client':
        return redirect(url_for('client'))
    else:
        flash("Rôle inconnu", "error")
        return redirect(url_for('logout'))


@app.route('/home/pentester',methods=['GET', 'POST'] )
def pentester():
    form = ReportUploadForm()
    if 'user_id' not in session :
        flash("Accès réservé aux pentesters", "error")
        return redirect(url_for('login'))
    
    user = User.query.filter(User.id == session['user_id']).first()

    reports = Report.query.filter_by(owner_id=user.id).all()



    if request.method == 'POST' and form.validate_on_submit():
        if 'report' not in request.files:
            flash("aucun fichier selecionné", "error")
            return redirect(request.url)
        
        file = request.files['report']
        emails = form.allowed_emails.data
        email_list = [email.strip() for email in emails.split("\n") if email.strip()]

        if file and allowed_file(file.filename):

                valid_users = User.query.filter(User.email.in_(email_list)).all()
                filename = secure_filename(form.report_name.data)
            
                filename = f"{user.id}_{ datetime.utcnow().strftime('%Y%m%d%H%M%S') }_{filename}"

                file.save(os.path.join(UPLOAD_FOLDER, filename))

                new_report = Report(
                    title = form.report_name.data,
                    file_path = f"uploads/{filename}",
                    description = form.description.data,
                    owner_id = user.id
                    
                )



                new_report.allowed_users = valid_users

                db.session.add(new_report)
                db.session.commit()

                flash("Rapport téléchargé avec succès", "success")
                return redirect(url_for('pentester'))

    return render_template('pentester_home.html', user = user, form=form, reports = reports )





@app.route('/uploads/<file_title>')
def downloadfile(file_title):
     # Serve the file
    report = Report.query.filter(Report.title == file_title).first()
    file_path = report.file_path
    file_name = os.path.basename(file_path)
    file_directory = os.path.dirname(file_path)
    if os.path.exists(file_path):
        print("file dowloaded")
        response = send_file(f"../{file_path}")
        return response
    
    # If the file is not found
    flash("File not found", "error")
    return redirect(url_for('home'))








@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect('/')