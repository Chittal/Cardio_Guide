from extensions import db


class Doctor(db.Model):
    __tablename__ = 'doctors'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    num_ratings = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    practice_name = db.Column(db.String(200), nullable=False)
    street_address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    postal_code = db.Column(db.String(20), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    
    def __init__(self, name, rating, num_ratings, phone, practice_name, street_address, city, state, postal_code, latitude, longitude):
        self.name = name
        self.rating = rating
        self.num_ratings = num_ratings
        self.phone = phone
        self.practice_name = practice_name
        self.street_address = street_address
        self.city = city
        self.state = state
        self.postal_code = postal_code
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return f'<Doctor {self.name}>'
