import datetime
import os
from flask import Blueprint, current_app, request, jsonify, flash, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from .models import *
from .utils import get_file_extension
from . import db


UPLOAD_FOLDER = '/files/'
views = Blueprint('views', __name__)

@views.route("/")
def start():
    return render_template('home.html')


@views.route("/projects/", methods=['GET', 'POST'])
def get_create_projects():
    if request.method == "GET":
        projects = [project.to_dict() for project in Project.query.all()]
        return jsonify(projects)
    elif request.method == 'POST':
        create_fields = request.form.to_dict()

        name = create_fields['name']
        description = create_fields['description']
        user_id = create_fields['user_id']

        project = Project(name=name, description=description, user_id= user_id)

        if 'highlight' in create_fields.keys():
            setattr(project, 'highlight', create_fields['highlight'] == 'True')

        db.session.add(project)
        db.session.commit()

        if 'tools' in create_fields.keys():
            tools = [int(tool_id) for tool_id in create_fields['tools'].split(',')]

            for tool_id in tools:
                tool = Tool.query.get(tool_id)
                project.tools.append(tool)


        db.session.commit()

        return "<p>Added New Project</p>"


@views.route('/projects/<int:project_id>', methods=['PUT', 'GET', 'DELETE'])
def get_update_project(project_id):
    project = Project.query.get(project_id)
    if request.method == 'GET':
        return jsonify(project.to_dict())
    elif request.method == 'PUT':
        
        put_fields = request.form.to_dict()
        if 'tools' in put_fields.keys():
            additional_tools = [int(tool_id) for tool_id in put_fields['tools'].split(',')]
            del put_fields['tools']

            for tool_id in additional_tools:
                tool = Tool.query.get(tool_id)

                if tool not in project.tools:
                    project.tools.append(tool)

        if 'highlight' in put_fields.keys():
            setattr(project, 'highlight', put_fields['highlight'] == 'True')
            del put_fields['highlight']

        for key, value in put_fields.items():
            if value is not None:
                setattr(project, key, value)

        db.session.commit()
        return "<p>Updated Project</p>"

    if request.method == 'DELETE':
            db.session.delete(project)
            db.session.commit()

            return "<p>Project deleted</p>"
    


@views.route("/tools/", methods=['GET', 'POST'])
def get_create_tools():
    if request.method == 'GET':
        tools = [tool.to_dict() for tool in Tool.query.all()]
        return jsonify(tools)
    if request.method == 'POST':
        name = request.form['name']

        new_tool = Tool(name=name)

        db.session.add(new_tool)
        db.session.commit()

        return "<p>Added New Tool</p>"
    

@views.route("/tools/<int:tool_id>", methods=['GET', 'DELETE'])
def get_delete_tool(tool_id):
    tool = Tool.query.get_or_404(tool_id)
    if request.method == 'GET':
        return jsonify(tool.to_dict())
    if request.method == 'DELETE':
        db.session.delete(tool)
        db.session.commit()

        return "<p>Tool deleted</p>"

@views.route("/users/", methods=['GET'])
def get_users():
    users = [user.to_dict() for user in User.query.all()]
    return jsonify(users)


@views.route("/users/<int:user_id>", methods=['GET', 'PUT'])
def get_update_user(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == "GET":
        return jsonify(user.to_dict())
    elif request.method == "PUT":
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
    if request.method == 'POST':
        link_type = request.form['link_type']
        link_value = request.form['link_value']
        portfolio_id = request.form['portfolio_id']

        social_link = SocialLink(link_value=link_value, link_type=link_type,
                                 portfolio_id=portfolio_id)

        db.session.add(social_link)
        db.session.commit()

        return "<p>Added New Social Link</p>"


@views.route("/social_links/<int:social_link_id>", methods=['GET', "PUT", 'DELETE'])
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
    if request.method == 'DELETE':
        db.session.delete(social_link)
        db.session.commit()

        return "<p>social link  removed</p>"

@views.route("/portfolios/", methods=['GET', 'POST'])
def get_create_portfolios():
    if request.method == 'GET':
        portfolios = [portfolio.to_dict() for portfolio in Portfolio.query.all()]
        return jsonify(portfolios)
    if request.method == 'POST':
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


@views.route("/portfolios/<int:portfolio_id>", methods=['GET', 'PUT'])
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
    
@views.route('/portfolios/<int:portfolio_id>', methods=['GET', 'DELETE'])
def get_delete_portfolio(portfolio_id):
    portfolio = Portfolio.query.filter_by(id=portfolio_id).first()

    if request.method == "GET":
        return jsonify(portfolio.to_dict())
    elif request.method == 'DELETE':
        db.session.delete(portfolio)
        db.session.commit()

        return "<p>Portfolio deleted</p>"
    


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
        country=post_fields['country'])

        db.session.add(location)
        db.session.commit()

        return "<p>Added Location</p>"


