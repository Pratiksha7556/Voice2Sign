import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Flask app setup
app = Flask(__name__)
# Set a temporary dummy DB URI to avoid init error
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///temp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy()
db.init_app(app)  # ✅ Initialize it once during app setup

# Define LANGUAGES before using it
LANGUAGES = {
    'english': 'databases/english.db',
    'hindi': 'databases/hindi.db',
    'marathi': 'databases/marathi.db',
}

# Models
class LanguageTranslation(db.Model):
    __tablename__ = 'language_translation'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    lang_code = db.Column(db.String(2), nullable=False)
    text_content = db.Column(db.String(100), nullable=False)

class ISLSign(db.Model):
    __tablename__ = 'isl_sign'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    translation_id = db.Column(db.Integer, db.ForeignKey('language_translation.id'), nullable=False)
    image_path = db.Column(db.String(255))
    video_path = db.Column(db.String(255))
    description = db.Column(db.String(255))

def setup_db(lang_key):
    # Ensure the db folder exists
    db_folder = os.path.join(os.getcwd(), 'databases')  # Use absolute path
    os.makedirs(db_folder, exist_ok=True)

    # Ensure the database file path is correct and accessible
    db_path = os.path.join(db_folder, f"{lang_key}.db")
    print(f"Using database at: {db_path}")
    
    # Configure the URI with the absolute path for each language
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    
    try:
        # Create the tables if they do not exist
        with app.app_context():
            db.create_all()

            # Set up media folder
            media_path = os.path.join('static', 'media', lang_key)
            os.makedirs(media_path, exist_ok=True)

            # List all image and video files in the media folder
            files = os.listdir(media_path)
            words = set(os.path.splitext(f)[0] for f in files if f.endswith(('.jpg', '.jpeg', '.png', '.gif', '.mp4')))

            # For each word found in the media folder, associate it with a translation
            for word in words:
                lang_code = lang_key[:2].lower()  # Take first 2 characters as language code
                translation = LanguageTranslation.query.filter_by(
                    lang_code=lang_code,
                    text_content=word
                ).first()

                if not translation:
                    translation = LanguageTranslation(lang_code=lang_code, text_content=word)
                    db.session.add(translation)
                    db.session.commit()

                image_path = None
                video_path = None

                # Check for image files
                for ext in ['.jpg', '.jpeg', '.png', '.gif']:
                    full_img_path = os.path.join(media_path, f"{word}{ext}")
                    if os.path.exists(full_img_path):
                        image_path = f"media/{lang_key}/{word}{ext}"
                        break

                # Check for video files
                vid_path = os.path.join(media_path, f"{word}.mp4")
                if os.path.exists(vid_path):
                    video_path = f"media/{lang_key}/{word}.mp4"

                # Check if the ISLSign for this word already exists
                if not ISLSign.query.filter_by(translation_id=translation.id).first():
                    sign = ISLSign(
                        translation_id=translation.id,
                        image_path=image_path,
                        video_path=video_path,
                        description=f"{word} in ISL"
                    )
                    db.session.add(sign)

            db.session.commit()
            print(f"[✓] Mapped media for: {lang_key}")

    except Exception as e:
        print(f"Error setting up database for {lang_key}: {e}")
        db.session.rollback()

if __name__ == "__main__":
    with app.app_context():
        for lang in LANGUAGES:
            setup_db(lang)
