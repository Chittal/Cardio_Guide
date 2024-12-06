import pandas as pd
import json

from encrypt_utility import SimpleEncryptor
from postgres import save_to_database


encryptor = SimpleEncryptor()


with open('data/doctors_data.json', 'r') as f:
    doctors_data = json.load(f)

with open('data/user_data.json', 'r') as f:
    user_data = json.load(f)


print('Create doctors table')
doctors_df = pd.DataFrame([{
    "id": data["id"],
    "name": data["name"],
    "rating": data["rating"],
    "num_ratings": data["num_ratings"],
    "phone": data["phone"],
    "speciality": 'Cardiologist',
    "practice_name": data["practice_name"],
    "street_address": data["street_address"],
    "city": data["city"],
    "state": data["state"],
    "postal_code": data["postal_code"],
    "latitude": float(data["latitude"]),
    "longitude": float(data["longitude"])
} for data in doctors_data])
save_to_database(doctors_df, 'doctors', primary_key_column='id')

print('Create users table')
user_df = pd.DataFrame([{
    "id": data["id"],
    "name": data["name"],
    "email": data["email"],
    "street_address": data["street_address"],
    "city": data["city"],
    "state": data["state"],
    "postal_code": data["postal_code"],
    "password": encryptor.encrypt(data["password"]),
    "latitude": float(data["latitude"]),
    "longitude": float(data["longitude"])
} for data in user_data])
save_to_database(user_df, 'users', primary_key_column='id')

print('Create user report table')
patients_data = pd.read_csv('data/hdp_data.csv')
patients_data['user_id'] = range(1, len(patients_data)+1)
patients_data['id'] = range(1, len(patients_data)+1)
save_to_database(patients_data, 'user_report', primary_key_column='id', 
                foreign_keys=[
                    {"column": "user_id", "referenced_table": "users", "referenced_column": "id"}
                ])

print('Create doctor reviews table')
doctor_reviews_df = pd.DataFrame([{
    "doctor_id": d["id"],
    "rating": data["rating"],
    "date_published": data["date_published"],
    "user_id": data["patient_id"]
} for d in doctors_data for data in d.get("reviews", [])])
doctor_reviews_df['id'] = range(1, len(doctor_reviews_df) + 1)
save_to_database(doctor_reviews_df, 'doctor_reviews', primary_key_column='id',  
                foreign_keys=[
                    {"column": "user_id", "referenced_table": "users", "referenced_column": "id"},
                    {"column": "doctor_id", "referenced_table": "doctors", "referenced_column": "id"}
                ])
