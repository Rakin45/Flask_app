from flask import Blueprint, jsonify, request, render_template, current_app, url_for, redirect
from datetime import datetime
from .extensions import db  
from .models import User, WaterQualityData, Location
from .schemas import LocationSchema, UserSchema, UploadedDataSchema, VisualisationDataSchema, WaterQualityDataSchema,WaterQualityUpdateDataSchema
from marshmallow import ValidationError
from .model.model import predict_water_qaulity, load_the_model
from .utils import csv_to_dict
import os
from flask_login import current_user,login_required,login_user,logout_user
import pandas as pd


api_bp = Blueprint('api_bp', __name__)

# Create schema instances
location_schema = LocationSchema()
user_schema = UserSchema()
uploaded_data_schema = UploadedDataSchema()
visualisation_data_schema = VisualisationDataSchema()
water_quality_data_schema = WaterQualityDataSchema()

# Create Model instance
model = load_the_model()

def load_location_data_from_excel():
    basedir = os.path.abspath(os.path.dirname(__file__))
    excel_file_name = 'water_quality_locations.xlsx'
    excel_file_path = os.path.join(basedir, excel_file_name)
    df =pd.read_excel(excel_file_path,usecols=['Site number','Site Name','Decimal latitude', 'Decimal longitude'], sheet_name='locations')
    df.columns = ['site_number','location_name', 'latitude', 'longitude']

    # Insert data into database
    records = df.to_dict(orient='records')
    
    return records

def get_location_details(site_number, locations):
    for location in locations:
        print(type(location['site_number']))
        if location['site_number'] == int(site_number):
            return {
                'latitude': location['latitude'],
                'longitude': location['longitude'],
                'location_name': location['location_name']
            }
    # If site number not found, return None or handle accordingly
    return None


location_records = load_location_data_from_excel()

@api_bp.route('/')
def home():
    # Return the homepage
    # data = csv_to_dict()
    root_dir = os.path.dirname(current_app.root_path)
    data_dir = os.path.join(root_dir, 'original_data','dataset_mod.csv')
    data = csv_to_dict(data_dir)
    return render_template('index.html')


@api_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        # print(username, password)

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            response = jsonify(message = "Login successful!", redirectURL=url_for('api_bp.dashboard'))
            return response
        else:
            return jsonify(message="Invalid credentials"), 401

    return render_template('registration/login.html')

@api_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        try:
            data = request.get_json()
            
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')

            # Perform user creation logic (e.g., validation, password hashing, saving to database)
            new_user = User(username=username, email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            # flash('Signup successful!', 'signup_success')
            return jsonify(message="Signup successful!"), 201

        except Exception as e:
            # Handle any errors during user creation (e.g., database errors, validation failures)
            print(f"Error during signup: {e}")
            return jsonify(message="Signup failed", data={username,email,password}), 400

    # Render signup template on GET request
    return render_template('registration/signup.html')


@api_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('api_bp.login'))

@api_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    # Get All the locations
    locations = Location.query.all()
    # Return the user-specific dashboard page content
    return render_template('dashboard/pages/index.html', locations=locations)

@api_bp.route('/upload', methods=['POST'])
@login_required
def upload_data():
    # Receive data and return the prediction
    data = request.json.get('data', None)
    # Data will be processed and a prediction will be made
    prediction_result = {"prediction": 0.75}  # Example output
    return jsonify(prediction_result), 201


@api_bp.route('/profile', methods=['GET', 'PATCH','POST'])
@login_required
def user_profile():

    if request.method == 'GET':
        return render_template('dashboard/pages/profile.html',user=current_user)

    elif request.method == 'PATCH':
        data = request.get_json()
        user = current_user
        
        if 'email' in data:
            user.email = data.get('email')
        if 'password' in data:
            user.set_password(data.get('password'))

        db.session.commit()
        return jsonify(message="Profile updated successfully"), 200

    return jsonify({"message": "User profile page"}), 200


@api_bp.route('/account', methods=['DELETE'])
@login_required
def delete_account():
    user = User.query.filter_by(username=current_user.username).first()
    if not user:
        return jsonify(message="User not found"), 404
    logout_user()
    # Uncommend after testing
    db.session.delete(user)
    db.session.commit()
    response = jsonify(message="success full",success_url=url_for('api_bp.home') )
    return response


@api_bp.route('/history', methods=['GET'])
@login_required
def get_history():
    # Logic to retrieve the history of user uploads and predictions
    return render_template('dashboard/pages/history.html')

# @api_bp.route('/visualization_data', methods=["GET"])
# def visualization_data():
#     root_dir = os.path.dirname(current_app.root_path)
#     data_dir = os.path.join(root_dir, 'original_data','dataset_mod.csv')
#     data = csv_to_dict(data_dir)
#     def format_floats(data):
#         """Formats floats in a dictionary to have two decimal places."""
#         for item in data:    
#             for key, value in item.items():
#                 if isinstance(value, float):
#                     item[key] = float("%.15f" % value)
#         return data
    
