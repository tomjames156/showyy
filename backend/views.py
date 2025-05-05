import datetime
import os
from flask import (Blueprint, abort, current_app, request, jsonify, flash, redirect, url_for,
                   render_template, make_response)
from flask_restful import Resource, marshal_with
from werkzeug.utils import secure_filename
from werkzeug.exceptions import HTTPException
import json
from sqlalchemy import text
from .models import *
from .utils import get_file_extension
from hashlib import md5
from time import localtime
from . import db
from .auth import token_required


UPLOAD_FOLDER = '/files/'
views = Blueprint('views', __name__)


@views.errorhandler(HTTPException)
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


def check_user_id_exists_in_table(table, user_id):
    query = text(f"""
                    SELECT user_id
                    FROM {table}
                    WHERE user_id = "{user_id}"
                """)
    users = db.session.execute(query)

    users = [user for user in users]

    return not(users == [])


def check_tool_exists(name):
    query = text(f"""
                        SELECT name
                        FROM tool
                        WHERE name = "{name}"
                    """)
    tools = db.session.execute(query)

    tools = [tool for tool in tools]

    return not (tools == [])


def new_filename():
    prefix = md5(str(localtime()).encode('utf-8')).hexdigest()
    return f"{prefix}"


@views.route("/")
@token_required
def start(current_user):
    user = User.query.filter_by(username=current_user.username).first()

    return render_template('home.html', user=user)


@views.route("/users/", methods=['GET'])
@token_required
def get_users(current_user):

    if current_user.id == 1:
        users = [user.to_dict() for user in User.query.all()]
        return jsonify(users)
    else:
        abort(401, "Access Denied")


@views.route("/users/<int:user_id>", methods=['GET', 'PUT'])
@token_required
def get_update_user(user_id, current_user):
    user = User.query.get_or_404(user_id)

    if request.method == "GET":
        if user.id != current_user.id and current_user.id != 1:
            abort(401, "Access Denied")

        return jsonify(user.to_dict())
    if request.method == "PUT":
        if user_id != current_user.id:
            abort(403, "Unauthorised Update")
        update_fields = request.json

        for key, value in update_fields.items():
            if value is not None and key in ['first_name', 'last_name']:
                setattr(user, key, value)

        db.session.commit()

        response = make_response(jsonify({"message": "Updated User Information"}))
        return response, 200


@views.route("/portfolios/", methods=['GET', 'POST'])
@token_required
def get_create_portfolios(current_user):
    if request.method == 'GET':
        if current_user.id == 1:
            portfolios = [portfolio.to_dict() for portfolio in Portfolio.query.all()]
            return jsonify(portfolios)
        else:
            abort(401, "Access Denied")
    elif request.method == 'POST':
        create_fields = request.json
        create_fields['user_id'] = current_user.id

        if check_user_id_exists_in_table('portfolio', create_fields['user_id']):
            abort(409, description="Portfolio already exists for this user")

        portfolio = Portfolio()

        for key, value in create_fields.items():
            if value is not None and key in ['role', 'user_id', 'location_id']:
                setattr(portfolio, key, value)

        db.session.add(portfolio)
        db.session.commit()

        response = make_response(jsonify({"message": "Created New Portfolio"}))
        return response, 200


@views.route('portfolios/<int:portfolio_id>', methods=["GET", "PUT"])
@token_required
def get_update_portfolio(portfolio_id, current_user):
    portfolio = Portfolio.query.get_or_404(portfolio_id)

    if request.method == "GET":

        if portfolio.user_id != current_user.id and current_user.id != 1:
            abort(401, "Access Denied")

        return jsonify(portfolio.to_dict())
    if request.method == "PUT":
        update_fields = request.json

        if portfolio.user_id != current_user.id:
            abort(401, "Access Denied")

        for key, value in update_fields.items():
            if value is not None and key in ['role', 'location_id']:
                setattr(portfolio, key, value)
        portfolio.last_updated = datetime.datetime.now(datetime.UTC)

        db.session.commit()

        response = make_response(jsonify({"message": "Updated Portfolio"}))
        return response, 200


