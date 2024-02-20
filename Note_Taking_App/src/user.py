from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, User
from .validators import validate_email, validate_name, validate_password
from .jwt import generate_token
import logging
from flask import session

auth_bp = Blueprint('auth', __name__)

# Configuring the logging
logging.basicConfig(filename='logs/application.log', level=logging.INFO, format='%(asctime)s - %(message)s')


# this is the api for user registration
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not name.strip():
        logging.error('Name is required.')
        return jsonify({'message': 'Name is required.'}), 400

    if not validate_name(name):
        logging.error('Name should be between 2 and 15 characters long and contain only alphabets.')
        return jsonify({'message': 'Name should be between 2 and 15 characters long and contain only alphabets.'}), 400

    if email and not validate_email(email):
        logging.error('Invalid email address.')
        return jsonify({'message': 'Invalid email address.'}), 400

    if not password or not validate_password(password):
        logging.error('Invalid password format.')
        return jsonify({'message': 'Password must be at least 6 characters long and contain at least one uppercase letter, one lowercase letter, and one digit.'}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        logging.error('Account already exists with provided email.')
        return jsonify({'message': 'An account already exists with the provided email.'}), 409

    hashed_password = generate_password_hash(password)
    new_user = User(name=name, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    logging.info(f'User {new_user.id} registered successfully.')
    return jsonify({'message': 'User registered successfully, Please login to continue.'}), 201


# this is the api for user login
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not password:
        logging.error('Password is required.')
        return jsonify({'message': 'Password is required.'}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        logging.error('Invalid email or password.')
        return jsonify({'message': 'Invalid phone number or password.'}), 401

    session['current_user_id'] = user.id
    session['current_user_email'] = user.email

    token = generate_token(user.id)

    logging.info(f'User {user.id} has logged in.')
    return jsonify({'Message': 'Login Successfull','token': token}), 200



@auth_bp.route('/logout', methods=['POST'])
def logout():

    session.clear()

    return jsonify({'message': 'Logged out successfully.'}), 200