@views.route("locations/<int:location_id>", methods=['GET', 'PUT', 'DELETE'])
def get_update_location(location_id):
    location = Location.query.filter_by(id=location_id).first()
    if request.method == 'GET':
        return jsonify(location.to_dict())
    if request.method == 'PUT':
        update_fields = request.form.to_dict()
        for key, value in update_fields.items():
            if value is not None:
                setattr(location, key, value)

        db.session.commit()
        return jsonify(location.to_dict())
    if request.method == 'DELETE':
        db.session.delete(location)
        db.session.commit()

        return "<p>Location deleted.</p>"


@views.route("/testimonials/", methods=['GET', 'POST'])
def get_create_testimonial():
    if request.method == 'GET':
        testimonials = [testimonial.to_dict() for testimonial in Testimonial.query.all()]
        return jsonify(testimonials)
    if request.method == 'POST':
        
        testimonial_text = request.json['testimonial_text']
        client_id = request.json['client_id']

        new_testimonial = Testimonial(testimonial_text=testimonial_text, client_id=client_id)

        db.session.add(new_testimonial)
        db.session.commit()

        return "<p>Added New testimonial</p>"

@views.route("testimonials/<int:testimonial_id>", methods=['GET', 'PUT', 'DELETE'])
def get_update_testimonial(testimonial_id):
    testimonial = Testimonial.query.get_or_404(testimonial_id)
    if request.method == 'GET':
        return jsonify(testimonial.to_dict())
    if request.method == 'PUT':
        put_fields = request.json

        for key, value in put_fields.items():
            if value is not None:
                setattr(testimonial, key, value)

        db.session.commit()
        return "<p>testimonial updated</p>"
    if request.method == 'DELETE':
        db.session.delete(testimonial)
        db.session.commit()

        return "<p>Testimonial deleted</p>"



@views.route("/clients/", methods=['GET', 'POST'])
def get_create_clients():
    if request.method == 'GET':
        clients = [client.to_dict() for client in Client.query.all()]
        return jsonify(clients)
    if request.method == 'POST':
        create_fields = request.json

        name = create_fields['name']
        organization = create_fields['organization']

        new_client = Client(name=name, organization=organization)

        db.session.add(new_client)
        db.session.commit()

        return "<p>Added client</p>"

@views.route("clients/<int:client_id>", methods=['GET', 'PUT', 'DELETE'])
def get_update_client(client_id):
    client = Client.query.get_or_404(client_id)
    if request.method == 'GET':
        return jsonify(client.to_dict())
    if request.method == 'PUT':
        put_fields = request.json

        for key, value in put_fields.items():
            if value is not None:
                setattr(client, key, value)

        db.session.commit()
        return "<p>client updated</p>"
    if request.method == 'DELETE':
        db.session.delete(client)
        db.session.commit()

        return "<p>client removed</p>"

@views.route("/about_section/", methods=['GET', 'POST'])
def get_create_about_section():
    if request.method == 'GET':
        about_section = [about_section.to_dict() for about_section in AboutSection.query.all()]
        return jsonify(about_section)
    if request.method == 'POST':
        create_fields = request.json

        paragraph1 = create_fields['paragraph1']
        paragraph2 = create_fields['paragraph2']
        skills_intro = create_fields['skills_intro']

        about_section = AboutSection(paragraph1=paragraph1, paragraph2=paragraph2, skills_intro=skills_intro)

        db.session.add(about_section)
        db.session.commit()

        return "<p>About section added</p>"


