import datetime
import os
from flask import Blueprint, current_app, request, jsonify, flash, redirect, url_for, render_template
from flask_restful import Resource, marshal_with
from werkzeug.utils import secure_filename
from .models import *
from .utils import get_file_extension
from . import db


UPLOAD_FOLDER = '/files/'
views = Blueprint('views', __name__)

@views.route("/")
def start():
    return render_template('home.html')

@views.route('/about_sections/', methods=['GET', 'POST'])
def get_create_about_section():
    if request.method == "GET":
        about_sections = [about.to_dict() for about in AboutSection.query.all()]
        return jsonify(about_sections)
    elif request.method == 'POST':
        create_fields = request.json
        tools = []

        if 'tools' in create_fields.keys():
            tools = create_fields['tools']
            del create_fields['tools']

        new_about_section = AboutSection()

        for key, value in create_fields.items():
            if value is not None:
                setattr(new_about_section, key, value)

        db.session.add(new_about_section)
        db.session.commit()

        if tools:
            for tool_id in tools:
                tool = Tool.query.get(tool_id)
                new_about_section.tools.append(tool)

            db.session.commit()

        return f"<p>Added About Section for User id {new_about_section.user_id}</p>"


@views.route('/about_sections/<int:about_id>', methods=['GET', 'PUT'])
def get_update_about_section(about_id):
    about_section = AboutSection.query.get_or_404(about_id)
    if request.method == 'GET':
        return jsonify(about_section.to_dict())
    if request.method == 'PUT':
        put_fields = request.json
        tools = []

        if 'tools' in put_fields.keys():
            tools = put_fields['tools']
            del put_fields['tools']

        for key, value in put_fields.items():
            if value is not None:
                setattr(about_section, key, value)

        db.session.commit()

        if tools:
            for tool_id in tools:
                tool = Tool.query.get(tool_id)
                if tool not in about_section.tools:
                    about_section.tools.append(tool)

            db.session.commit()
        return "<p>Updated About Section</p>"


@views.route("/experiences/", methods=['GET', 'POST'])
def get_create_experiences():
    if request.method == "GET":
        experiences = [experience.to_dict() for experience in Experience.query.all()]
        return jsonify(experiences)
    elif request.method == 'POST':
        create_fields = request.json
        bullet_points = []

        if 'bullet_points' in create_fields.keys():
            bullet_points = create_fields['bullet_points']
            del create_fields['bullet_points']

        new_experience = Experience()

        if 'start_date' in create_fields.keys():
            new_experience.start_date = datetime.datetime.fromisoformat(create_fields['start_date'])
            del create_fields['start_date']

        if 'end_date' in create_fields.keys():
            new_experience.end_date = datetime.datetime.fromisoformat(create_fields['end_date'])
            del create_fields['end_date']

        for key, value in create_fields.items():
            if value is not None:
                setattr(new_experience, key, value)

        db.session.add(new_experience)
        db.session.commit()

        if bullet_points:
            for bullet_point in bullet_points:
                bullet_point = ExperienceBullet(bullet_point=bullet_point,
                                                experience_id=new_experience.id)
                db.session.add(bullet_point)

            db.session.commit()

        return "<p>Added New Experience</p>"


@views.route('/experiences/<int:experience_id>', methods=['GET', 'PUT'])
def get_update_experience(experience_id):
    experience = Experience.query.get_or_404(experience_id)
    if request.method == 'GET':
        return jsonify(experience.to_dict())
    if request.method == 'PUT':
        put_fields = request.json
        bullet_points = []

        if 'bullet_points' in put_fields.keys():
            bullet_points = put_fields['bullet_points']
            del put_fields['bullet_points']

        if 'start_date' in put_fields.keys():
            experience.start_date = datetime.datetime.fromisoformat(put_fields['start_date'])
            del put_fields['start_date']

        if 'end_date' in put_fields.keys():
            experience.end_date = datetime.datetime.fromisoformat(put_fields['end_date'])
            del put_fields['end_date']

        for key, value in put_fields.items():
            if value is not None:
                setattr(experience, key, value)

        db.session.commit()

        if bullet_points:
            for bullet_point in bullet_points:
                bullet_point = ExperienceBullet(bullet_point=bullet_point,
                                                experience_id=experience.id)
                db.session.add(bullet_point)

            db.session.commit()
        return "<p>Updated Experience</p>"


