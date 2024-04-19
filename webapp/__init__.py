from flask import Flask,request
from flask_marshmallow import Marshmallow
from . import models
import os
from .extensions import db,login_manager
import pandas as pd


ma = Marshmallow()

basedir = os.path.abspath(os.path.dirname(__file__))


def create_app(database_uri=None):
    app = Flask(__name__, instance_relative_config=True)
     # Set the template folder path
    app.config['TEMPLATES_FOLDER'] = os.path.join(basedir, 'templates')
    app.config['SECRET_KEY'] = 'h7V4kCJ9ySec4tOQjoik2A'
    
    if database_uri:
        app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(app.instance_path, 'water_quality.sqlite')
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    ma.init_app(app)
    login_manager.init_app(app)

    from webapp.routes import api_bp
    app.register_blueprint(api_bp)
    
    

    def inject_website_name():
        return {"appinfo": {"name":"Water Quality Control"}}
    app.context_processor(inject_website_name)
    
    import logging

    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(filename='app.log', level=logging.INFO, format=log_format)
    
    @app.before_request
    def log_request_info():
        logging.info(f"Request: {request.method} {request.url} - IP: {request.remote_addr}")


    @app.cli.command('init-db')
    def init_db_command():
        db.create_all()
        # Import data from Excel
        excel_file_name = 'water_quality_locations.xlsx'
        excel_file_path = os.path.join(basedir, excel_file_name)
        df =pd.read_excel(excel_file_path,usecols=['Site Name','Decimal latitude', 'Decimal longitude'], sheet_name='locations')
        df.columns = ['location_name', 'latitude', 'longitude']

        # Insert data into database
        records = df.to_dict(orient='records')
        for record in records:
            instance = models.Location(**record)
            db.session.add(instance)

        db.session.commit()
        print('Initialised the database and inserted the location values')

    return app
