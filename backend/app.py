from flask import Flask, request
import hashlib

app = Flask(__name__)

@app.route('/')
def index():
    return "Flask backend is running. Use /submit with POST."


@app.route('/submit', methods=['POST'])
def submit():
    action = request.form.get('action')  # Use 'action' instead of 'site'
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        return "Missing email or password", 400

    # Hash the password
    hashed = hashlib.sha256(password.encode()).hexdigest()

    if action == "signup":
        name = request.form.get('name')
        if not name:
            return "Missing name for signup", 400

        # Check if the email already exists (for signup)
        with open("login_info.txt", "r") as f:
            lines = f.readlines()
            for line in lines:
                if email in line:
                    return "Email already exists", 400
        
        # Write the new signup info to the file
        with open("login_info.txt", "a") as f:
            f.write(f"SignUp,{name},{email},{hashed}\n")
        return "Signed up successfully!"

    elif action == "login":
        user_found = False
        with open("login_info.txt", "r") as f:
            lines = f.readlines()
            for line in lines:
                # Check if email exists and password matches
                if email in line:
                    stored_action, stored_name, stored_email, stored_password = line.strip().split(',')
                    if stored_email == email and stored_password == hashed:
                        user_found = True
                        break
        
        if user_found:
            return "Logged in successfully!"
        else:
            return "Invalid email or password", 400

    return "Unknown action", 400

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, jsonify, render_template, request
from models import db, LanguageContent, ISLSign


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///isl.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/isl/<lang_code>/<text>', methods=['GET'])
def get_sign(lang_code, text):
    entry = LanguageContent.query.filter_by(lang_code=lang_code, text_content=text).first()
    if entry:
        signs = ISLSign.query.filter_by(content_id=entry.id).all()
        return jsonify([
            {
                "video_path": sign.video_path,
                "description": sign.description
            } for sign in signs
        ])
    return jsonify({"error": "Sign not found"}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)




