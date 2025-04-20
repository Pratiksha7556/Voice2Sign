# models.py
from flask_sqlalchemy import SQLAlchemy

# Create an instance of SQLAlchemy
db = SQLAlchemy()

# User Authentication Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

# ISL Translation Model
class LanguageTranslation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lang_code = db.Column(db.String(10), nullable=False)
    text_content = db.Column(db.String(255), nullable=False, unique=True)
    isl_signs = db.relationship('ISLSign', backref='translation', lazy=True)
    
class ISLSign(db.Model):
    __tablename__ = 'isl_sign'
    __table_args__ = {'extend_existing': True}  # ✅ This line fixes the error

    id = db.Column(db.Integer, primary_key=True)
    translation_id = db.Column(db.Integer, db.ForeignKey('language_translation.id'), nullable=False)
    image_path = db.Column(db.String(255))
    video_path = db.Column(db.String(255))
    description = db.Column(db.String(255))


class LanguageContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text_content = db.Column(db.String(255), nullable=False)

class ISLSign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content_id = db.Column(db.Integer, db.ForeignKey('language_content.id'), nullable=False)
    video_path = db.Column(db.String(255))
    description = db.Column(db.String(255))

    content = db.relationship('LanguageContent', backref='signs')
