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

