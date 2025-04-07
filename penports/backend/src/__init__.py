from flask import Flask
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object('src.config.Config')

from src.models import db
from src.routes import *

migrate = Migrate(app, db)


with app.app_context():

    db.create_all()
    print("Creating all tables...")

