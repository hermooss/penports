from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from src.routes import init_routes



db = SQLAlchemy()

def create_app(config_class='src.config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)

    init_routes(app)
    with app.app_context():
        db.create_all()

    return app