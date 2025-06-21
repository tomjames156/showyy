import datetime
import os
from flask import (Blueprint, abort, current_app, request, jsonify, render_template, make_response)
from flask_restful import Resource, marshal_with
from flask_wtf.csrf import generate_csrf, validate_csrf
from werkzeug.utils import secure_filename
from flask_jwt_extended import create_access_token
from werkzeug.exceptions import HTTPException
from flask_jwt_extended import jwt_required
import json
from sqlalchemy import text
from .models import *
from .utils import get_file_extension
from hashlib import md5
from time import localtime
from . import db
from .auth import get_current_user


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


@views.route("/grid")
@jwt_required()
def begin():
    current_user = get_current_user()

    return current_user.profile_dict()


def get_date_string(date):
    return date.strftime("%B %Y")


@views.route('/profile/<string:username>/', methods=['GET'])
def portfolio(username):
    profile = User.query.filter_by(username=username).one_or_404()
    return render_template('portfolio.html', profile=profile.profile_dict(), get_date_string=get_date_string)


@views.route('/', methods=['GET'])
def get_tool():
    return render_template('tool.html')


@views.route('/profile_data/<string:username>/', methods=['GET'])
def get_user_profile_data(username):
    profile = User.query.filter_by(username=username).one_or_404()
    return jsonify(profile.profile_dict())


@views.route('/cms/<string:username>/edit', methods=['GET'])
def cms(username):
    profile = User.query.filter_by(username=username).one_or_404()
    locations = Location.query.all()
    access_token = create_access_token(identity=username, expires_delta=datetime.timedelta(days=100))
    tools = Tool.query.all()

    return render_template('cms.html', profile=profile.to_dict(), token=access_token, locations=locations, tools=tools)


@views.route('/cms/<string:username>/profile/edit', methods=['GET', 'POST'])
def profile(username):
    user = User.query.filter_by(username=username).one_or_404()
    portfolio = Portfolio.query.filter_by(user_id=user.id).first()
    access_token = create_access_token(identity=username, expires_delta=datetime.timedelta(days=100))

    # if request.method == 'POST':
    #     print(request.form)

    return render_template('profile.html', profile=user.to_dict(), portfolio=portfolio.to_dict(), token=access_token)


@views.route("/users/", methods=['GET'])
@jwt_required()
def get_users():

    current_user = get_current_user()

    if current_user.id == 1:
        users = [user.to_dict() for user in User.query.all()]
        return jsonify(users)
    else:
        abort(401, "Access Denied")


@views.route("/users/<int:user_id>/", methods=['GET', 'PUT'])
@jwt_required()
def get_update_user(user_id):
    current_user = get_current_user()
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
@jwt_required()
def get_create_portfolios():
    current_user = get_current_user()
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


@views.route('portfolios/<int:portfolio_id>/', methods=["GET", "PUT"])
@jwt_required()
def get_update_portfolio(portfolio_id):
    current_user = get_current_user()
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


@views.route('user/profile_pic/', methods=['GET', 'POST'])
@jwt_required()
def update_profile_pic():
    current_user = get_current_user()
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

            if user.portfolio.profile_pic is not None:
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


@views.route('user/resume/', methods=['GET', 'POST'])
@jwt_required()
def update_resume():
    current_user = get_current_user()
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
@jwt_required()
def create_get_social_links():
    current_user = get_current_user()
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


@views.route("/social_links/<int:social_link_id>/", methods=['GET', "PUT", "DELETE"])
@jwt_required()
def get_update_social_links(social_link_id):
    current_user = get_current_user()
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
@jwt_required()
def get_create_about_section():
    current_user = get_current_user()
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


@views.route('/about_sections/<int:about_id>/', methods=['GET', 'PUT'])
@jwt_required()
def get_update_about_section(about_id):
    current_user = get_current_user()
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
@jwt_required()
def get_create_experiences():
    current_user = get_current_user()
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
            if create_fields['end_date'] is None:
                new_experience.end_date = None
            else:
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


@views.route('/experiences/<int:experience_id>/', methods=['GET', 'PUT'])
@jwt_required()
def get_update_experience(experience_id):
    current_user = get_current_user()
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
@jwt_required()
def get_create_experience_bullets():
    current_user = get_current_user()
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


