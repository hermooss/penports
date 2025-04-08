from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, FileField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Regexp

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=150), Regexp(r'^[a-zA-Z0-9_]+$', message="Seuls les lettres, chiffres et underscores sont autorisés.")])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=100)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=6, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email(), ])
    role = SelectField('Role', choices=[('pentester', 'Pentester'), ('client', 'Client')], validators=[DataRequired()])



class LoginForm(FlaskForm):
    username_or_email = StringField('Username or Email', validators=[DataRequired(), Regexp(r'^[a-zA-Z0-9_]+$', message="Seuls les lettres, chiffres et underscores sont autorisés.")])
    password = PasswordField('Password', validators=[DataRequired()])



class ReportUploadForm(FlaskForm):
    report_name = StringField('report name', validators=[DataRequired()])
    report = FileField('Upload Report', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])
    allowed_emails = TextAreaField('Emails (newline seperated)', validators =[DataRequired()])