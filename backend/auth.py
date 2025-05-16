import datetime
from flask import (Blueprint, abort, current_app, request, jsonify,
                   request, render_template, make_response)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import HTTPException
import json
import jwt
import uuid
from . import db
from .models import *
from sqlalchemy import text
from flask_jwt_extended import (create_access_token, jwt_required)

auth = Blueprint('auth', __name__)


@auth.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP error"""

    response = e.get_response()
    response.data = json.dumps({
        'code': e.code,
        'name': e.name,
        'description': e.description
    })

    response.content_type = 'application/json'
    return response


def get_current_user():
    token = request.headers.get("Authorization")

    if not token:
        abort(401, "Token is missing")
    try:
        token = token[7:]
        data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        current_user = User.query.filter_by(username=data['sub']).first()
    except Exception as e:
        abort(401, "Token is Invalid")
    
    return current_user


def check_username_exists(username):
    query = text(f"""
                    SELECT username
                    FROM user
                    WHERE username = "{username}"
                """)
    users = db.session.execute(query)

    users = [user for user in users]

    return not(users == [])


def check_email_exists(email):
    query = text(f"""
                    SELECT email
                    FROM user
                    WHERE email = "{email}"
                """)
    users = db.session.execute(query)

    users = [user for user in users]
    return not(users == [])


@auth.route('signup/', methods=['POST'])
def signup_user():
    if request.method == 'POST':
        username = request.form['username']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']

        if len(password) < 8:
            abort(404, "Password too short")

        if check_username_exists(username):
            abort(409, "Username Already Exists")

        if check_email_exists(email):
            abort(409, "Email already in use")

        #     Maybe add functionality to make sure only these are passed

        user = User(username=username, first_name=first_name, last_name=last_name, email=email,
        password=generate_password_hash(password, method='scrypt', salt_length=16),
                    public_id=str(uuid.uuid4()))

        db.session.add(user)
        db.session.commit()

        response = make_response(jsonify({"message": "Added New User"}))
        return response, 200


@auth.route('update_password/', methods=['PUT'])
@jwt_required()
def update_password():
    current_user = get_current_user()
    put_fields = request.json
    new_pass = put_fields['password']

    if len(new_pass) < 8:
        abort(400, "Password too short")

    user = User.query.get_or_404(current_user.id)
    new_pass = generate_password_hash(new_pass, method='scrypt', salt_length=16)

    setattr(user, 'password', new_pass)
    db.session.commit()

    response = make_response(jsonify({"message": "Successfully Updated Password"}))
    return response, 200


@auth.route('login/', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user:

            if check_password_hash(user.password, password):
                response = make_response(jsonify({"message": "Login successful"}))

                if not user.portfolio:
                    users_portfolio = Portfolio(user_id=user.id)
                    db.session.add(users_portfolio)

                if not user.about_section:
                    users_about_sect = AboutSection(user_id=user.id)
                    db.session.add(users_about_sect)

                if not user.services_section:
                    users_services_section = ServicesSection(user_id=user.id)
                    db.session.add(users_services_section)

                if not user.contact_section:
                    users_contact_section = ContactSection(user_id=user.id,
                                                           phone_number='000-000-0000')
                    db.session.add(users_contact_section)

                db.session.commit()

                access_token = create_access_token(identity=username, expires_delta=datetime.timedelta(days=100))
                return jsonify(access_token=access_token)
            else:
                abort(401, "Authentication Failed")
        else:
            abort(401, "Username Does Not Exist")

    return render_template('login.html')


@auth.route('verify/', methods=["POST"])
@jwt_required()
def verify_email():
    current_user = get_current_user()
    user = User.query.get_or_404(current_user.id)

    user.verified = True
    db.session.commit()

    response = make_response(jsonify({"message": "Verified User Email"}))
    return response, 200


@auth.route('update_email/', methods=["POST"])
@jwt_required()
def update_email():
    current_user = get_current_user()
    user = User.query.get_or_404(current_user.id)
    new_email = request.form['email']

    user.email = new_email
    user.verified = False

    db.session.commit()

    response = make_response(jsonify({"message": "Updated User Email"}))
    return response, 200

