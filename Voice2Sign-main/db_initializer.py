from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Folder to store databases
DB_FOLDER = os.path.join(os.getcwd(), 'databases')
os.makedirs(DB_FOLDER, exist_ok=True)

# List of language codes and DB names
LANGUAGES = {
    'hindi': 'hindi.db',
    'english': 'english.db',
    'marathi': 'marathi.db'
}

def create_app_and_db(db_name):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(DB_FOLDER, db_name)}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)

    class LanguageContent(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        lang_code = db.Column(db.String(10), nullable=False)
        text_content = db.Column(db.String(200), nullable=False)

    class ISLSign(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        content_id = db.Column(db.Integer, db.ForeignKey('language_content.id'), nullable=False)
        video_path = db.Column(db.String(200))
        description = db.Column(db.String(200))
        content = db.relationship('LanguageContent', backref='signs')

    with app.app_context():
        db.create_all()
        print(f"✅ Created database: {db_name}")

# Create DBs
for lang, db_file in LANGUAGES.items():
    create_app_and_db(db_file)
