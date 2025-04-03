from . import db
import datetime
from flask_login import UserMixin


project_tools = db.Table(
    'project_tools',
    db.Column("project_id", db.Integer, db.ForeignKey('project.id'), primary_key=True),
    db.Column("tool_id", db.Integer, db.ForeignKey('tool.id'), primary_key=True)
)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    highlight = db.Column(db.Boolean, default=False)
    image = db.Column(db.String, default='default.png')
    tools = db.relationship('Tool', secondary=project_tools, backref='projects', lazy='subquery')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description':self.description,
            'highlight': self.highlight,
            'image': self.image,
            'tools': [tool.to_dict() for tool in self.tools],
            'user_id': self.user_id
        }


class Tool(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    country = db.Column(db.String(100))
    portfolios = db.relationship('Portfolio', backref='location', lazy=True)

    def to_dict(self):
        return{
            'id': self.id,
            'city': self.city,
            'state': self.state,
            'country': self.country
        }


class SocialLink(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    link_type = db.Column(db.String(150), nullable=False)
    link_value = db.Column(db.String(2000), nullable=False)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolio.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'link_type': self.link_type,
            'link_value': self.link_value,
            'portfolio_id': self.portfolio_id
        }


class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role = db.Column(db.String(100), nullable=False)
    resume = db.Column(db.String(150))
    date_created = db.Column(db.DateTime)
    last_updated = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    profile_pic = db.Column(db.String(100), default='default.png')
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    social_links = db.relationship('SocialLink', backref='portfolio', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'role': self.role,
            'resume': self.resume,
            'date_created': self.date_created,
            'last_updated': self.last_updated,
            'user_id': self.user_id,
            'profile_pic': self.profile_pic,
            'location_id': self.location_id,
            'location': self.location.to_dict() if self.location else None,
            'social_links': [social_link.to_dict() for social_link in self.social_links]
        }
class ExperienceBullet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bullet_point = db.Column(db.String(500), nullable=False)
    experience_id = db.Column(db.Integer, db.ForeignKey('experience.id'))

    def to_dict(self):
        return{
            'id' : self.id,
            'bullet_point' : self.bullet_point,
            'experience_id' : self.experience_id
        }


class Experience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    organization = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(150), nullable=False)
    start_date = db.Column(db.DateTime(timezone=True), nullable=False)
    end_date = db.Column(db.DateTime(timezone=True))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    bullet_points = db.relationship('ExperienceBullet', backref='experience', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'organization': self.organization,
            'role': self.role,
            'start_date' : self.start_date,
            'end_date' : self.end_date,
            'user_id' : self.user_id,
            'bullet_points': [bullet.to_dict() for bullet in self.bullet_points]
        }

class Testimonial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    testimonial_text = db.Column(db.String(10000))
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'testimonial_text': self.testimonial_text
        }



class client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    organization = db.Column(db.String(150))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'organization': self.organization
        }
class ContactSection(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     intro_text = db.Column(db.String(10000))
     phone_number = db.Column(db.Integer, nullable=False)
     contact_email = db.Column(db.String(150), unique=True)
     city = db.Column(db.String(100))
     state = db.Column(db.String(100))

     def to_dict(self):
        return {
            'id': self.id,
            'intro_text': self.intro_text,
            'phone_number': self.phone_number,
            'contact_email': self.contact_email,
            'city': self.city,
            'state': self.state
        }



class AboutSection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paragraph1 = db.Column(db.String(10000))
    skills_intro = db.Column(db.String(10000))
    paragraph2 = db.Column(db.String(10000))
    picture_display = db.Column(db.String(10000), default='default.png')

    def to_dict(self):
        return {
            'id': self.id,
            'paragraph1': self.paragraph1,
            'skills_intro': self.skills_intro,
            'paragraph2': self.paragraph2,
            'picture_display': self.picture_display
        }
class Service_Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    intro_text = db.Column(db.String(10000))
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    def to_dict(self):
        return {
            'id': self.id,
            'intro_text': self.intro_text
        }

class Testimonial_Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    testimonial_id = db.Column(db.Integer, db.ForeignKey('testimonial.id'))
   
    def to_dict(self):
        return {
            'id': self.id
        }

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(15000))
    image = db.Column(db.String(10000), default='default.png')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'user_id': self.user_id,
            'description': self.description,
            'image': self.image
        }


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(10000), default='default.png')
    name = db.Column(db.String(150))
    organization = db.Column(db.String(10000), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'image': self.image,
            'organization': self.organization
        }

class User(UserMixin, db.Model,):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now(datetime.UTC))
    portfolio = db.relationship('Portfolio', backref='user', uselist=False)
    projects = db.relationship('Project', backref='user', lazy=True)

    def to_dict(self):
        portfolio = self.portfolio.to_dict() if self.portfolio else None

        return {
            'id': self.id,
            'email': self.email,
            'password': self.password,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'verified': self.verified,
            'created_at': self.created_at,
            'portfolio': portfolio,
            'projects': [project.to_dict() for project in self.projects]
        }
