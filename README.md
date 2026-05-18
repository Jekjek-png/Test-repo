# RTU - SERVICE SURVEY APPLICATION DOCUMENTATION

 ---

## Project Overview
- RTU-SSA (Service Survey Application) is designed to create a digital feedback system for campus services, which will help cut down on paper forms and make it easier for students, parents, staff, faculty, and service admins to give feedback. The web app only covers four school services/departments and is locally deployed.

---

## Features
- Users can choose the department or service that they have availed service from.
- Rate limiting for survey submissions
- Admins login with assigned service
- Admin dashboard with useful charts and analytics
- Admin can view individual raw response 

---

## Tech Stack
- *Backend*: Python & FastAPI
- *Frontend*: Streamlit & CSS
- *Simulated Data Base*: CSV file
- *Password hashing*: PBKDF2 & SHA-256
- *Libraries*: pandas, pydantic, FastAPI, pathlib, datetime, numpy, hashlib, slowAPI, request, base64, streamlit.

---


## Project Folder Structure
├── backend/
│   ├── Endpoints/
│   │   ├── admin_auth.py
│   │   ├── admin_getdashboard.py
│   │   ├── user_postrespo.py
│   │   ├── user_getservice.py
│   │   └── rate_lim.py
│   └── app.py
├── data/
│   ├── Survey_response.csv
│   ├── Admins.csv
│   └── Services.csv
├── frontend/
│   └── app.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md

---


## Prerequisites
- *Python (3.12.3+)*
- *pip*
- *Virtual environment setup*

---

## How to Setup
- *Clone the repo*
- *Create a virtual environment and activate*
- *pip install requirements.txt* 
- *Include your venv to gitignore*
- *Verify if CSV file exist in the data folder*

---

## CSV File contents 

## 📂 Admins.csv
| username | salt | pwd_hash | service_id |
|----------|------|----------|-------------|

## 📂 Services.csv
| service_id | service_name |
|------------|--------------|

## 📂 Survey_response.csv
| service_id | service_availed | respondent_name | date_of_visit | age_bracket | gender | category_of_respondent | cc1 | cc2 | cc3 | service_satisfaction (1–5) | service_time (1–5) | service_requirements (1–5) | service_steps (1–5) | service_transaction (1–5) | service_fee (1–5 or N/A) | service_fair (1–5) | service_courtesy (1–5) | service_request (1–5) | comments_suggestions | attending_employee | comments_suggestions_for_employee |
|------------|----------------|-----------------|---------------|-------------|--------|------------------------|-----|-----|-----|-----------------------------|--------------------|----------------------------|--------------------|---------------------------|---------------------------|-------------------|-----------------------|----------------------|----------------------|-------------------|----------------------------------|

*Note: Survey_response.csv, Admins.csv, & Services.csv must exist first before deploying locally*

---

## How to deploy the app locally

- *Backend*
    - *cd backend*
        - uvicorn app:app --reload

-  *Frontend*
    - *cd frontend*
        - streamlit run app.py

---

## Admin Accounts Details

## API Reference

## How to Use
- *Students*
    - Select the survey form option
    - Select a Department or service that have been availed
    - Fill up the required fields
    - Click the submit button 
    - The student will be redirected to a landing page
- *Admin*
    - Select the admin login option
    - Input the premade admin credentials
    - navigate
    - filtering
    - raw response

## Validation Rules


## Limitations
- 
- 
- 
- 

## Possible Improvements


## Contributors
