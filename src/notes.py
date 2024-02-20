from flask import Blueprint, request, jsonify, session
from .models import db, Note, User
from .jwt import token_required
from .validators import validate_note_title, validate_note_text
from datetime import datetime

notes_bp = Blueprint('notes', __name__)

# this is the api for creating notes
@notes_bp.route('/notes/create', methods=['POST'])
@token_required
def create_note():
    data = request.json
    note_title = data.get('noteTitle')
    note_text = data.get('noteText')

    # Validating
    if not note_title:
        return jsonify({'message': 'Note title is required.'}), 400

    if not validate_note_title(note_title):
        return jsonify({'message': 'Note title should be between 1 and 15 characters long and contain only alphabets.'}), 400

    if not note_text:
        return jsonify({'message': 'Note text is required.'}), 400

    if not validate_note_text(note_text):
        return jsonify({'message': 'Note text contains invalid content.'}), 400

    # fetching the current user id from session
    current_user_id = session.get('current_user_id')

    # Creating note
    new_note = Note(
        note_title=note_title,
        note_text=note_text,
        note_admin=current_user_id,
        note_access=str(current_user_id),
        time_created=datetime.now(),
        last_updated_time=datetime.now(),
        last_updated_by=current_user_id
    )

    db.session.add(new_note)
    db.session.commit()

    return jsonify({'message': 'Note created successfully.'}), 201

# api for fetching the note details
@notes_bp.route('/notes/<int:id>', methods=['GET'])
@token_required
def get_note(id):
    current_user_id = session.get('current_user_id')

    note = Note.query.get(id)

    if not note:
        return jsonify({'message': 'Note does not exist.'}), 404

    if str(current_user_id) not in note.note_access.split(','):
        return jsonify({'message': 'You do not have access to this note.'}), 403

    return jsonify({
        'noteTitle': note.note_title,
        'noteText': note.note_text,
        'time_created': note.time_created
    }), 200


# api for sharing the notes with other users
@notes_bp.route('/notes/share', methods=['POST'])
@token_required
def share_note():
    data = request.json
    
    if not data:
        return jsonify({'message': 'Please enter required data like noteid and email of the user you want to share.'}), 400

    note_id = data.get('noteid')
    user_email = data.get('email')

    if not note_id:
        return jsonify({'message': 'Please enter the noteid you want to share.'}), 400

    if not user_email:
        return jsonify({'message': 'Please enter the email of the user you want to share the note with.'}), 400

    current_user_id = session.get('current_user_id')

    note = Note.query.get(note_id)

    if not note:
        return jsonify({'message': 'Incorrect note id or note does not exist.'}), 404

    if note.note_admin != current_user_id:
        return jsonify({'message': 'You are not authorized to share this note.'}), 403

    user = User.query.filter_by(email=user_email).first()
    if not user:
        return jsonify({'message': 'User with provided email does not exist.'}), 404

    note_access_user_ids = note.note_access.split(',') if note.note_access else []
    if user.id not in note_access_user_ids:
        note_access_user_ids.append(str(user.id))
        note.note_access = ','.join(note_access_user_ids)

    db.session.commit()

    return jsonify({'message': 'Note shared successfully.'}), 200

# api for updating the note
@notes_bp.route('/notes/<int:id>', methods=['PUT'])
@token_required
def update_note(id):
    data = request.json
    new_note_text = data.get('noteText')

    current_user_id = session.get('current_user_id')

    note = Note.query.get(id)

    if not note:
        return jsonify({'message': 'Incorrect note id or note does not exist.'}), 404

    if str(current_user_id) not in note.note_access.split(','):
        return jsonify({'message': 'You do not have access to update this note.'}), 403

    note.note_text = new_note_text
    note.last_updated_time = datetime.now()
    note.last_updated_by = current_user_id

    db.session.commit()

    return jsonify({'message': 'Note updated successfully.'}), 200


# api to track the note updation details
@notes_bp.route('/notes/version-history/<int:id>', methods=['GET'])
@token_required
def get_version_history(id):
    current_user_id = session.get('current_user_id')

    note = Note.query.get(id)

    if not note:
        return jsonify({'message': 'Note ID does not exist.'}), 404

    if str(current_user_id) not in note.note_access.split(','):
        return jsonify({'message': 'You do not have permission to view version history of this note.'}), 403

    # get the user who last updated the note
    last_updated_user = User.query.get(note.last_updated_by)

    if not last_updated_user:
        last_updated_by = 'Unknown'  # Default value if user not found
    else:
        last_updated_by = last_updated_user.name

    version_history = {
        'last_updated_time': note.last_updated_time,
        'last_updated_by': last_updated_by,
        'note_text': note.note_text
    }

    return jsonify(version_history), 200


# api for deleting the specific note only the user who created can delete it
@notes_bp.route('/deletenote', methods=['DELETE'])
@token_required
def delete_note():
    note_id = request.json.get('noteid')
    current_user_id = session.get('current_user_id')

    note = Note.query.filter_by(id=note_id).first()

    if not note:
        return jsonify({'message': 'Note ID does not exist.'}), 404

    if note.note_admin != current_user_id:
        return jsonify({'message': 'You do not have permission to delete this note.'}), 403

    db.session.delete(note)
    db.session.commit()

    return jsonify({'message': 'Note successfully deleted.'}), 200




