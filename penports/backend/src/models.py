from flask_sqlalchemy import SQLAlchemy
from enum import Enum
from sqlalchemy.dialects.postgresql import ENUM
from src import app 



class Role(Enum):
    CLIENT = 'client'
    PENTESTER = 'pentester'


db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(10), nullable=False)
    
    # Relation One-to-Many avec les rapports (l'utilisateur est l'owner)
    reports = db.relationship('Report', backref='owner', lazy=True)

class Report(db.Model):
    __tablename__ = 'reports'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # L'utilisateur propriétaire

    # Relation Many-to-Many pour les utilisateurs autorisés à voir le rapport
    allowed_users = db.relationship('User', secondary='user_report_association', backref=db.backref('accessible_reports', lazy='dynamic'))
    



user_report_association = db.Table(
    'user_report_association',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id', ondelete='CASCADE')),
    db.Column('report_id', db.Integer, db.ForeignKey('reports.id', ondelete='CASCADE'))
)