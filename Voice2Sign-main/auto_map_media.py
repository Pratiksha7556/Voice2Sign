import os
from flask import Flask
from models import db, LanguageTranslation, ISLSign

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

LANGUAGES = {
    'english': 'databases/english.db',
    'hindi': 'databases/hindi.db',
    'marathi': 'databases/marathi.db',
}

def setup_db(lang_key):
    db_path = LANGUAGES[lang_key]
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    
    # Initialize SQLAlchemy AFTER setting URI
    db.init_app(app)

    # Everything DB-related inside the context
    with app.app_context():
        db.create_all()

        media_path = os.path.join('static', 'media', lang_key)
        if not os.path.exists(media_path):
            print(f"[!] Media folder not found for {lang_key}")
            return

        media_files = os.listdir(media_path)
        words = {os.path.splitext(f)[0] for f in media_files if f.endswith(('.jpg', '.mp4'))}

        for word in words:
            # Create or fetch translation
            translation = LanguageTranslation.query.filter_by(
                lang_code=lang_key[:2], text_content=word
            ).first()

            if not translation:
                translation = LanguageTranslation(
                    lang_code=lang_key[:2],
                    text_content=word
                )
                db.session.add(translation)
                db.session.commit()

            # Check for existing ISLSign
            existing_sign = ISLSign.query.filter_by(translation_id=translation.id).first()
            if not existing_sign:
                image_path = f"media/{lang_key}/{word}.jpg"
                video_path = f"media/{lang_key}/{word}.mp4"

                sign = ISLSign(
                    translation_id=translation.id,
                    image_path=image_path if os.path.exists(f"static/{image_path}") else None,
                    video_path=video_path if os.path.exists(f"static/{video_path}") else None,
                    description=f"{word} in ISL"
                )
                db.session.add(sign)

        db.session.commit()
        print(f"[✓] Media mapped for {lang_key}")

if __name__ == '__main__':
    for lang in LANGUAGES:
        setup_db(lang)
