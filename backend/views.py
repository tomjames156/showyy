import datetime
import os
from flask import Blueprint, current_app, request, jsonify, flash, redirect, url_for, render_template
from flask_restful import Resource, marshal_with
from werkzeug.utils import secure_filename
from .models import Location, Portfolio, SocialLink, User
from .utils import get_file_extension
from . import db


UPLOAD_FOLDER = '/files/'
views = Blueprint('views', __name__)

@views.route("/")
def start():
    return render_template('home.html')


# @views.route("/projects/", methods=['GET', 'POST'])
# def create_get_projects():
#     if request.method == "GET":
#         projects = [project.to_dict() for project in Project.query.all()]
#         return jsonify(projects)
#     elif request.method == 'POST':
#         highlight = request.form['highlight']
#         tool_id = request.form['tool_id']
#         name = request.form['name']
#         description = request.form['description']

#         project = Project(highlight=highlight, tool_id=tool_id,
#                                  name=name, description=description)

#         db.session.add(project)
#         db.session.commit()

#         return "<p>Added New Project</p>"


# @views.route("/tools/", methods=['GET', 'POST'])
# def get_create_tools():
#     if request.method == 'GET':
#         tools = [tool.to_dict() for tool in Tool.query.all()]
#         return jsonify(tools)
#     elif request.method == 'POST':
#         name = request.form['name']

#         new_tool = Tool(name=name)

#         db.session.add(new_tool)
#         db.session.commit()

#         return "<p>Added New Tool</p>"


@views.route("/users/", methods=['GET'])
def get_users():
    users = [user.to_dict() for user in User.query.all()]
    return jsonify(users)


@views.route("/users/<int:user_id>", methods=['GET', 'PUT'])
def get_update_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if request.method == "GET":
        return jsonify(user.to_dict())
    if request.method == "PUT":
        update_fields = request.form.to_dict()

        for key, value in update_fields.items():
            if value is not None:
                setattr(user, key, value)

        db.session.commit()
        return jsonify(user.to_dict())


@views.route("/social_links/", methods=['GET', 'POST'])
def create_get_social_links():
    if request.method == "GET":
        social_links = [social_link.to_dict() for social_link in SocialLink.query.all()]
        return jsonify(social_links)
    elif request.method == 'POST':
        link_type = request.form['link_type']
        link_value = request.form['link_value']
        portfolio_id = request.form['portfolio_id']

        social_link = SocialLink(link_value=link_value, link_type=link_type,
                                 portfolio_id=portfolio_id)

        db.session.add(social_link)
        db.session.commit()

        return "<p>Added New Social Link</p>"


@views.route("/social_links/<int:social_link_id>", methods=['GET', "PUT"])
def get_update_social_links(social_link_id):
    social_link = SocialLink.query.filter_by(id=social_link_id).first()
    if request.method == "GET":
        return jsonify(social_link.to_dict())
    if request.method == 'PUT':
        update_fields = request.form.to_dict()

        for key, value in update_fields.items():
            if value is not None:
                setattr(social_link, key, value)

        db.session.commit()
        return jsonify(social_link.to_dict())

@views.route("/portfolios/", methods=['GET', 'POST'])
def get_create_portfolios():
    if request.method == 'GET':
        portfolios = [portfolio.to_dict() for portfolio in Portfolio.query.all()]
        return jsonify(portfolios)
    elif request.method == 'POST':
        role = request.form['role']
        resume = request.form['resume']
        date_created = datetime.datetime.now()
        last_updated = datetime.datetime.now()
        user_id = request.form['user_id']
        location_id = request.form['location_id']

        portfolio = Portfolio(role=role, resume=resume, date_created=date_created,
                              last_updated=last_updated, user_id=user_id, location_id=location_id)

        db.session.add(portfolio)
        db.session.commit()

        return "<p>Added New Portfolio</p>"


@views.route('portfolios/<int:portfolio_id>', methods=["GET", "PUT"])
def get_update_portfolio(portfolio_id):
    portfolio = Portfolio.query.filter_by(id=portfolio_id).first()

    if request.method == "GET":
        return jsonify(portfolio.to_dict())
    if request.method == "PUT":
        update_fields = request.form.to_dict()

        if "role" in update_fields.keys() and update_fields['role'] is not None:
            portfolio.role = update_fields['role']
        portfolio.last_updated = datetime.datetime.now(datetime.UTC)

        db.session.commit()

        return jsonify(portfolio.to_dict())


@views.route('user/profile_pic', methods=['GET', 'POST'])
def update_profile_pic():
    user = User.query.filter_by(username='tom1sin').first()

    if request.method == 'POST':
        uploaded_file = request.files['file']
        new_pic = f"{user.username}{get_file_extension(uploaded_file.filename)}"

        if uploaded_file.filename != '':
            # Remove user's existing profile pic

            if user.portfolio.profile_pic:
                os.remove(os.path.join(current_app.config['IMG_UPLOAD_FOLDER'],
                                       user.portfolio.profile_pic))

            uploaded_file.save(os.path.join(current_app.config['IMG_UPLOAD_FOLDER'],
                                            new_pic))

        user.portfolio.profile_pic = new_pic
        user.portfolio.last_updated = datetime.datetime.now(datetime.UTC)
        db.session.commit()
        return f"<p>{new_pic}</p>"
    return '''
    <!doctype html>
    <title>Upload Profile Picture</title>
    <h1>Upload Profile Picture</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file accept=".png,.jpg,.jpeg,.gif">
      <input type=submit value=Upload>
    </form>
    '''


@views.route('user/resume', methods=['GET', 'POST'])
def update_resume():
    user = User.query.filter_by(username='tom1sin').first()

    if request.method == 'POST':
        uploaded_file = request.files['file']
        new_resume = f"{user.username}{get_file_extension(uploaded_file.filename)}"

        if uploaded_file.filename != '':
            # Remove user's existing resume

            if user.portfolio.resume:
                os.remove(os.path.join(current_app.config['DOC_UPLOAD_FOLDER'],
                                            user.portfolio.resume))

            uploaded_file.save(os.path.join(current_app.config['DOC_UPLOAD_FOLDER'],
                                            new_resume))

        user.portfolio.resume = new_resume
        user.portfolio.last_updated = datetime.datetime.now(datetime.UTC)
        db.session.commit()
        return f"<p>{new_resume}</p>"
    return '''
    <!doctype html>
    <title>Upload Resume</title>
    <h1>Upload Resume</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file accept=".pdf">
      <input type=submit value=Upload>
    </form>
    '''


@views.route('locations/', methods=['GET', 'POST'])
def get_add_locations():
    if request.method == "GET":
        locations = [location.to_dict() for location in Location.query.all()]

        return jsonify(locations)
    if request.method == "POST":
        city = request.form['city']
        country = request.form['country']

        location = Location(city=city, country=country)

        db.session.add(location)
        db.session.commit()

        return "<p>Added Location</p>"


@views.route('locations/<int:location_id>', methods=["GET", "PUT"])
def get_update_location(location_id):
    location = Location.query.filter_by(id=location_id).first()
    if request.method == "GET":
        return jsonify(location.to_dict())
    if request.method == "PUT":
        update_fields = request.form.to_dict()
        for key, value in update_fields.items():
            if value is not None:
                setattr(location, key, value)

        db.session.commit()
        return jsonify(location.to_dict())