@views.route('/about_section/<int:about_section_id>', methods=['PUT', 'GET', 'DELETE'])
def get_update_about_section(about_section_id):
    about_section = AboutSection.query.get_or_404(about_section_id)
    if request.method == 'GET':
        return jsonify(about_section.to_dict())
    elif request.method == 'PUT':
        
        put_fields = request.json

        for key, value in put_fields.items():
            if value is not None:
                setattr(about_section, key, value)

        db.session.commit()
        return "<p>About section updated</p>"
    if request.method == 'DELETE':
        db.session.delete(about_section)
        db.session.commit()

        return "<p>About section removed</p>"

@views.route("/contact_section/", methods=['GET', 'POST'])
def get_create_contact_section():
    if request.method == 'GET':
        contact_section = [contact_section.to_dict() for contact_section in ContactSection.query.all()]
        return jsonify(contact_section)
    if request.method == 'POST':
        create_fields = request.json

        intro_text = create_fields['intro_text']
        phone_number = create_fields['phone_number']
        city = create_fields['city']
        state = create_fields['state']

        contact_section = ContactSection(intro_text=intro_text, phone_number=phone_number, city=city, state=state)

        db.session.add(contact_section)
        db.session.commit()

        return "<p>Contact section added</p>"


@views.route('/contact_section/<int:contact_section_id>', methods=['PUT', 'GET', 'DELETE'])
def get_update_contact_section(contact_section_id):
    contact_section = ContactSection.query.get_or_404(contact_section_id)
    if request.method == 'GET':
        return jsonify(contact_section.to_dict())
    elif request.method == 'PUT':
        
        put_fields = request.json

        for key, value in put_fields.items():
            if value is not None:
                setattr(contact_section, key, value)

        db.session.commit()
        return "<p>Contact section updated</p>"
    if request.method == 'DELETE':
        db.session.delete(contact_section)
        db.session.commit()

        return "< Contact section removed</p>"
    
@views.route("/testimonial_section/", methods=['GET', 'POST'])
def get_create_testimonial_section():
    if request.method == 'GET':
        testimonial_section = [testimonial_section.to_dict() for testimonial_section in TestimonialSection.query.all()]
        return jsonify(testimonial_section)
    if request.method == 'POST':
        create_fields = request.json

        testimonial_id = create_fields['testimonial_id']
        

        testimonial_section = TestimonialSection(testimonial_id=testimonial_id)

        db.session.add(testimonial_section)
        db.session.commit()

        return "<p>Testimonial section added</p>"


@views.route('/testimonial_section/<int:testimonial_section_id>', methods=['PUT', 'GET', 'DELETE'])
def get_update_testimonial_section(testimonial_section_id):
    testimonial_section = TestimonialSection.query.get_or_404(testimonial_section_id)
    if request.method == 'GET':
        return jsonify(testimonial_section.to_dict())
    elif request.method == 'PUT':
        
        put_fields = request.json

        for key, value in put_fields.items():
            if value is not None:
                setattr(testimonial_section, key, value)

        db.session.commit()
        return "<p>Testimonial section updated</p>"
    if request.method == 'DELETE':
        db.session.delete(testimonial_section)
        db.session.commit()

        return "<p>Testimonial section removed</p>"
    
@views.route("/service/", methods=['GET', 'POST'])
def get_create_about_section():
    if request.method == 'GET':
        service = [service.to_dict() for service in Service.query.all()]
        return jsonify(service)
    if request.method == 'POST':
        create_fields = request.json

        user_id = create_fields['user_id']
        name = create_fields['name']
        description = create_fields['description']

        service = Service(user_id=user_id, name=name, description=description)

        db.session.add(service)
        db.session.commit()

        return "<p>Service added</p>"

@views.route('/service/<int:service_id>', methods=['PUT', 'GET', 'DELETE'])
def get_update_service(service_id):
    service = Service.query.get_or_404(service_id)
    if request.method == 'GET':
        return jsonify(service.to_dict())
    elif request.method == 'PUT':
        
        put_fields = request.json

        for key, value in put_fields.items():
            if value is not None:
                setattr(service, key, value)

        db.session.commit()
        return "<p>Service updated</p>"
    if request.method == 'DELETE':
        db.session.delete(service)
        db.session.commit()

        return "<p>Service removed</p>"

@views.route("/service_section/", methods=['GET', 'POST'])
def get_create_service_section():
    if request.method == 'GET':
        service_section = [service_section.to_dict() for service_section in ServiceSection.query.all()]
        return jsonify(service_section)
    if request.method == 'POST':
        create_fields = request.json

        intro_text = create_fields['intro_text']

        service_section = ServiceSection(intro_text=intro_text)

        db.session.add(service_section)
        db.session.commit()

        return "<p>Service section added</p>"


