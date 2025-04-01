from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()
DB_NAME = 'folio.db'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'kturgiofjisjclkvdk'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.config['SQLALCHEMY_ECHO'] = True
    app.config['IMG_UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/images')
    app.config['DOC_UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/docs')
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

    # Ensure the upload folder exists
    os.makedirs(app.config['IMG_UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['DOC_UPLOAD_FOLDER'], exist_ok=True)

    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # from .models import Location, User, Portfolio, SocialLink

    create_database(app)    

    return app


def create_database(app):
    if not os.path.exists('backend/' + DB_NAME):
        db.create_all(app=app)
        print("Created Database!")