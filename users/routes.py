from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.colors import toColor
from datetime import datetime
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

from helper.postgres import select_one_row
from helper.encrypt_utility import SimpleEncryptor

from users.model import Users, db

from flask import session

encryptor = SimpleEncryptor()


def verify_password(password, db_password_hash):
    decrypted = encryptor.decrypt(db_password_hash)
    if decrypted == password:
        return True
    return False


def check_login(email, password):
    """Fetch user record by email from the database."""
    # query = f"SELECT email, password_hash FROM users WHERE email = {email}"
    # user = select_one_row(query)
    # Find the user by email
    user = Users.query.filter_by(email=email).first()
    if user:
        db_password_hash = user.password
        # Verify the provided password against the stored hash
        if verify_password(password, db_password_hash):
            session['name'] = user.name
            session['email'] = user.email
            session['location'] = user.full_address
            session['lat'] = user.latitude
            session['long'] = user.longitude
            return {"success": True, "message": "Login successful!"}
    
    return {"success": False, "message": "Invalid email or password"}


def get_lat_long(address):
    from geopy.geocoders import Nominatim

    # Create a geocoder instance
    geolocator = Nominatim(user_agent="doctor_recommendation")
    location = geolocator.geocode(address)
    if location:
        return location.latitude, location.longitude
    else:
        return None


def check_user_already_exists(email):
    # Check if the email already exists in the database
    existing_user = Users.query.filter_by(email=email).first()
    if existing_user:
        return True
    return False


def create_user(name, email, password, street_address, city, state, postal_code):
    # Create a new User object
    lat, long = get_lat_long(address=f"{street_address}, {city}, {state} - {postal_code}")
    if lat is None or long is None:
        return {"success": False, "message": "Invalid Address"}
    new_user = Users(
        name=name,
        email=email,
        password=encryptor.encrypt(password),
        street_address=street_address,
        city=city,
        state=state,
        postal_code=postal_code,
        latitude=lat,
        longitude=long
    )

    try:
        # Add the user to the database and commit the transaction
        db.session.add(new_user)
        db.session.commit()
        return {"success": True, "message": "User registered successfully."}
    except:
        db.session.rollback()
        return {"success": False, "message": "Error registering user."}
    


def create_buffer_pdf(name, email, location, age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, probability):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    title_style.fontSize = 24
    title_style.fontName = 'Helvetica-Bold'
    title_style.alignment = 1  # Centered title
    title_style.textColor = "#1C304A"  # Set title text color

    normal_style = styles['Normal']
    normal_style.fontSize = 12
    normal_style.fontName = 'Helvetica'
    
    heading_style = styles['Heading2']
    heading_style.fontSize = 14
    heading_style.fontName = 'Helvetica-Bold'

    # Create a list to store the elements of the PDF
    elements = []
    
    # Add logo near the title (adjust path to your logo)
    # Add the logo
    logo_path = 'static/heartcp.png'  # Path to your logo
    logo = Image(logo_path, width=0.5 * inch, height=0.5 * inch)
    logo.hAlign = 'CENTER'
    elements.append(logo)
    elements.append(Spacer(1, 12))  # Add space after logo

    # Add the title
    title = Paragraph("<font size=24><b>CardioGuide</b></font>", title_style)
    elements.append(title)
    elements.append(Spacer(1, 50))  # Add a small space
    
    # Add the contact details
    contact_details = f"""
    <b>Name:</b> {name}<br/>
    <b>Email:</b> {email}<br/>
    <b>Location:</b> {location}
    """
    contact_paragraph = Paragraph(contact_details, normal_style)
    elements.append(contact_paragraph)
    elements.append(Spacer(1, 24))
    
    # Add the prediction result
    prediction_text = f"You have {probability}% chances of heart disease. Please contact nearby hospitals."
    prediction_paragraph = Paragraph(prediction_text, normal_style)
    elements.append(prediction_paragraph)
    elements.append(Spacer(1, 12))
    
    # Add input parameters
    input_data = [
        ["Age", age],
        ["Sex", sex],
        ["Cholesterol", chol],
        ["Blood Pressure", trestbps],
        ["Chest Pain Type", cp],
        ["Fasting Blood Sugar", fbs],
        ["Resting Electrocardiographic Results", restecg],
        ["Max Heart Rate", thalach],
        ["Exercise Induced Angina", exang],
        ["Old Peak", oldpeak],
        ["Slope", slope],
        ["CA", ca],
        ["Thalassemia", thal]
    ]
    
    # Create a table for the input parameters
    data = [["Parameter", "Value"]]  # Table headers
    data.extend(input_data)  # Add input data rows
    
    table = Table(data)
    table.setStyle(TableStyle([ 
        ('BACKGROUND', (0, 0), (-1, 0), toColor("#D3D3D3")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 24))

    # Footer
    footer = f"Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    footer_paragraph = Paragraph(footer, normal_style)
    elements.append(Spacer(1, 24))
    elements.append(footer_paragraph)
    
    # Build the PDF document
    doc.build(elements)
    
    # Move the pointer to the beginning of the buffer
    buffer.seek(0)
    
    return buffer