@views.route('/service_section/<int:service_section_id>', methods=['PUT', 'GET', 'DELETE'])
def get_update_service_section(service_section_id):
    service_section = ServiceSection.query.get_or_404(service_section_id)
    if request.method == 'GET':
        return jsonify(service_section.to_dict())
    elif request.method == 'PUT':
        
        put_fields = request.json

        for key, value in put_fields.items():
            if value is not None:
                setattr(service_section, key, value)

        db.session.commit()
        return "<p>service section updated</p>"
    if request.method == 'DELETE':
        db.session.delete(service_section)
        db.session.commit()

        return "<p>service section removed</p>"
    
@views.route("/person/", methods=['GET', 'POST'])
def get_create_person():
    if request.method == 'GET':
        person = [person.to_dict() for person in Person.query.all()]
        return jsonify(person)
    if request.method == 'POST':
        create_fields = request.json

        name = create_fields['name']
        organization = create_fields['organization']

        person = Person(name=name, organization=organization)

        db.session.add(person)
        db.session.commit()

        return "<p>person added</p>"


@views.route('/person/<int:person_id>', methods=['PUT', 'GET', 'DELETE'])
def get_update_person(person_id):
    person = Person.query.get_or_404(person_id)
    if request.method == 'GET':
        return jsonify(person.to_dict())
    elif request.method == 'PUT':
        
        put_fields = request.json

        for key, value in put_fields.items():
            if value is not None:
                setattr(person, key, value)

        db.session.commit()
        return "<p>Person updated</p>"
    if request.method == 'DELETE':
        db.session.delete(person)
        db.session.commit()

        return "<p>Person removed</p>"
    

@views.route("/experienceBullet/", methods=['GET', 'POST'])
def get_create_experienceBullet():
    if request.method == 'GET':
        experienceBullet = [experienceBullet.to_dict() for experienceBullet in ExperienceBullet.query.all()]
        return jsonify(experienceBullet)
    if request.method == 'POST':
        create_fields = request.json

        bullet_point = create_fields['bullet_point']
        experience_id = create_fields['experience_id']

        experienceBullet = ExperienceBullet(bullet_point=bullet_point, experience_id=experience_id)

        db.session.add(experienceBullet)
        db.session.commit()

        return "<p> Experience added</p>"


@views.route('/experienceBullet/<int:experienceBullet_id>', methods=['PUT', 'GET', 'DELETE'])
def get_update_experienceBullet(experienceBullet_id):
    experienceBullet = ExperienceBullet.query.get_or_404(experienceBullet_id)
    if request.method == 'GET':
        return jsonify(experienceBullet.to_dict())
    elif request.method == 'PUT':
        
        put_fields = request.json

        for key, value in put_fields.items():
            if value is not None:
                setattr(experienceBullet, key, value)

        db.session.commit()
        return "<p>Experience updated</p>"
    if request.method == 'DELETE':
        db.session.delete(experienceBullet)
        db.session.commit()

        return "<p>Experience removed</p>"
    

@views.route("/experience/", methods=['GET', 'POST'])
def get_create_experience():
    if request.method == 'GET':
        experience = [experience.to_dict() for experience in Experience.query.all()]
        return jsonify(experience)
    if request.method == 'POST':
        create_fields = request.json

        organization = create_fields['organization']
        role = create_fields['role']
        user_id = create_fields['user_id']
        start_date = 
        end_date = 


        experience = Experience(organization=organization, role=role, user_id=user_id, start_date=start_date, end_date=end_date)

        db.session.add(experience)
        db.session.commit()

        return "<p>Experience added</p>"


@views.route('/experience/<int:experience_id>', methods=['PUT', 'GET', 'DELETE'])
def get_update_experience(experience_id):
    experience = Experience.query.get_or_404(experience_id)
    if request.method == 'GET':
        return jsonify(experience.to_dict())
    elif request.method == 'PUT':
        
        put_fields = request.json

        for key, value in put_fields.items():
            if value is not None:
                setattr(experience, key, value)

        db.session.commit()
        return "<p>Experience updated</p>"
    if request.method == 'DELETE':
        db.session.delete(Experience)
        db.session.commit()

        return "<p>Experience removed</p>"