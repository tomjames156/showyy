import datetime
import os
from flask import Blueprint, current_app, request, jsonify, flash, redirect, url_for, render_template
from flask_restful import Resource, marshal_with
from werkzeug.utils import secure_filename
from .models import Location, Portfolio
from .utils import *
from . import db


UPLOAD_FOLDER = '/files/'
views = Blueprint('views', __name__)

@views.route("/")
def start():
    return render_template('home.html')


ALLOWED_EXTENSIONS = ['png', 'pdf', 'jpg', 'jpeg', 'gif']
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@views.route('/pic', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            uploaded_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], uploaded_file.filename))
        return (f"<p>{uploaded_file.filename}</p><img src="
                f"{os.path.join(current_app.config['UPLOAD_FOLDER'], uploaded_file.filename)}>")
    # if request.method == 'POST':
        # check if the post request has the file part
        # if 'file' not in request.files:
        #     flash('No file part')
        #     return redirect(request.url)
        # file = request.files['file']
        # # If the user does not select a file, the browser submits an
        # # empty file without a filename.
        # if file.filename == '':
        #     flash('No selected file')
        #     return redirect(request.url)
        # if file and allowed_file(file.filename):
        #     filename = secure_filename(file.filename)
        #     file.save(os.path.join(UPLOAD_FOLDER, filename))
        #     return f"<p>{filename} Saved</p>"
            # return redirect(url_for('download_file', name=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file accept=".png,.jpg,.jpeg,.gif">
      <input type=submit value=Upload>
    </form>
    '''

@views.route("/locations/", methods=['GET', 'POST'])
def get_locations():
    if request.method == 'GET':
        locations = [location.to_dict() for location in Location.query.all()]
        return jsonify(locations)
    elif request.method == 'POST':
        city = request.form['city']
        country = request.form['country']
        new_location = Location(city=city, country=country)
        db.session.add(new_location)
        db.session.commit()
        return "<p>Locate</p>"


@views.route("/portfolios/", methods=['GET', 'POST'])
def get_portfolios():
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
        portfolios = [portfolio.to_dict() for portfolio in Portfolio.query.all()]
        return jsonify(portfolios)

# class Location(Resource):
#     def get(self):
#         locations = [location for location in Location.query.all()]
#         return locations

#     def post(self):
#         args = location_args.parse_args()
#         print(args)
#         location = Location(city=args['city'], country=args['country'])
#         db.session.add(location)
#         db.session.commit()
#         return "<p>Added Location</p>"


# class Portfolio(Resource):
#     @