@views.route("/experience_bullets/", methods=['GET', 'POST'])
def get_create_experience_bullets():
    if request.method == "GET":
        bullet_points = [point.to_dict() for point in ExperienceBullet.query.all()]
        return jsonify(bullet_points)
    elif request.method == 'POST':
        create_fields = request.form.to_dict()

        bullet_point = ExperienceBullet(bullet_point=create_fields['bullet_point'],
                                        experience_id=create_fields['experience_id'])

        db.session.add(bullet_point)
        db.session.commit()

        return "<p>Added New Bullet Point</p>"


@views.route('/experience_bullets/<int:experience_id>', methods=['GET', 'PUT'])
def get_update_experience_bullets(experience_id):
    bullet_point = ExperienceBullet.query.get_or_404(experience_id)
    if request.method == 'GET':
        return jsonify(bullet_point.to_dict())
    if request.method == 'PUT':
        put_fields = request.form.to_dict()

        for key, value in put_fields.items():
            if value is not None:
                setattr(bullet_point, key, value)

        db.session.commit()
        return "<p>Updated Bullet Point</p>"


@views.route("/projects/", methods=['GET', 'POST'])
def get_create_projects():
    if request.method == "GET":
        projects = [project.to_dict() for project in Project.query.all()]
        return jsonify(projects)
    elif request.method == 'POST':
        create_fields = request.json

        name = create_fields['name']
        description = create_fields['description']
        user_id = create_fields['user_id']

        project = Project(name=name, description=description, user_id= user_id)

        if 'highlight' in create_fields.keys():
            setattr(project, 'highlight', create_fields['highlight'] == 'True')

        db.session.add(project)
        db.session.commit()

        if 'tools' in create_fields.keys():
            for tool_id in create_fields['tools']:
                tool = Tool.query.get(tool_id)
                project.tools.append(tool)

        db.session.commit()

        return "<p>Added New Project</p>"


@views.route('/projects/<int:project_id>', methods=['GET', 'PUT'])
def get_update_project(project_id):
    project = Project.query.get_or_404(project_id)
    if request.method == 'GET':
        return jsonify(project.to_dict())
    if request.method == 'PUT':
        put_fields = request.json

        if 'tools' in put_fields.keys():
            for tool_id in put_fields['tools']:
                tool = Tool.query.get(tool_id)

                if tool not in project.tools:
                    project.tools.append(tool)

            del put_fields['tools']

        if 'highlight' in put_fields.keys():
            setattr(project, 'highlight', put_fields['highlight'] == 'True')
            del put_fields['highlight']

        for key, value in put_fields.items():
            if value is not None:
                setattr(project, key, value)

        db.session.commit()
        return "<p>Updated Project</p>"


@views.route("/tools/", methods=['GET', 'POST'])
def get_create_tools():
    if request.method == 'GET':
        tools = [tool.to_dict() for tool in Tool.query.all()]
        return jsonify(tools)
    elif request.method == 'POST':
        name = request.form['name']

        new_tool = Tool(name=name)

        db.session.add(new_tool)
        db.session.commit()

        return "<p>Added New Tool</p>"


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


@views.route('projects/<int:project_id>/image', methods=['GET', 'POST'])
def update_project_image(project_id):
    project = Project.query.get(project_id)
    user = User.query.get(project.user_id)

    if request.method == 'POST':
        uploaded_file = request.files['file']
        new_pic = f"{user.username}-proj-{project_id}{get_file_extension(uploaded_file.filename)}"

        if uploaded_file.filename != '':
            # Remove user's existing profile pic

            if project.image:
                os.remove(os.path.join(current_app.config['IMG_UPLOAD_FOLDER'],
                                       project.image))

            uploaded_file.save(os.path.join(current_app.config['IMG_UPLOAD_FOLDER'],
                                            new_pic))

        project.image = new_pic
        db.session.commit()
        return f"<p>{new_pic}</p>"
    return f'''
    <!doctype html>
    <title>Upload Profile Picture</title>
    <h1>Upload Profile Picture</h1>
    {project.name}
    <form method=post enctype=multipart/form-data>
      <input type=file name=file accept=".png,.jpg,.jpeg,.gif">
      <input type=submit value=Upload>
    </form>
    '''

@views.route('locations/', methods=['GET', 'POST'])
def get_add_locations():
    if request.method == "GET":
        locations = [location.to_dict() for location in Location.query.all()]

        return jsonify(locations)
    if request.method == "POST":
        post_fields = request.form.to_dict()
        location = Location(city=post_fields['city'], state=post_fields['state'],
        country=post_fields[
            'country'])

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