@views.route('/experience_bullets/<int:bullet_point_id>/', methods=['GET', 'PUT'])
@jwt_required()
def get_update_experience_bullets(bullet_point_id):
    current_user = get_current_user()
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
@jwt_required()
def get_create_services():
    current_user = get_current_user()
    if request.method == 'GET':
        
        if current_user.id != 1:
            abort(401, "Access Denied")

        services = [service.to_dict() for service in Service.query.all()]
        return jsonify(services)
    elif request.method == 'POST':
        create_fields = request.form

        service_name = create_fields['name']
        description = create_fields['description']

        services_section = ServicesSection.query.filter_by(user_id=current_user.id).first()

        # Handle image upload if file is present
        image_filename = None
        if 'service_image' in request.files and request.files['service_image'].filename != '':
            uploaded_file = request.files['service_image']
            image_filename = f"{new_filename()}{get_file_extension(uploaded_file.filename)}"
            uploaded_file.save(os.path.join(current_app.config['IMG_UPLOAD_FOLDER'], image_filename))

        new_service = Service(
            name=service_name,
            description=description,
            services_section_id=services_section.id,
            image=image_filename
        )

        db.session.add(new_service)
        db.session.commit()

        response = make_response(jsonify({"message": "Added New Service"}))
        return response, 200


@views.route("/services/<int:service_id>", methods=['GET', 'PUT'])
@jwt_required()
def get_update_service(service_id):
    current_user = get_current_user()
    service = Service.query.get_or_404(service_id)
    if request.method == "GET":
        
        if service.services_section.user_id != current_user.id and current_user.id != 1:
            abort(401, "Access Denied")
        
        return jsonify(service.to_dict())
    if request.method == "PUT":
        put_fields = request.json

        if service.services_section.user_id != current_user.id:
            abort(401, "Access Denied")

        if 'services_section_id' in put_fields.keys():
            del put_fields['services_section_id']

        for key, value in put_fields.items():
            if value is not None and key in ["name", "description"]:
                setattr(service, key, value)

        db.session.commit()
        
        response = make_response(jsonify({"message": "Updated Service"}))
        return response, 200


@views.route("/services/<int:service_id>/pic/", methods=['GET', 'POST'])
@jwt_required()
def get_update_service_img(service_id):
    current_user = get_current_user()
    service = Service.query.get_or_404(service_id)
    user = User.query.filter_by(username=current_user.username).first()

    if service.services_section.id != current_user.services_section.id and current_user.id != 1:
        abort(401, "Access Denied")

    if request.method == 'POST':
        uploaded_file = request.files['file']

        if service.services_section.id != current_user.services_section.id:
            abort(401, "Access Denied")

        new_pic = f"{new_filename()}{get_file_extension(uploaded_file.filename)}"

        # For new user without service_section, create one
        if not user.services_section:
            new_services_section = ServicesSection(user_id=user.id)
            db.session.add(new_services_section)
            db.session.commit()

        if uploaded_file.filename != '':
            # Remove user's existing profile pic

            if service.image is not None:
                os.remove(os.path.join(current_app.config['IMG_UPLOAD_FOLDER'],
                                       service.image))

            uploaded_file.save(os.path.join(current_app.config['IMG_UPLOAD_FOLDER'],
                                            new_pic))

        service.image = new_pic
        db.session.commit()

        response = make_response(jsonify({"message": "Updated Service Image"}))
        return response, 200
    return f'''
    <!doctype html>
    <title>Upload Profile Picture</title>
    <h1>Upload Profile Picture</h1>
    <img src={service.image} alt={service.image}>
    <p>{service.name}</p>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file accept=".png,.jpg,.jpeg,.gif">
      <input type=submit value=Upload>
    </form>
    '''


@views.route("/services/names/", methods=['GET'])
@jwt_required()
def get_service_names():
    current_user = get_current_user()
    query = text(f"""
                SELECT DISTINCT (name)
                FROM service
                WHERE services_section_id = {current_user.services_section.id};
            """)
    service_names = db.session.execute(query)

    service_names_list = [service_name[0] for service_name in service_names]
    result = {
        "service_names": service_names_list
    }

    return jsonify(result)


