import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Flask app setup
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Language-specific DB mapping
LANGUAGES = {
    'english': 'databases/english.db',
    'hindi': 'databases/hindi.db',
    'marathi': 'databases/marathi.db',
}

# Models defined inside this file to avoid redefinition issues
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
    db_path = LANGUAGES[lang_key]
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    db.engine.dispose()  # Clean previous engine binding
    db.init_app(app)

    with app.app_context():
        db.create_all()

        media_path = os.path.join('static', 'media', lang_key)
        if not os.path.exists(media_path):
            print(f"[!] Media folder missing for: {lang_key}")
            return

        words = {os.path.splitext(f)[0] for f in os.listdir(media_path)}

        for word in words:
            translation = LanguageTranslation.query.filter_by(
                lang_code=lang_key[:2],
                text_content=word
            ).first()

            if not translation:
                translation = LanguageTranslation(
                    lang_code=lang_key[:2],
                    text_content=word
                )
                db.session.add(translation)
                db.session.commit()

            image_path = f"media/{lang_key}/{word}.jpg"
            video_path = f"media/{lang_key}/{word}.mp4"

            if not ISLSign.query.filter_by(translation_id=translation.id).first():
                sign = ISLSign(
                    translation_id=translation.id,
                    image_path=image_path if os.path.exists(f"static/{image_path}") else None,
                    video_path=video_path if os.path.exists(f"static/{video_path}") else None,
                    description=f"{word} in ISL"
                )
                db.session.add(sign)

        db.session.commit()
        print(f"[✓] Mapped media for: {lang_key}")

if __name__ == '__main__':
    for lang in LANGUAGES:
        setup_db(lang)
