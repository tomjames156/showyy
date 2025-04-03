from flask import Blueprint, request, flash, get_flashed_messages, jsonify, request
from flask_restful import Resource, marshal_with
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User

auth = Blueprint('auth', __name__)


@auth.route('signup/', methods=['POST'])
def signup_user():
    if request.method == 'POST':
        username = request.form['username']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']

        user = User(username=username, first_name=first_name, last_name=last_name, email=email,
        password=generate_password_hash(password, method='scrypt', salt_length=16))

        db.session.add(user)
        db.session.commit()

        return "<p>Added New User</p>"


@auth.route('login/', methods=['POST'])
def login_user():
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username).first()

    if check_password_hash(user.password, password):
        return f"<p>Successfully Logged In {username}</p>"
    else:
        return "<p>Authentication Failed</p>"