@views.route("/services_sections/", methods=['GET', 'POST'])
@jwt_required()
def get_create_services_sections():
    current_user = get_current_user()
    if request.method == 'GET':
        if current_user.id != 1:
            abort(401, "Access Denied")
        service_sections = [service_section.to_dict() for service_section in ServicesSection.query.all()]
        return jsonify(service_sections)
    if request.method == "POST":
        create_fields = request.json
        services = []

        if 'services' in create_fields.keys():
            services = create_fields['services']
            del create_fields['services']

        if check_user_id_exists_in_table('services_section', current_user.id):
            abort(409, "Services section already exists for this user")

        new_services_section = ServicesSection(user_id=current_user.id)

        for key, value in create_fields.items():
            if value is not None and key in ["intro_text"]:
                setattr(new_services_section, key, value)

        db.session.add(new_services_section)
        db.session.commit()

        if services:
            for service in services:
                new_service = Service(name=service["name"], description=service["description"],
                                      services_section_id=new_services_section.id)
                db.session.add(new_service)

        db.session.commit()
        
        response = make_response(jsonify({"message": "Added New Service Section"}))
        return response, 200


@views.route("/services_sections/<int:service_section_id>/", methods=['GET', 'PUT'])
@jwt_required()
def get_update_services_sections(service_section_id):
    current_user = get_current_user()
    services_section = ServicesSection.query.get_or_404(service_section_id)
    if request.method == 'GET':
        if current_user.services_section.user_id != services_section.user_id and current_user.id != 1:
            abort(401, "Access Denied")
        return jsonify(services_section.to_dict())
    if request.method == "PUT":
        update_fields = request.json
        services = []

        if current_user.services_section.user_id != services_section.user_id:
            abort(401, "Access Denied")

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

        response = make_response(jsonify({"message": "Updated Service Section"}))
        return response, 200


@views.route("/projects/", methods=['GET', 'POST'])
@jwt_required()
def get_create_projects():
    current_user = get_current_user()
    if request.method == "GET":

        if current_user.id != 1:
            abort(401, "Access Denied")

        projects = [project.to_dict() for project in Project.query.all()]
        return jsonify(projects)
    elif request.method == 'POST':
        create_fields = request.form.to_dict()
        name = create_fields['name']
        description = create_fields['description']
        user_id = current_user.id

        project = Project(name=name, description=description, user_id=user_id)

        if 'highlight' in create_fields.keys():
            setattr(project, 'highlight', create_fields['highlight'])

        db.session.add(project)
        db.session.commit()

        # Handle tools if provided
        if 'tools' in create_fields.keys():
            tools = request.form.getlist('tools')
            for tool_id in tools:
                tool = Tool.query.get_or_404(tool_id)
                project.tools.append(tool)
            db.session.commit()

        # Handle image upload if file is present
        if 'project_image' in request.files and request.files['project_image'].filename != '':
            uploaded_file = request.files['project_image']
            # Save image using the same logic as update_project_image
            new_pic = f"{new_filename()}{get_file_extension(uploaded_file.filename)}"
            uploaded_file.save(os.path.join(current_app.config['IMG_UPLOAD_FOLDER'], new_pic))
            project.image = new_pic
            db.session.commit()

        response = make_response(jsonify({"message": "Added New Project"}))
        return response, 200


@views.route('/projects/<int:project_id>/', methods=['GET', 'PUT'])
@jwt_required()
def get_update_project(project_id):
    current_user = get_current_user()
    project = Project.query.get_or_404(project_id)
    if request.method == 'GET':

        if project.user_id != current_user.id and current_user.id != 1:
            abort(401, "Access Denied")

        return jsonify(project.to_dict())
    if request.method == 'PUT':
        put_fields = request.json

        if project.user_id != current_user.id:
            abort(401, "Access Denied")

        if 'tools' in put_fields.keys():
            for tool_id in put_fields['tools']:
                tool = Tool.query.get_or_404(tool_id)

                if tool not in project.tools:
                    project.tools.append(tool)

            del put_fields['tools']

        if 'highlight' in put_fields.keys():
            setattr(project, 'highlight', put_fields['highlight'])
            del put_fields['highlight']

        for key, value in put_fields.items():
            if value is not None:
                setattr(project, key, value)

        db.session.commit()

        response = make_response(jsonify({"message": "Updated Project"}))
        return response, 200
    

