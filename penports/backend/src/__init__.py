from flask import Flask, session
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config.from_object('src.config.Config')

@app.before_request
def make_session_permanent():
    session.permanent = True

    
csrf = CSRFProtect(app)



from src.models import db
from src.routes import *

migrate = Migrate(app, db)


with app.app_context():

    db.create_all()
    print("Creating all tables...")

