from flask import Flask
from models import db
import os

DB_FOLDER = os.path.join(os.getcwd(), 'databases')
os.makedirs(DB_FOLDER, exist_ok=True)

LANGUAGES = {
    'hindi': 'hindi.db',
    'english': 'english.db',
    'marathi': 'marathi.db'
}

def create_app_and_db(db_name):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(DB_FOLDER, db_name)}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()
        print(f"✅ Created database: {db_name}")

for lang, db_file in LANGUAGES.items():
    create_app_and_db(db_file)
