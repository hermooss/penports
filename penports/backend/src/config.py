import os 
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY')
    SESSION_COOKIE_NAME = 'session.web2'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)
    SQLALCHEMY_DATABASE_URI  = f"postgresql://pentest_user:{os.environ.get('DB_PASSWORD')}@localhost/pentest_report_db"
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///pentest_report.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False