#     formatted_data = format_floats(data.copy())
#     print(formatted_data)
#     return jsonify(formatted_data), 200 
 
@api_bp.route('/visualization_data', methods=["POST"])
def visualization_data():
    
    data = request.json

    # Extract form fields

    site_number = data.get('site-number')
    location_data = get_location_details(site_number=site_number,locations=location_records)
    
    
    print(site_number)
    print(location_data)
    
    root_dir = os.path.dirname(current_app.root_path)
    data_dir = os.path.join(root_dir, 'data',f'{site_number}.csv')
    
    df =pd.read_csv(data_dir)
    
    # Define the mapping of old column names to new column names
    column_mapping = {
        'Unnamed: 0': 'Unnamed: 0',
        'Specific conductance, water, unfiltered, microsiemens per centimeter at 25 degrees Celsius (Maximum)': 'spec_cond_max',
        'pH, water, unfiltered, field, standard units (Maximum)': 'ph_max',
        'pH, water, unfiltered, field, standard units (Minimum)': 'ph_min',
        'Specific conductance, water, unfiltered, microsiemens per centimeter at 25 degrees Celsius (Minimum)': 'spec_cond_min',
        'Specific conductance, water, unfiltered, microsiemens per centimeter at 25 degrees Celsius (Mean)': 'spec_cond_mean',
        'Dissolved oxygen, water, unfiltered, milligrams per liter (Maximum)': 'dissolved_oxy_max',
        'Dissolved oxygen, water, unfiltered, milligrams per liter (Mean)': 'dissolved_oxy_mean',
        'Dissolved oxygen, water, unfiltered, milligrams per liter (Minimum)': 'dissolved_oxy_min',
        'Temperature, water, degrees Celsius (Mean)': 'temp_mean',
        'Temperature, water, degrees Celsius (Minimum)': 'temp_min',
        'Temperature, water, degrees Celsius (Maximum)': 'temp_max',
        'Water Quality': 'water_quality',
        'Training': 'training',
        'Location ID': 'location_id',
        'Date': 'date'
    }

    # Rename the columns using the mapping
    df = df.rename(columns=column_mapping)
        
    data = df.to_dict(orient='records')
    
    def format_floats(data):
        """Formats floats in a dictionary to have two decimal places."""
        for item in data:    
            for key, value in item.items():
                if isinstance(value, float):
                    item[key] = float("%.15f" % value)
        return data
    
    formatted_data = format_floats(data.copy())
    # print(formatted_data)
    return jsonify({'plotData':formatted_data,'location':location_data}), 200  
    
@api_bp.route('/water_quality_data', methods=["GET"])
def water_quality_data():
    water_quality_data = db.session.query(WaterQualityData, Location.location_name).join(Location, WaterQualityData.location_id == Location.location_id).all()
    data = [
        {
            'Location ID': row.location_id,
            'Location Name': location,  # Access location name from joined data
            'Date': row.date.strftime('%a, %b %d, %Y'),
            'Spec_Cond_Max': row.spec_cond_max,
            'PH_Max':row.ph_max,
            'PH_Min':row.ph_min,
            'Spec_Cond_Min':row.spec_cond_min,
            'Spec_Cond_Mean':row.spec_cond_mean,
            'Dissolved_Oxy_Max':row.dissolved_oxy_max,
            'Dissolved_Oxy_Mean':row.dissolved_oxy_mean,
            'Dissolved_Oxy_Min':row.dissolved_oxy_min,
            'Temp Mean':row.temp_mean,
            'Temp Min':row.temp_min,
            'Temp Max':row.temp_max,
            'Training':row.training == 1 or row.training == '1',
            'Water Quality':row.water_quality,
            
        }
        for row, location in water_quality_data
    ]

    return jsonify(data),200


@api_bp.route('/predictions', methods=["GET",'POST'])
@login_required
def get_predictions():
    water_quality_data = db.session.query(WaterQualityData, Location.location_name).join(Location, WaterQualityData.location_id == Location.location_id).all()
    data = [
        {
            'Location ID': row.location_id,
            'Location Name': location,  # Access location name from joined data
            'Date': row.date,
            'Spec_Cond_Max': row.spec_cond_max,
            'PH_Max':row.ph_max,
            'PH_Min':row.ph_min,
            'Spec_Cond_Min':row.spec_cond_min,
            'Spec_Cond_Mean':row.spec_cond_mean,
            'Dissolved_Oxy_Max':row.dissolved_oxy_max,
            'Dissolved_Oxy_Mean':row.dissolved_oxy_mean,
            'Dissolved_Oxy_Min':row.dissolved_oxy_min,
            'Temp Mean':row.temp_mean,
            'Temp Min':row.temp_min,
            'Temp Max':row.temp_max,
            'Training':row.training == 1 or row.training == '1',
            'Water Quality':row.water_quality,
           
        }
        for row, location in water_quality_data
    ]
    
    print(data)
    
    return render_template('dashboard/pages/predictions.html', water_quality_data=data)

    return jsonify({"message": "List of predictions"}), 200

