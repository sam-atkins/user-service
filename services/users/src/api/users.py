from flask import Blueprint, jsonify, request
from sqlalchemy import exc

from src.api.models import User
from src import db

users_blueprint = Blueprint('users', __name__)


@users_blueprint.route('/users/ping', methods=['GET'])
def health_check():
    return jsonify({'status': 'success', 'message': 'ping!'})


@users_blueprint.route('/users', methods=['POST'])
def add_user():
    post_data = request.get_json()
    response_object = {'status': 'fail', 'message': 'Invalid payload.'}
    if not post_data:
        return jsonify(response_object), 400
    username = post_data.get('username')
    email = post_data.get('email')
    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            db.session.add(User(username=username, email=email))
            db.session.commit()
            response_object['status'] = 'success'
            response_object['message'] = f'{email} was added!'
            return jsonify(response_object), 201
        else:
            response_object['message'] = 'Sorry. That email already exists.'
            return jsonify(response_object), 400
    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify(response_object), 400