# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

class LanguageTranslation(db.Model):
    __tablename__ = 'language_translation'
    id = db.Column(db.Integer, primary_key=True)
    lang_code = db.Column(db.String(10), nullable=False)
    text_content = db.Column(db.String(255), nullable=False, unique=True)
    isl_signs = db.relationship('ISLSign', backref='translation', lazy=True)

class LanguageContent(db.Model):
    __tablename__ = 'language_content'
    id = db.Column(db.Integer, primary_key=True)
    text_content = db.Column(db.String(255), nullable=False)
    signs = db.relationship('ISLSign', backref='content', lazy=True)

class ISLSign(db.Model):
    __tablename__ = 'isl_sign'
    id = db.Column(db.Integer, primary_key=True)
    translation_id = db.Column(db.Integer, db.ForeignKey('language_translation.id'), nullable=True)
    content_id = db.Column(db.Integer, db.ForeignKey('language_content.id'), nullable=True)
    video_path = db.Column(db.String(255))
    image_path = db.Column(db.String(255))
    description = db.Column(db.String(255))