@views.route('projects/<int:project_id>/image', methods=['GET', 'POST'])
@jwt_required()
def update_project_image(project_id):
    current_user = get_current_user()
    project = Project.query.get_or_404(project_id)

    if project.user_id != current_user.id and current_user.id != 1:
        abort(401, "Access Denied")

    if request.method == 'POST':
        uploaded_file = request.files['file']
        new_pic = f"{new_filename()}{get_file_extension(uploaded_file.filename)}"

        if project.user_id != current_user.id:
            abort(401, "Access Denied")

        if uploaded_file.filename != '':
            # Remove user's existing profile pic

            if project.image is not None:
                os.remove(os.path.join(current_app.config['IMG_UPLOAD_FOLDER'],
                                       project.image))

            uploaded_file.save(os.path.join(current_app.config['IMG_UPLOAD_FOLDER'],
                                            new_pic))

        project.image = new_pic
        db.session.commit()
        
        response = make_response(jsonify({"message": "Updated Project Image"}))
        return response, 200
    return f'''
    <!doctype html>
    <title>Upload Profile Picture</title>
    <h1>Upload Profile Picture</h1>
    <p>{project.name} - Img {project.image}</p>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file accept=".png,.jpg,.jpeg,.gif">
      <input type=submit value=Upload>
    </form>
    '''


@views.route("/tools/", methods=['GET', 'POST'])
@jwt_required()
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


@views.route("/tools/search/", methods=['GET'])
@jwt_required()
def find_tool():
    tool_string = request.args.get('tool_string')

    query = text(f"""
                SELECT *
                FROM tool
                WHERE name LIKE "{tool_string + '%'}";
            """)
    tools_found = db.session.execute(query)

    tools_list = [{"id": tool.id, "name": tool.name} for tool in tools_found]

    result = {
        "tools": tools_list
    }

    return jsonify(result)    


@views.route('locations/', methods=['GET', 'POST'])
@jwt_required()
def get_add_locations():
    if request.method == "GET":
        locations = [location.to_dict() for location in Location.query.all()]

        return jsonify(locations)
    if request.method == "POST":
        post_fields = request.form.to_dict()

        # Add a feature later to check whether the location already exists
        # query = text(f"""
        #         SELECT *
        #         FROM tool
        #         WHERE (name, city, country) = {f"({post_fields['city']}, {post_fields[]}, {})"};
        #         """)
        
        location = Location(city=post_fields['city'], state=post_fields['state'],
        country=post_fields[
            'country'])

        db.session.add(location)
        db.session.commit()

        response = make_response(jsonify({"message": "Added New Location"}))
        return response, 200


@views.route('locations/<int:location_id>/', methods=["GET"])
@jwt_required()
def get_location(location_id):
    location = Location.query.get_or_404(location_id)
    if request.method == "GET":
        return jsonify(location.to_dict())


@views.route("/locations/search/", methods=['POST'])
@jwt_required()
def find_location():
    """
    Finds locations based on city, state, and/or country.
    Requires a POST request with JSON data.
    """
    search_data = request.get_json()

    if not search_data:
        return jsonify({'message': 'No search parameters provided'}), 400

    city = search_data.get('city', '')
    state = search_data.get('state', '')
    country = search_data.get('country', '')

    # Build the query dynamically
    query_parts = []
    if city:
        query_parts.append(f"city LIKE '{city}%'")
    if state:
        query_parts.append(f"state LIKE '{state}%'")
    if country:
        query_parts.append(f"country LIKE '{country}%'")

    if not query_parts:
        return jsonify({'message': 'At least one search parameter (city, state, or country) is required'}), 400

    # Add '1=1' to handle the case where no other conditions are added
    sql_query = "SELECT * FROM location WHERE 1=1 "
    if query_parts:  # Add AND only if there are conditions
        sql_query += " AND " + " AND ".join(query_parts) + ";"
    else:
        sql_query += ";" #this is needed

    query = text(sql_query)

    try:
        locations_found = db.session.execute(query)
        # Fetch all results at once and convert to a list of dictionaries
        locations_list = [{"id": loc.id, "city": loc.city, "state": loc.state, "country": loc.country} for loc in locations_found]

        result = {
            "locations": locations_list
        }
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500


@views.route("/client_testimonials/", methods=['GET', 'POST'])
@jwt_required()
def get_create_testimonials():
    current_user = get_current_user()
    if request.method == 'GET':
        if current_user.id != 1:
            abort(401, "Access Denied")

        testimonials = [testimonial.to_dict() for testimonial in ClientTestimonial.query.all()]

        return jsonify(testimonials)
    if request.method == 'POST':
        create_fields = request.form
        
        new_testimonial = ClientTestimonial(user_id=current_user.id, testimonial=create_fields["testimonial"], organization=create_fields['organization'], name=create_fields['name'])

        db.session.add(new_testimonial)
        db.session.commit() 

        response = make_response(jsonify({"message": "Added New Testimonial"}))
        return response, 200


