from faker import Faker
import random
import json

# Initialize Faker
fake = Faker()

# Function to generate a single doctor entry
def generate_user_data(id):
    return {
        "id": id,
        "name": f"{fake.first_name()} {fake.last_name()}",
        "email": fake.email(),
        "street_address": fake.street_address(),
        "city": fake.city(),
        "state": fake.state(),
        "postal_code": fake.zipcode(),
        "password": fake.password(),
        "latitude": str(fake.latitude()),
        "longitude": str(fake.longitude())
    }

# Generate 500 rows
data = [generate_user_data(i) for i in range(1, 304)]

# Save to JSON
with open("data/user_data.json", "w") as file:
    json.dump(data, file, indent=4)

print("300 rows of user data generated and saved to 'user_data.json'.")
