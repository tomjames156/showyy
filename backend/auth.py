from flask import Blueprint, request, flash, get_flashed_messages, jsonify, request
from flask_restful import Resource, marshal_with
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User

auth = Blueprint('auth', __name__)


@auth.route('/users/', methods=['GET', 'POST'])
def get_users():
    if request.method == 'GET':
        users = User.query.all()
        return jsonify([user.to_dict() for user in users])
    elif request.method == 'POST':
        return "<p>Yeah</p>"
