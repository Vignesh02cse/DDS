from flask import Flask, request, render_template, redirect, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Tamilveera123$@localhost/mental'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(256))  # Increase the length to 256


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/home')
def home():
    return render_template('user_patient.html')


@app.route('/dashboard')
def dashboard():
    return render_template('user_patient.html')


@app.route('/chatbot')
def chatbot():
    return redirect("http://localhost:8501")


@app.route('/faq')
def faq():
    return render_template('faq_patient.html')


@app.route('/signup', methods=['POST'])
def signup():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    if not username:
        return 'Username is required.', 400

    if not email:
        return 'Email is required.', 400

    if not password:
        return 'Password is required.', 400

    # Hash the password
    password_hash = generate_password_hash(password)

    # Create a new User instance
    user = User(username=username, email=email, password_hash=password_hash)

    # Add the user to the session
    db.session.add(user)

    # Commit the session to store the data in the database
    db.session.commit()

    return 'User signed up successfully!', 201


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username:
        return 'Username is required.', 400

    if not password:
        return 'Password is required.', 400

    user = User.query.filter_by(username=username).first()

    if not user:
        return 'User not found.', 404

    if not user.check_password(password):
        return 'Username or password is incorrect.', 400

    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.run(debug=True)