@views.route("/client_testimonials/<int:testimonial_id>/", methods=['GET', 'PUT'])
@jwt_required()
def get_update_client_testimonial(testimonial_id):
    current_user = get_current_user()
    testimonial = ClientTestimonial.query.get_or_404(testimonial_id)

    if request.method == 'GET':

        if current_user.id != 1 and current_user.id != testimonial.user_id:
            abort(401, "Access Denied")

        return jsonify(testimonial.to_dict())
    
    if request.method == "PUT":
        put_fields = request.form
        
        if current_user.id != testimonial.user_id:
            abort(401, "Access Denied")

        for key, value in put_fields.items():
            if value is not None and key in ['name', 'organization', 'testimonial']:
                setattr(testimonial, key, value)

        db.session.commit()
        
        response = make_response(jsonify({"message": "Updated Client Testimonial"}))
        return response, 200


@views.route("/client_testimonials/<int:testimonial_id>/pic/", methods=['GET', 'POST'])
@jwt_required()
def get_update_client_image(testimonial_id):
    current_user = get_current_user()
    testimonial = ClientTestimonial.query.get_or_404(testimonial_id)

    if testimonial.user_id != current_user.id and current_user.id != 1:
        abort(401, "Access Denied")

    if request.method == 'POST':
        uploaded_file = request.files['file']

        if testimonial.user_id != current_user.id:
            abort(401, "Access Denied")

        new_pic = f"{new_filename()}{get_file_extension(uploaded_file.filename)}"

        if uploaded_file.filename != '':
            # Remove user's existing profile pic

            if testimonial.image is not None:
                os.remove(os.path.join(current_app.config['IMG_UPLOAD_FOLDER'],
                                       testimonial.image))

            uploaded_file.save(os.path.join(current_app.config['IMG_UPLOAD_FOLDER'],
                                            new_pic))

        testimonial.image = new_pic
        db.session.commit()

        response = make_response(jsonify({"message": "Updated Client Image"}))
        return response, 200
    return f'''
    <!doctype html>
    <title>Upload Profile Picture</title>
    <h1>Upload Profile Picture</h1>
    <img style='width: 100px; height: auto; border-radius: 50%;' src='../../../static/images/{testimonial.image}' alt='Picture of {testimonial.name}'>
    <p>{testimonial.testimonial}</p>
    <p>{testimonial.name}</p>
    <p>{testimonial.organization}<p>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file accept=".png,.jpg,.jpeg,.gif">
      <input type=submit value=Upload>
    </form>
    '''


@views.route("/contact_sections/", methods=['GET', 'POST'])
@jwt_required()
def get_create_contact_sections():
    current_user = get_current_user()
    
    if request.method == 'GET':
        if current_user.id != 1:
            abort(401, "Access Denied")

        contact_sections = [contact.to_dict() for contact in ContactSection.query.all()]
        return jsonify(contact_sections)
    if request.method == "POST":
        create_fields = request.form

        if check_user_id_exists_in_table('contact_section', current_user.id):
            abort(409, "Already Exists")
        new_contact_section = ContactSection(user_id=current_user.id)

        for key, value in create_fields.items():
            if value is not None and key in ['intro_text', 'phone_number', 'contact_email', 'location_id']:
                setattr(new_contact_section, key, value)

        db.session.add(new_contact_section)
        db.session.commit()

        response = make_response(jsonify({"message": "Created new Contact Section"}))
        response, 200


@views.route("/contact_sections/<int:contact_sect_id>/", methods=['GET', 'PUT'])
@jwt_required()
def get_update_contact_section(contact_sect_id):
    current_user = get_current_user()
    contact_section = ContactSection.query.get_or_404(contact_sect_id)

    if request.method == "GET":

        if current_user.id != 1 and contact_section.user_id != current_user.id:
            abort(401, "Access Denied")

        return jsonify(contact_section.to_dict())
    if request.method == 'PUT':
        put_fields = request.form.to_dict()

        if contact_section.user_id != current_user.id:
            abort(401, "Access Denied")

        for key, value in put_fields.items():
            if value is not None and key in ['intro_text', 'phone_number', 'contact_email', 'location_id']:
                put_fields['location_id'] = int(put_fields['location_id'])
                setattr(contact_section, key, value)

        db.session.commit()

        response = make_response(jsonify({"message": "Updated Contact Section"}))
        return response, 200

