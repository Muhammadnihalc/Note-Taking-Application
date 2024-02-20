import jwt
from flask import current_app, request, jsonify, session
from functools import wraps
from .models import User
import logging
from datetime import datetime, timedelta

def generate_token(user_id):
    # Seting token expiry time to 24 hours from now
    expiry_time = datetime.utcnow() + timedelta(hours=24)
    token_data = {
        'user_id': user_id,
        'exp': expiry_time
    }
    token = jwt.encode(token_data, current_app.config['SECRET_KEY'], algorithm='HS256')
    return token


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]

        if not token:
            logging.error('Token is missing.')
            return jsonify({'message': 'Token is missing.'}), 401

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user_id = data['user_id']
            current_user = User.query.get(current_user_id)
        except jwt.ExpiredSignatureError:
            logging.error('Token has expired.')
            return jsonify({'message': 'Token has expired.'}), 401
        except jwt.InvalidTokenError:
            logging.error('Token is invalid.')
            return jsonify({'message': 'Token is invalid.'}), 401

        # Checking if the user ID from the token matches the currently logged-in user
        if current_user_id != session.get('current_user_id'):
            logging.error('Token does not correspond to the current user.')
            return jsonify({'message': 'Token does not correspond to the current user.'}), 401

        request.current_user = current_user
        return f(*args, **kwargs)

    return decorated


