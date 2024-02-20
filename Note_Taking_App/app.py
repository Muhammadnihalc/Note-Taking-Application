from flask import Flask, jsonify
from src.models import db
from src.notes import notes_bp
from src.user import auth_bp
from src.jwt import token_required
from src.validators import validate_note_title, validate_note_text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '54abcdef'

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(notes_bp)
app.register_blueprint(auth_bp)

# Global error handler
@app.errorhandler(404)
def not_found(error):
    return jsonify({'message': 'something went wrong or url Not found.'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'message': 'Internal server error.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