@views.route('user/profile_pic', methods=['GET', 'POST'])
@token_required
def update_profile_pic(current_user):
    user = User.query.filter_by(username=current_user.username).first()

    if request.method == 'POST':
        uploaded_file = request.files['file']

        new_pic = f"{new_filename()}{get_file_extension(uploaded_file.filename)}"

        # For new user without portfolio, create one
        if not user.portfolio:
            new_portfolio = Portfolio(user_id=user.id)
            db.session.add(new_portfolio)
            db.session.commit()

        if uploaded_file.filename != '':
            # Remove user's existing profile pic

            if user.portfolio.profile_pic and user.portfolio.profile_pic != 'default.png':
                os.remove(os.path.join(current_app.config['IMG_UPLOAD_FOLDER'],
                                       user.portfolio.profile_pic))

            uploaded_file.save(os.path.join(current_app.config['IMG_UPLOAD_FOLDER'],
                                            new_pic))

        user.portfolio.profile_pic = new_pic
        user.portfolio.last_updated = datetime.datetime.now(datetime.UTC)
        db.session.commit()

        response = make_response(jsonify({"message": "Updated Profile Pic"}))
        return response, 200
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
@token_required
def update_resume(current_user):
    user = User.query.filter_by(username=current_user.username).first()

    if request.method == 'POST':
        uploaded_file = request.files['file']

        new_resume = f"{new_filename()}{get_file_extension(uploaded_file.filename)}"

        # For new user without portfolio, create one
        if not user.portfolio:
            new_portfolio = Portfolio(user_id=user.id)
            db.session.add(new_portfolio)
            db.session.commit()

        if uploaded_file.filename != '':
            # Remove user's existing resume

            if user.portfolio.resume is not None:
                os.remove(os.path.join(current_app.config['DOC_UPLOAD_FOLDER'],
                                       user.portfolio.profile_pic))

            uploaded_file.save(os.path.join(current_app.config['DOC_UPLOAD_FOLDER'],
                                            new_resume))

        user.portfolio.resume = new_resume
        user.portfolio.last_updated = datetime.datetime.now(datetime.UTC)
        db.session.commit()

        response = make_response(jsonify({"message": "Updated Resume"}))
        return response, 200
    return '''
    <!doctype html>
    <title>Upload Resume</title>
    <h1>Upload Resume</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file accept=".pdf">
      <input type=submit value=Upload>
    </form>
    '''


@views.route("/social_links/", methods=['GET', 'POST'])
@token_required
def create_get_social_links(current_user):
    if not current_user.portfolio:
        abort(401, "Access Denied")

    if request.method == "GET":

        if current_user.id != 1:
            abort(401, "Access Denied")

        social_links = [social_link.to_dict() for social_link in SocialLink.query.all()]
        return jsonify(social_links)
    elif request.method == 'POST':
        link_type = request.form['link_type']
        link_value = request.form['link_value']
        portfolio_id = int(request.form['portfolio_id'])

        if current_user.portfolio.id != portfolio_id:
            abort(401, "Access Denied")

        social_link = SocialLink(link_value=link_value, link_type=link_type,
                                 portfolio_id=portfolio_id)

        db.session.add(social_link)
        db.session.commit()

        response = make_response(jsonify({"message": "Added Social Link"}))
        return response, 200


@views.route("/social_links/<int:social_link_id>", methods=['GET', "PUT", "DELETE"])
@token_required
def get_update_social_links(social_link_id, current_user):
    social_link = SocialLink.query.get_or_404(social_link_id)

    # Authenticated User doesnt have a portfolio
    if not current_user.portfolio:
        abort(401, "Access Denied")

    if request.method == "GET":
        if social_link.portfolio_id != current_user.portfolio.id and current_user.portfolio.id != 1:
            abort(401, "Access Denied")

        return jsonify(social_link.to_dict())
    if request.method == 'PUT':
        update_fields = request.form.to_dict()

        if current_user.portfolio.id != social_link.portfolio_id:
            abort(401, "Access Denied")

        for key, value in update_fields.items():
            if value is not None:
                setattr(social_link, key, value)

        db.session.commit()

        response = make_response(jsonify({"message": "Updated Social Link"}))
        return response
    if request.method == "DELETE":

        if current_user.portfolio.id != social_link.portfolio_id:
            abort(401, "Access Denied")

        db.session.delete(social_link)
        db.session.commit()

        response = make_response(jsonify({"message": "Deleted Social Link"}))
        return response


