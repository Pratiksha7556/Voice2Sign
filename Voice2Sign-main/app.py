from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import hashlib
from models import db, User, LanguageTranslation, ISLSign  # type: ignore

# Create Flask app instance
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users_and_isl.db'  # Base DB for users
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Mapping language code to specific DB paths
LANG_DB_PATHS = {
    'en': 'databases/english.db',
    'hi': 'databases/hindi.db',
    'mr': 'databases/marathi.db',
}

# Function to switch to the appropriate language DB
def use_language_db(lang_code):
    if lang_code not in LANG_DB_PATHS:
        raise ValueError("Unsupported language code.")

    db_path = LANG_DB_PATHS[lang_code]
    app.config['SQLALCHEMY_BINDS'] = {
        'lang_db': f"sqlite:///{db_path}"
    }

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/voice2sign')
def voice2sign():
    return render_template("voice2sign.html")

@app.route('/submit', methods=['POST'])
def submit():
    action = request.form.get('action')
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        return "Missing email or password", 400

    hashed = hashlib.sha256(password.encode()).hexdigest()

    if action == "signup":
        name = request.form.get('name')
        if not name:
            return "Missing name for signup", 400

        if User.query.filter_by(email=email).first():
            return "Email already exists", 400

        new_user = User(name=name, email=email, password=hashed)
        db.session.add(new_user)
        db.session.commit()
        return "Signed up successfully!"

    elif action == "login":
        user = User.query.filter_by(email=email).first()
        if user and user.password == hashed:
            return "Logged in successfully!"
        else:
            return "Invalid email or password", 400

    return "Unknown action", 400

# API to translate and return ISL signs
@app.route('/api/translate', methods=['POST'])
def translate():
    data = request.get_json()
    text = data.get('text', '')
    lang_code = data.get('lang', 'en')

    try:
        use_language_db(lang_code)
    except ValueError:
        return jsonify({"error": "Unsupported language"}), 400

    if not text:
        return jsonify({"error": "Text is empty"}), 400

    tokens = text.lower().strip().split()  # Simple tokenizer (space-separated)
    result = []

    for word in tokens:
        entry = LanguageTranslation.query.filter_by(lang_code=lang_code, text_content=word).first()
        if entry:
            signs = ISLSign.query.filter_by(translation_id=entry.id).all()
            for sign in signs:
                result.append({
                    "word": word,
                    "video_path": sign.video_path,
                    "description": sign.description
                })

    if not result:
        return jsonify({"error": "No ISL signs found"}), 404

    return jsonify(result)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
