import numpy as np
import joblib
import os

from users.routes import check_login, check_user_already_exists, create_user, create_buffer_pdf
from doctors.route import get_doctors
from extensions import create_app

from flask import render_template , request, jsonify, send_file, session

from dotenv import load_dotenv

load_dotenv()

app = create_app()

@app.route("/",)
def hello():
    return render_template("index.html")


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    resp = check_login(email, password)
    return jsonify(resp)
    

@app.route('/signup')
def signup():
    return render_template('signup.html')  # The signup page you created


@app.route('/signup', methods=['POST'])
def signup_api():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    street_address = data.get("street_address")
    city = data.get("city")
    state = data.get("state")
    postal_code = data.get("postal_code")
    if check_user_already_exists(email):
        return jsonify({"success": False, "message": "Email already registered."})  # User already exists
    resp = create_user(name, email, password, street_address, city, state, postal_code)
    print(resp)
    # users[email] = {"username": username, "password": password}
    return jsonify(resp)


@app.route("/detail", methods = ["GET"])
def submit():
    # Html to py
    # if request.method == "POST":
    #     name = request.form["Username"]

    return render_template("detail.html", n=session['name'])


@app.route('/predict', methods = ["POST"])
def predict():
    # load model
    location = os.getenv('PROJECT_PATH')
    fullpath = os.path.join(location, 'hdp_model.pkl')
    #model = pickle.load(open(fullpath, 'rb'))
    model = joblib.load(fullpath)

    # get params
    age = int(request.form['age'])
    sex = int(request.form['sex'])
    cp = int(request.form['cp'])
    trestbps = int(request.form['trestbps'])
    chol = int(request.form['chol'])
    fbs = int(request.form['fbs'])
    restecg = int(request.form['restecg'])
    thalach = int(request.form['thalach'])
    exang = int(request.form['exang'])
    oldpeak = float(request.form['oldpeak'])
    slope = int(request.form['slope'])
    ca = int(request.form['ca'])
    thal = int(request.form['thal'])
    values = np.array([[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]])
    prediction = model.predict(values)
    # calculate prediction probability for user has heart disease case
    probabilities = model.predict_proba(values)
    probability_of_heart_disease = probabilities[0][1]  # Index 1 for class "1" (heart disease)
    return render_template('predict.html', prediction=prediction, age=age, sex=sex, cp=cp, trestbps=trestbps, chol=chol,
                        fbs=fbs, restecg=restecg, thalach=thalach, exang=exang,
                        oldpeak=oldpeak, slope=slope, ca=ca, thal=thal, probability=probability_of_heart_disease)
    

@app.route('/download_report', methods=['POST'])
def download_report():
    # Capture the parameters from the POST request
    # print(request.form)
    name = session['name']
    email = session['email']
    location = session['location']
    age = request.form['age']
    sex = request.form['sex']
    cp = request.form['cp']
    trestbps = request.form['trestbps']
    chol = request.form['chol']
    fbs = request.form['fbs']
    restecg = request.form['restecg']
    thalach = request.form['thalach']
    exang = request.form['exang']
    oldpeak = request.form['oldpeak']
    slope = request.form['slope']
    ca = request.form['ca']
    thal = request.form['thal']
    probability = request.form['probability']
    probability = round(float(probability) * 100, 2)
     # Create PDF
    pdf_buffer = create_buffer_pdf(name, email, location, age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, probability)
    
    # Return the PDF as a downloadable file
    return send_file(pdf_buffer, as_attachment=True, download_name="heart_disease_report.pdf", mimetype="application/pdf")


@app.route('/find_doctors', methods=['POST'])
def find_doctor():
    # Capture the parameters from the POST request
    # print(request.form)
    name = session['name']
    age = request.form['age']
    sex = request.form['sex']
    cp = request.form['cp']
    trestbps = request.form['trestbps']
    chol = request.form['chol']
    fbs = request.form['fbs']
    restecg = request.form['restecg']
    thalach = request.form['thalach']
    exang = request.form['exang']
    oldpeak = request.form['oldpeak']
    slope = request.form['slope']
    ca = request.form['ca']
    thal = request.form['thal']
    
    resp = get_doctors(age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal)
    return render_template('find_doctors.html', doctors=resp['doctors'], name=name)


if __name__=="__main__":
    app.run(debug=True)
    
