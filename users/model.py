from extensions import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Unique identifier
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    street_address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    postal_code = db.Column(db.String(20), nullable=False)
    password = db.Column(db.Text, nullable=False)  # Store encrypted password
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    def __init__(self, name, email, street_address, city, state, postal_code, password, latitude, longitude):
        self.name = name
        self.email = email
        self.street_address = street_address
        self.city = city
        self.state = state
        self.postal_code = postal_code
        self.password = password
        self.latitude = latitude
        self.longitude = longitude
    
    @property
    def full_address(self):
        return f"{self.street_address}, {self.city}, {self.state}, {self.postal_code}"