@views.route('/about_sections/', methods=['GET', 'POST'])
@token_required
def get_create_about_section(current_user):
    user = User.query.get_or_404(current_user.id)

    if request.method == "GET":
        if user.id != 1:
            abort(401, "Access Denied")

        about_sections = [about.to_dict() for about in AboutSection.query.all()]
        return jsonify(about_sections)
    elif request.method == 'POST':
        create_fields = request.json
        create_fields['user_id'] = user.id

        tools = []

        if check_user_id_exists_in_table('about_section', create_fields['user_id']):
            abort(409, "About Section already exists for this user")

        if 'tools' in create_fields.keys():
            tools = create_fields['tools']
            del create_fields['tools']

        new_about_section = AboutSection()

        for key, value in create_fields.items():
            if value is not None and key in ['paragraph1', 'paragraph2', 'skills_intro', 'user_id']:
                setattr(new_about_section, key, value)

        db.session.add(new_about_section)
        db.session.commit()

        if tools:
            for tool_id in tools:
                tool = Tool.query.get_or_404(tool_id)
                new_about_section.tools.append(tool)

            db.session.commit()

        response = make_response(jsonify({"message": "Added About Section"}))
        return response, 200


@views.route('/about_sections/<int:about_id>', methods=['GET', 'PUT'])
@token_required
def get_update_about_section(about_id, current_user):
    about_section = AboutSection.query.get_or_404(about_id)

    if request.method == 'GET':

        if about_section.user_id != current_user.id and current_user.id != 1:
            abort(401, "Access Denied")

        return jsonify(about_section.to_dict())
    if request.method == 'PUT':
        put_fields = request.json
        tools = []

        if current_user.id != about_section.user_id:
            abort(401, "Access Denied")

        if 'tools' in put_fields.keys():
            tools = put_fields['tools']
            del put_fields['tools']

        for key, value in put_fields.items():
            if value is not None:
                setattr(about_section, key, value)

        db.session.commit()

        if tools:
            for tool_id in tools:
                tool = Tool.query.get_or_404(tool_id)
                if tool not in about_section.tools:
                    about_section.tools.append(tool)

            db.session.commit()

        response = make_response(jsonify({"message": "Updated About Section"}))
        return response, 200


@views.route("/experiences/", methods=['GET', 'POST'])
@token_required
def get_create_experiences(current_user):
    if request.method == "GET":

        if current_user.id != 1:
            abort(401, "Access Denied")

        experiences = [experience.to_dict() for experience in Experience.query.all()]
        return jsonify(experiences)
    elif request.method == 'POST':
        create_fields = request.json
        create_fields['user_id'] = current_user.id
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

        response = make_response(jsonify({"message": "Added New Experience"}))
        return response, 200


@views.route('/experiences/<int:experience_id>', methods=['GET', 'PUT'])
@token_required
def get_update_experience(experience_id, current_user):
    experience = Experience.query.get_or_404(experience_id)
    if request.method == 'GET':

        if current_user.id != experience.user_id and current_user.id != 1:
            abort(401, "Access Denied")

        return jsonify(experience.to_dict())
    if request.method == 'PUT':
        put_fields = request.json
        bullet_points = []

        if experience.user_id != current_user.id:
            abort(401, "Access Denied")

        if 'user_id' in put_fields.keys():
            del put_fields['user_id']

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

        response = make_response(jsonify({"message": "Updated Experience"}))
        return response, 200


@views.route("/experience_bullets/", methods=['GET', 'POST'])
@token_required
def get_create_experience_bullets(current_user):
    if request.method == "GET":
        if current_user.id != 1:
            abort(401, "Access Denied")
        bullet_points = [point.to_dict() for point in ExperienceBullet.query.all()]
        return jsonify(bullet_points)
    elif request.method == 'POST':
        create_fields = request.json
        experience = Experience.query.get(create_fields['experience_id'])

        if experience.user_id != current_user.id:
            abort(401, "Access Denied")

        bullet_point = ExperienceBullet(bullet_point=create_fields['bullet_point'],
                                        experience_id=create_fields['experience_id'])

        db.session.add(bullet_point)
        db.session.commit()

        response = make_response(jsonify({"message": "Added New Bullet Point"}))
        return response, 200


@views.route('/experience_bullets/<int:bullet_point_id>', methods=['GET', 'PUT'])
@token_required
def get_update_experience_bullets(bullet_point_id, current_user):
    bullet_point = ExperienceBullet.query.get_or_404(bullet_point_id)

    if request.method == 'GET':

        if bullet_point.experience.user_id != current_user.id and current_user.id != 1:
            abort(401, "Access Denied")

        return jsonify(bullet_point.to_dict())
    if request.method == 'PUT':
        new_bullet_text = request.json['bullet_point']

        if bullet_point.experience.user_id != current_user.id:
            abort(401, "Access Denied")
        
        bullet_point.bullet_point = new_bullet_text

        db.session.commit()

        response = make_response(jsonify({"message": "Updated Bullet Point"}))
        return response, 200


