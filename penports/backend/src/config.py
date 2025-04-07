import os 

class Config:

    SQLALCHEMY_DATABASE_URI  = f"postgresql://pentest_user:{os.environ.get('DB_PASSWORD')}@localhost/pentest_report_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

