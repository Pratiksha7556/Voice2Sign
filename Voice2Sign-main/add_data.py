from models import db, LanguageContent, ISLSign
from flask import Flask

def add_sample_entry(db_path, text, video, desc):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()
        content = LanguageContent(text_content=text)
        db.session.add(content)
        db.session.commit()

        sign = ISLSign(content_id=content.id, video_path=video, description=desc)
        db.session.add(sign)
        db.session.commit()
        print(f"Inserted '{text}' into {db_path}")

# Example
add_sample_entry("databases/hindi.db", "नमस्ते", "videos/namaste.mp4", "Namaste gesture")
add_sample_entry("databases/english.db", "hello", "videos/hello.mp4", "Hello sign")
add_sample_entry("databases/marathi.db", "नमस्कार", "videos/namaskar.mp4", "Greeting in Marathi")
