import os
import joblib
import numpy as np

from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder

from doctors.model import Doctor

from flask import session
from math import radians, sin, cos, sqrt, atan2

# Function to calculate Haversine distance
def haversine_distance(loc1, loc2):
    R = 6371.0  # Radius of Earth in kilometers
    lat1, lon1 = loc1
    lat2, lon2 = loc2
    
    # Convert degrees to radians
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    return R * c


def get_close_proximity_doctors(doctors):
    # Example: User's mock location (latitude, longitude)
    user_location = (session['lat'], session['long'])  # Example: San Francisco, CA

    # Step 1: Calculate distances from user to each doctor
    doctor_distances = {}
    for doctor in doctors.values():
        distance = haversine_distance(user_location, (doctor['latitude'], doctor['longitude']))
        doctor_distances[doctor['id']] = distance

    # Step 2: Sort doctors by distance (ascending order)
    sorted_doctors = sorted(doctor_distances.items(), key=lambda x: x[1])

    # Step 4: Select the top 5 closest doctors
    top_5_closest_doctors = sorted_doctors[:5]

    # Output the 5 closest doctors to the user
    closest_doctors = []
    print("\nTop 5 Closest Doctors to the User:")
    for doc_id, distance in top_5_closest_doctors:
        doctor_info = doctors[doc_id]
        doctor_info['distance_km'] = round(distance, 2)  # Add distance to doctor info
        closest_doctors.append(doctor_info)
        print(f"{doctor}: {distance:.2f} km")
    return closest_doctors


def get_recommended_doctors(user_health_params):
    # Normalize the user's health parameters (same scaling as the training data)
    scaler = MinMaxScaler()
    user_health_params_scaled = scaler.fit_transform(user_health_params)

    # 2. Get doctor recommendations from the model
    # Make a prediction for the user (this will give probabilities for each doctor)
    
    location = os.getenv('PROJECT_PATH')
    fullpath = os.path.join(location, 'doctor_recommend.pkl')
    #model = pickle.load(open(fullpath, 'rb'))
    model = joblib.load(fullpath)

    doctor_probabilities = model.predict([user_health_params_scaled, np.zeros((user_health_params.shape[0], 1))])
    print(len(doctor_probabilities[0]), "prob")
    # 3. Sort the probabilities and select the top 5 doctors
    # Get the indices of the top 5 doctors with the highest probabilities
    top_10_doctors = np.argsort(doctor_probabilities[0])[::-1][:10]
    print("top_10_doctors", top_10_doctors)

    # 4. Load the fitted LabelEncoder for doctor IDs
    label_encoder_path = os.path.join(location, 'doctor_label_encoder.pkl')
    label_encoder = joblib.load(label_encoder_path)  # Load the fitted LabelEncoder

    # 4. Convert the indices back to doctor IDs
    recommended_doctors = label_encoder.inverse_transform(top_10_doctors)
    # Convert numpy.int64 to native Python int before querying the database
    recommended_doctors = [int(doctor_id) for doctor_id in recommended_doctors]
    return recommended_doctors


def get_doctors(age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal):
    # 1. Prepare the user's health parameters
    # Let's say these are the user's health parameters
    user_health_params = np.array([[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]])
    
    recommended_doctors = get_recommended_doctors(user_health_params)
    # Output the recommended doctors
    print("Recommended Doctors:", recommended_doctors)

    # Fetch doctors with the given ids
    doctors = Doctor.query.filter(Doctor.id.in_(recommended_doctors)).all()

    if not doctors:
        return {"status": False, "error": "No doctors found", "doctors": []}
    
    # Convert doctors to list of dictionaries
    doctors_list = {}
    for doctor in doctors:
        doctors_list[doctor.id] = {
            'id': doctor.id,
            'name': doctor.name,
            'rating': doctor.rating,
            'phone': doctor.phone,
            'practice_name': doctor.practice_name,
            'street_address': doctor.street_address,
            'city': doctor.city,
            'state': doctor.state,
            'postal_code': doctor.postal_code,
            "latitude": doctor.latitude,
            "longitude": doctor.longitude
        }
    closest_doctors = get_close_proximity_doctors(doctors_list)
    return {"status": True, "doctors": closest_doctors}