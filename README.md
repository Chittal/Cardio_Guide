# MedX-Heart Disease Prediction Webapp

## About

This project is to help user in predicting if they have heart disease or not. If they have heart disease, they can download report and see recommended doctors. The recommendation is based on doctors who treated patients with similar health conditions in user close proximity.
This project is developed using Flask.

## Steps to Run the Website on your System:
1. Download and extract the project zip file.
2. Download and install pgadmin. Also, setup username and password.
3. Create database in postgres.
4. Navigate to project repository in terminal.
5. Create virtual environment using below command.
```
python –m venv venv
```
6. Activate virtual environment using below command.
```
venv/Scripts/activate
```
7. Install requirements using below command.
```
pip install –r requirements.txt
```
8. Generate encryption key using below command.
```
python helper/generate_encryption_key.py
```
9. Create .env file in project and add these values.
```
POSTGRES_USERNAME
POSTGRES_PASSWORD
POSTGRES_HOST
POSTGRES_PORT
POSTGRES_DATABASE
SECRET_KEY=llm
ENCRYPTION_KEY=<encryption key generated in previous step>
PROJECT_PATH=<project whole path>
```
10. Populate database using below command.
```
python helper/populate_data_to_db.py
```
11. Run the application using below command.
```
python app.py
```
12. The application will run in port 5000 in localhost.
https://127.0.0.1:5000/
