from . import db
import datetime
from flask_login import UserMixin

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    city = db.Column(db.String(100))
    country = db.Column(db.String(100))
    portfolios = db.relationship('Portfolio', backref='location', lazy=True)

    def to_dict(self):
        return{
            'id': self.id,
            'city': self.city,
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


class User(UserMixin, db.Model,):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    verified = db.Column(db.Boolean, nullable=True, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now(datetime.UTC))
    portfolio = db.relationship('Portfolio', backref='user', uselist=False)

    def to_dict(self):
        portfolio = self.portfolio.to_dict() if self.portfolio else None

        return {
            'id': self.id,
            'email': self.email,
            'password': self.password,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.first_name,
            'verified': self.verified,
            'created_at': self.created_at,
            'portfolio': portfolio
        }