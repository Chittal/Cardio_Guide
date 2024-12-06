from faker import Faker
import random
import json

# Initialize Faker
fake = Faker()

# Function to generate a single doctor entry
def generate_doctor_data(id):
    # specialties = ['Cardiologist', 'Cardiac Surgeon', 'Interventional Cardiologist', 'Electrophysiologist']
    # specialty = fake.random_element(elements=specialties)
    return {
        "id": id,
        "name": f"Dr. {fake.first_name()} {fake.last_name()}, MD",
        "rating": round(random.uniform(1.0, 5.0), 1),
        "num_ratings": random.randint(10, 100),
        "phone": fake.phone_number(),
        "speciality": "Cardiologist",
        "practice_name": f"{fake.city()} Health - {fake.last_name()}",
        "street_address": fake.street_address(),
        "city": fake.city(),
        "state": fake.state(),
        "postal_code": fake.zipcode(),
        "latitude": str(fake.latitude()),
        "longitude": str(fake.longitude()),
        "reviews": [
            {
                "date_published": fake.date_between(start_date="-1y", end_date="today").strftime("%b %d, %Y"),
                "rating": random.randint(1, 5),
                "patient_id": random.randint(1, 300)
            } for _ in range(random.randint(1, 10))  # Random number of reviews per doctor
        ]
    }

# Generate 500 rows
data = [generate_doctor_data(i) for i in range(1, 151)]

# Save to JSON
with open("data/doctors_data.json", "w") as file:
    json.dump(data, file, indent=4)

print("150 rows of doctor data generated and saved to 'doctors_data.json'.")
