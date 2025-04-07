from flask import Flask 
from src.routes import init_routes
from src.models import db
from src.models import User, Report


# Initialize Flask app
app = Flask(__name__, template_folder='src/templates')


init_routes(app)


def main():
    app.run(debug=True)