@api_bp.route('/make-prediction', methods=['POST'])
@login_required
def make_prediction():
    feature_names = [
        'spec_cond_max',
        'ph_max',
        'ph_min',
        'spec_cond_min',
        'spec_cond_mean',
        'dissolved_oxy_max',
        'dissolved_oxy_mean',
        'dissolved_oxy_min',
        'temp_mean',
        'temp_min',
        'temp_max',
        'training'
    ]
    form_values = request.get_json()
    features = {}
    for feature in feature_names:
        features[feature] = float(form_values.get(feature))
    # data = {'spec_cond_max': 0.0051267056530214,
    #         'ph_max': 0.9102564102564102,
    #         'ph_min': 0.0043614931237721,
    #         'spec_cond_min': 0.00494140625,
    #         'spec_cond_mean': 0.4802631578947368,
    #         'dissolved_oxy_max': 0.878048780487805,
    #         'dissolved_oxy_mean': 0.5303030303030303,
    #         'dissolved_oxy_min': 0.5275590551181103,
    #         'temp_mean': 0.746875,
    #         'temp_min': 0.7467948717948718,
    #         'temp_max': 0.7209302325581396,
    #         'training': 0} # Template
    prediction = predict_water_qaulity(features, model)[0]
    features['water_quality'] = prediction
    features['location_id'] = int(form_values.get('location')) # location 
    features['date'] = str(datetime.now().date().today())# how to save the current data
    # Saving the water_quality_data
    water_quality_data = WaterQualityDataSchema().load(features)
    db.session.add(water_quality_data)
    db.session.commit()
    return jsonify(message="success", prediction=prediction)

@api_bp.route('/predictions/<prediction_id>', methods=['GET'])
@login_required
def get_prediction(prediction_id):
    # Logic to return the details for a given prediction
    return jsonify({"message": f"Details for prediction {prediction_id}"}), 200


@api_bp.route('/insights', methods=['GET'])
@login_required
def get_insights():
    print(location_records)
    # Logic to return insights and trends in water quality data
    return render_template('dashboard/pages/insights.html',locations=location_records)

@api_bp.route('/water-quality/<date>/<location_id>', methods=['PUT'])
@login_required
def update_water_quality(date, location_id):
    try:
        date_object = datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD.'}), 400
    
    schema = WaterQualityUpdateDataSchema()
    try:
        data = schema.load(request.json)
    except ValidationError as e:
        return jsonify({'error': e.messages}), 400

    # location = Location.query.get(location_id)
    location = db.session.get(Location, location_id)
    print(location)
    if not location:
        return jsonify({'error': "Location not found"}), 404
    
    water_quality_data = WaterQualityData.query.filter_by(
        location_id=location_id, date=date_object).first()
    if not water_quality_data:
        return jsonify({'error': "Water quality record not found"}), 404
    if 'spec_cond_max' in data:
        water_quality_data.spec_cond_max = data['spec_cond_max']
    if 'ph_max' in data:
        water_quality_data.ph_max = data['ph_max']
    if 'ph_min' in data:
        water_quality_data.ph_min = data['ph_min']
    if 'spec_cond_min' in data:
        water_quality_data.spec_cond_min = data['spec_cond_min']
    if 'spec_cond_mean' in data:
        water_quality_data.spec_cond_mean = data['spec_cond_mean']
    if 'dissolved_oxy_max' in data:
        water_quality_data.dissolved_oxy_max = data['dissolved_oxy_max']
    if 'dissolved_oxy_mean' in data:
        water_quality_data.dissolved_oxy_mean = data['dissolved_oxy_mean']
    if 'dissolved_oxy_min' in data:
        water_quality_data.dissolved_oxy_min = data['dissolved_oxy_min']
    if 'temp_mean' in data:
        water_quality_data.temp_mean = data['temp_mean']
    if 'temp_min' in data:
        water_quality_data.temp_min = data['temp_min']
    if 'temp_max' in data:
        water_quality_data.temp_max = data['temp_max']
    if 'water_quality' in data:
        water_quality_data.water_quality = data['water_quality']
    if 'training' in data:
        water_quality_data.training = data['training']
    db.session.commit()
    return jsonify({'message': 'Water quality record updated successfully'}), 200