@views.route("/services/", methods=['GET', 'POST'])
@token_required
def get_create_services(current_user):
    if request.method == 'GET':
        
        if current_user.id != 1:
            abort(401, "Access Denied")

        services = [service.to_dict() for service in Service.query.all()]
        return jsonify(services)
    elif request.method == 'POST':
        create_fields = request.form
        
        service_name = create_fields['service_name']
        description = create_fields['description']

        services_section = ServicesSection.query.filter_by(user_id=current_user.id).first()

        new_service = Service(name=service_name, description=description,
                              services_section_id=services_section.id)

        db.session.add(new_service)
        db.session.commit()

        response = make_response(jsonify({"message": "Added New Service"}))
        return response, 200


@views.route("/services/<int:service_id>", methods=['GET', 'PUT'])
def get_update_service(service_id):
    service = Service.query.get_or_404(service_id)
    if request.method == "GET":
        return jsonify(service.to_dict())
    if request.method == "PUT":
        put_fields = request.json

        if 'services_section_id' in put_fields.keys():
            del put_fields['services_section_id']

        for key, value in put_fields.items():
            if value is not None:
                setattr(service, key, value)

        db.session.commit()
        return f"<p>Updated {service.name} service</p>"


@views.route("/services/names", methods=['GET'])
def get_service_names():
    query = text("""
                SELECT DISTINCT (name)
                FROM service;
            """)
    service_names = db.session.execute(query)

    service_names_list = [service_name[0] for service_name in service_names]
    result = {
        "service_names": service_names_list
    }

    return jsonify(result)


@views.route("/services_sections/", methods=['GET', 'POST'])
def get_create_services_sections():
    if request.method == 'GET':
        service_sections = [service_section.to_dict() for service_section in ServicesSection.query.all()]
        return jsonify(service_sections)
    if request.method == "POST":
        create_fields = request.json
        services = []

        if 'services' in create_fields.keys():
            services = create_fields['services']
            del create_fields['services']

        if check_user_id_exists_in_table('services_section', create_fields['user_id']):
            abort(409, "Services section already exists for this user")

        new_services_section = ServicesSection()

        for key, value in create_fields.items():
            if value is not None:
                setattr(new_services_section, key, value)

        db.session.add(new_services_section)
        db.session.commit()

        if services:
            for service in services:
                new_service = Service(name=service["name"], description=service["description"],
                                      services_section_id=new_services_section.id)
                db.session.add(new_service)

        db.session.commit()
        return "<p>Added new Service Section</p>"


@views.route("/services_sections/<int:service_section_id>", methods=['GET', 'PUT'])
def get_update_services_sections(service_section_id):
    services_section = ServicesSection.query.get_or_404(service_section_id)
    if request.method == 'GET':
        return jsonify(services_section.to_dict())
    if request.method == "PUT":
        update_fields = request.json
        services = []

        if 'services' in update_fields.keys():
            services = update_fields['services']
            del update_fields['services']

        if 'intro_text' in update_fields.keys():
            services_section.intro_text = update_fields["intro_text"]

        if services:
            for service in services:
                new_service = Service(name=service["name"], description=service["description"],
                                      services_section_id=services_section.id)
                db.session.add(new_service)

        db.session.commit()
        return "<p>Updated Service Section</p>"


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
                tool = Tool.query.get_or_404(tool_id)
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
                tool = Tool.query.get_or_404(tool_id)

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

        if check_tool_exists(name):
            abort(409, f"Tool with the name '{name}' already exists")

        new_tool = Tool(name=name)

        db.session.add(new_tool)
        db.session.commit()

        response = make_response(jsonify({"message": "Added New Tool"}))
        return response, 200


@views.route('projects/<int:project_id>/image', methods=['GET', 'POST'])
def update_project_image(project_id):
    project = Project.query.get_or_404(project_id)
    user = User.query.get_or_404(project.user_id)

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
    location = Location.query.get_or_404(location_id)
    if request.method == "GET":
        return jsonify(location.to_dict())
    if request.method == "PUT":
        update_fields = request.form.to_dict()
        for key, value in update_fields.items():
            if value is not None:
                setattr(location, key, value)

        db.session.commit()
        return jsonify(location.to_dict())

