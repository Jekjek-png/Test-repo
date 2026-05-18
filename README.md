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

School survey system API endpointsClaude finished the responseYou said: In my web app we plan to deploy locally# RTU_SSA - API CONTRACTS

**BASE URL:** [http://localhost:8000](http://localhost:8000)  
pwede kayo mag base sa lesson na ginawa ni sir

## ENDPOINTS

### 1. SCHOOL SERVICES
- **Method:** GET
- **URL endpoint:** /get_available_services
- **NOTE:** ito yung tatlong gagawan na services
- *pastedIn my web app we plan to deploy locally is a centralized school service survey system, students can answer the survey without creating an account and admins get to login to premade accounts and see the dashboard based on their assigned services what are the api endpoints we needhere is out planned api contractMay 16Claude responded: Based on your API contract document, here's a clear summary of all the endpoints you need:Based on your API contract document, here's a clear summary of all the endpoints you need:
API Endpoints Summary
Base URL: http://localhost:8000

Public Endpoints (No auth needed)
1. GET /get_available_services
Returns the list of 3 services (Accounting, Registrar, Clinic) for the survey form dropdown.
2. POST /submit_survey_response
Accepts the completed survey form from a student. All fields are required. Returns 200 on success, 404 if service ID is invalid, 422 if any field is missing.

Admin Endpoints
3. POST /admin/login
Validates credentials against admins.csv. Returns the admin's assigned_service, which Streamlit must save to st.session_state["service"] for all subsequent calls.
4. GET /admin/summary?service=Accounting
Returns computed analytics — average ratings, total response count, and recent comments/suggestions — for the admin's assigned service. Drives the dashboard charts.
5. GET /responses?service=Accounting
Returns the full list of raw survey responses for a service. Used for the Comments tab in the admin dashboard.
6. GET /admin/export/pdf?service=Accounting
Returns a raw PDF file (not JSON) of all responses for the service. Triggered by the Download PDF button in Streamlit using st.download_button.

Key Rules to Remember

Streamlit never reads/writes CSV directly — everything goes through the API
Ratings must be integers 1–5, FastAPI rejects anything outside that range with 422
After login, always use st.session_state["service"] as the ?service= query param
Run both servers simultaneously — FastAPI on terminal 1, Streamlit on terminal 2

The contract looks solid. The one thing still marked as not final is the survey form fields (the CC1/CC2/CC3 and rating fields), so coordinate with your team once you have the actual paper form to finalize the /submit_survey_response request body.@router.get("/get_available_services")
def get_services():
    if not DATA_FILE.exists():
        raise HTTPException(
            status_code=500,
            detail=f"Services data file not found: {DATA_FILE}"
        )

    services = []
    with DATA_FILE.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            services.append({
                "service_id": row.get("service_id", "").strip(),
                "service_name": row.get("service_name", "").strip(),
            })

    return {"services": services}

Can you explain my code to meShow moreMay 16Claude responded: Sure!Sure! Here's a breakdown of your code:

The Route Decorator
python@router.get("/get_available_services")
This registers the function as a GET endpoint at /get_available_services. When someone visits that URL, this function runs.

File Check
pythonif not DATA_FILE.exists():
    raise HTTPException(
        status_code=500,
        detail=f"Services data file not found: {DATA_FILE}"
    )
Before doing anything, it checks if the CSV file actually exists on disk. If it doesn't, it immediately stops and returns a 500 error with a message telling you which file is missing. This prevents a crash later when trying to open it.

Reading the CSV
pythonservices = []
with DATA_FILE.open(newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        services.append({
            "service_id": row.get("service_id", "").strip(),
            "service_name": row.get("service_name", "").strip(),
        })

services = [] — starts an empty list to collect results
DATA_FILE.open(...) — opens the CSV file safely (auto-closes after the block)
csv.DictReader — reads each row as a dictionary, so you can access columns by name (e.g. row["service_id"]) instead of by index
row.get("service_id", "") — gets the value of that column, and defaults to an empty string if the column doesn't exist, avoiding a KeyError crash
.strip() — removes any accidental whitespace or newlines around the value
Each row gets appended to the services list as a clean dictionary


The Return
pythonreturn {"services": services}
Returns the collected list wrapped in a JSON object, matching your API contract:
json{ "services": [ { "service_id": "...", "service_name": "..." } ] }

In Short
PartWhat it does@router.get(...)Registers the URL routeDATA_FILE.exists()Guards against missing CSVcsv.DictReaderReads CSV rows as named dictionariesrow.get(..., "")Safe column access with a fallback.strip()Cleans up whitespacereturn {...}Sends the JSON responseYou said: in using pydantic, you define the shape of the data or the json format you expect from the frontend right?in using pydantic, you define the shape of the data or the json format you expect from the frontend right?May 16Claude responded: Yes, exactly!Yes, exactly! Pydantic models define the expected shape/structure of incoming data. FastAPI uses them to automatically validate requests.

Simple Example
pythonfrom pydantic import BaseModel

class SurveyResponse(BaseModel):
    service_id: str
    respondent_name: str
    age_bracket: str
    service_satisfaction: int
If the frontend sends this:
json{
    "service_id": "SVC001",
    "respondent_name": "Jake",
    "age_bracket": "18-20",
    "service_satisfaction": 4
}
Pydantic automatically validates it against your model.

What Pydantic does for you
SituationWhat happensAll fields correct✅ Passes through, function runsA required field is missing❌ Auto returns 422 errorWrong data type (e.g. string instead of int)❌ Auto returns 422 errorExtra unexpected fields sent⚠️ Ignored by default

In your project's context
Your /submit_survey_response endpoint would use a Pydantic model to enforce that all those fields in your API contract — service_id, CC1, CC2, ratings, etc. — are present and the correct type before any data gets saved. That's where your 422 - missing required field/s error response comes from automatically.You said: don't give me the code but just give me an idea where to start, I want to add like a validation to my code where I can limit the string characters for like nam…don't give me the code but just give me an idea where to start, I want to add like a validation to my code where I can limit the string characters for like name or service availed and limit the rating to 1-5 only for intMay 16Claude responded: Pydantic actually has built-in tools for exactly that — no need to write manual if-statements.Pydantic actually has built-in tools for exactly that — no need to write manual if-statements.
For string length limits, look into Pydantic's Field() with min_length and max_length parameters. You can attach these directly to your model fields.
For integer range limits, Field() also has ge (greater than or equal) and le (less than or equal) parameters — so for ratings 1–5 you'd combine both.

So your starting point is just Field() from Pydantic — it handles both cases. Look up:

Field(min_length=..., max_length=...) for strings
Field(ge=1, le=5) for integer ranges

FastAPI will then automatically reject any request that violates those rules with a 422 error, no extra code needed on your part.You said: what is the problem with my code why does fastapi throw error 500def service_availed_validator(value: str, max_length: int = 50) -> str:
    if len(value) > max_length:
        raise HTTPException(status_code=422, detail=f"Service availed exceeds character limit of {max_length}.")
    return value


class SuccessResponse(BaseModel):
    Message: str

class SurveyResponse(BaseModel):
    service_id: Annotated[str, AfterValidator(service_id_validator)] 
    service_availed: Annotated[str, AfterValidator(service_availed_validator)]what is the problem with my code why does fastapi throw error 500Show more12:41 AMClaude responded: The problem is you're raising an HTTPException inside a Pydantic validator, and that's the conflict.The problem is you're raising an HTTPException inside a Pydantic validator, and that's the conflict.
Pydantic validators and HTTPException don't mix — Pydantic doesn't know what HTTPException is. When Pydantic catches an unexpected exception inside a validator that it doesn't recognize, it panics and FastAPI surfaces that as a 500 Internal Server Error instead of a clean 422.

The Fix Concept
Inside Pydantic validators, you should raise ValueError instead of HTTPException. Pydantic knows how to handle ValueError — it catches it, formats it, and FastAPI automatically converts it into a proper 422 response.
So the rule is:

Inside a Pydantic validator → raise ValueError
Inside a route function → raise HTTPException


In your case
Replace the HTTPException in service_availed_validator with a ValueError with your error message. Pydantic will handle the rest and FastAPI will return a clean 422 automatically.
Also, as a side note — since you just want a max length limit on a string, this is actually the exact use case for Field(max_length=50) which is simpler and doesn't need a custom validator function at all. Custom validators are better saved for more complex logic.You said: it still throws error 500it still throws error 50012:42 AMClaude responded: Looking at your request data, I can spot the likely culprit —Looking at your request data, I can spot the likely culprit —
"service_fee": "4" is being sent as a string but your model probably expects an int.
Notice all the other rating fields are sent as plain integers (1, 2, 3, 4, 5) but service_fee has quotes around it, making it a string. If your Pydantic model defines service_fee as int, that mismatch could be causing the 500 if your validator is mishandling the type coercion.

Other things to check

"service_id": "SV003" — your services CSV likely has SVC001, SVC002, SVC003. Notice the request is missing the C, so if your service_id_validator does a lookup against the CSV and throws an HTTPException on not found (same problem as before — wrong exception type inside a Pydantic validator), that would also cause a 500.


How to debug quickly
Check your terminal where uvicorn is running — the actual traceback of the error is printed there, not in Swagger. That will tell you the exact line causing the 500, which is much faster than guessing from the response alone.You said: heres the code for you to further understanddef ratings_validator(value: int) -> int:
    if (1 < value > 5) | (value <= 0):
        raise HTTPException (status_code=422, detail=f"Rating value must be between 1 and 5.")
    return value

def ratings_fee_validator(value: str) -> str:
    if value != "N/A":
        try:
            int_value = int(value)
            if (1 < int_value > 5) | (int_value <= 0):
                raise HTTPException(status_code=422, detail=f"Rating value must be between 1 and 5 or 'N/A'.")
        except ValueError:
            raise HTTPException(status_code=422, detail=f"Rating value must be an integer between 1 and 5 or 'N/A'.")
    return value  


def service_id_validator(value: str) -> str:
    if value != "SV001" and value != "SV002" and value != "SV003":
        raise HTTPException(status_code=422, detail=f"Service ID must be one of the following: SV001, SV002, SV003.")
    return value

def service_availed_validator(value: str, max_length: int = 50) -> str:
    if len(value) > max_length:
        raise ValueError(status_code=422, detail=f"Service availed exceeds character limit of {max_length}.")
    return value


class SuccessResponse(BaseModel):
    Message: str

class SurveyResponse(BaseModel):
    service_id: Annotated[str, AfterValidator(service_id_validator)] 
    service_availed: Annotated[str, AfterValidator(service_availed_validator)]
    respondent_name: str
    date_of_visit: str
    age_bracket: str
    gender: str
    category_of_respondent: str
    cc1: str
    cc2: str
    cc3: str
    service_satisfaction: Annotated[int, AfterValidator(ratings_validator)]
    service_time: Annotated[int, AfterValidator(ratings_validator)]
    service_requirements: Annotated[int, AfterValidator(ratings_validator)]
    service_steps: Annotated[int, AfterValidator(ratings_validator)]
    service_transaction: Annotated[int, AfterValidator(ratings_validator)]
    service_fee: Annotated[str, AfterValidator(ratings_fee_validator)]
    service_fair: Annotated[int, AfterValidator(ratings_validator)]
    service_courtesy: Annotated[int, AfterValidator(ratings_validator)]
    service_request: Annotated[int, AfterValidator(ratings_validator)]
    comments_suggestions: str
    attending_employee: str
    comments_suggestions_for_employee: strheres the code for you to further understandShow more12:43 AMClaude responded: I can see multiple issues here:I can see multiple issues here:

Problem 1 — ValueError doesn't accept keyword arguments
pythonraise ValueError(status_code=422, detail=f"...")
ValueError only accepts a plain message string, not status_code or detail. That alone will cause a 500. It should just be:
pythonraise ValueError("Service availed exceeds character limit of 50.")

Problem 2 — Wrong logic in ratings_validator
pythonif (1 < value > 5) | (value <= 0):
This condition is logically broken. 1 < value > 5 means greater than both 1 and 5, which is just value > 5. It won't catch values like 0 or negative numbers properly when combined with the rest. You want to check if the value is outside 1–5, so the condition should be the opposite — check if it's less than 1 or greater than 5.

Problem 3 — All your other validators still use HTTPException
ratings_validator, ratings_fee_validator, and service_id_validator all still raise HTTPException — which as discussed before, causes 500 inside Pydantic. All of them need to raise ValueError instead.

Problem 4 — service_id_validator has wrong IDs
pythonif value != "SV001" and value != "SV002" and value != "SV003":
Your actual service IDs from the API contract are SVC001, SVC002, SVC003 — you're missing the C in all three.

Fix all four of those and your 500 should go away.You said: after the fix it still throws Internal Server Errorafter the fix it still throws Internal Server Error12:46 AMClaude responded: Check your uvicorn terminal and paste the exact traceback here — that's the only way to know for sure what's still failing.Check your uvicorn terminal and paste the exact traceback here — that's the only way to know for sure what's still failing.
But based on your code, one more thing I noticed that we haven't addressed yet:

Possible remaining issue — ratings_fee_validator logic is also broken
Same broken logic pattern:
pythonif (1 < int_value > 5) | (int_value <= 0):
Same problem as before — this doesn't correctly catch values outside 1–5. It also still uses | (bitwise OR) instead of or (logical OR). In Python, you should use or for boolean conditions.

Also double check

Does your route function itself have any logic after receiving the model that could be failing? The validator passing doesn't mean the route function won't crash — if you're writing to a CSV or doing any file operation in the route, that could also be the source of the 500.
Is your DATA_FILE path correct and does the CSV actually exist where your code expects it?


The terminal traceback will pinpoint the exact line. Without it we're just guessing at this point — the 500 could now be coming from somewhere completely different from the validators.You said: when I removed the serviceavailedvalidator it workedwhen I removed the service_availed_validator it worked12:47 AMClaude responded: That makes sense!That makes sense! The issue is this line specifically:
pythonraise ValueError(status_code=422, detail=f"Service availed exceeds character limit of {max_length}.")
Even after switching from HTTPException to ValueError, you kept the keyword arguments status_code and detail — but ValueError doesn't accept those. It only takes a plain string message. So Pydantic itself was crashing trying to raise that ValueError, causing the 500.

So the fix is simply:
pythonraise ValueError(f"Service availed exceeds character limit of {max_length}.")
Just the message string, nothing else.

But also, as mentioned before — since this is just a max length check, you don't even need a custom validator for this at all. You can just use:
pythonservice_availed: Annotated[str, Field(max_length=50)]
That's cleaner, less code, and Pydantic handles it natively without you needing to write or maintain a separate validator function.You said: serviceavailed: Annotated[str, Field(maxlength=50)]service_availed: Annotated[str, Field(max_length=50)]what is the code for this then1:05 AMClaude responded: That's it.pythonfrom pydantic import BaseModel, Field
from typing import Annotated

class SurveyResponse(BaseModel):
    service_availed: Annotated[str, Field(max_length=50)]
That's it. Just make sure Field is imported from pydantic and Annotated is imported from typing. You can remove the service_availed_validator function entirely.You said: in fastapi is it okay to put validators in the basemodel?in fastapi is it okay to put validators in the basemodel?10:27 AMClaude responded: Yes, absolutely!Yes, absolutely! That's actually the recommended and cleaner way to do it in Pydantic/FastAPI.
You can use the @field_validator decorator directly inside your model like this concept:
pythonclass SurveyResponse(BaseModel):
    service_id: str
    service_satisfaction: int

    @field_validator("service_satisfaction")
    def validate_rating(cls, value):
        # your logic here
        return value

Why this is better than separate functions
Separate validator functionsValidators inside the modelDefined outside, easy to lose track ofEverything in one placeHave to wire them with AfterValidator@field_validator handles it automaticallyHarder to read and maintainCleaner and more readableSame function can accidentally be reused wronglyScoped to that model only

One validator for multiple fields
You can also apply one validator to multiple fields at once:
python@field_validator("service_satisfaction", "service_time", "service_steps")
def validate_rating(cls, value):
    # applies to all three fields
    return value
This is much cleaner than what you currently have where you're repeating AfterValidator(ratings_validator) on every single rating field.You said: I did it this way, is this recommended or noef ratings_validator(value: int) -> int:
    if (1 < value > 5) | (value <= 0):
        raise HTTPException (status_code=422, detail=f"Rating value must be between 1 and 5.")
    return value

def ratings_fee_validator(value: str) -> str:
    if value != "N/A":
        try:
            int_value = int(value)
            if (1 < int_value > 5) | (int_value <= 0):
                raise HTTPException(status_code=422, detail=f"Rating value must be between 1 and 5 or 'N/A'.")
        except ValueError:
            raise HTTPException(status_code=422, detail=f"Rating value must be an integer between 1 and 5 or 'N/A'.")
    return value  

def service_id_validator(value: str) -> str:
    if value != "SV001" and value != "SV002" and value != "SV003":
        raise HTTPException(status_code=422, detail=f"Service ID must be one of the following: SV001, SV002, SV003.")
    return value



class SuccessResponse(BaseModel):
    Message: str

class SurveyResponse(BaseModel):
    service_id: Annotated[str, AfterValidator(service_id_validator)] 
    service_availed: Annotated[str, Field(max_length=50)]
    respondent_name: str
    date_of_visit: str
    age_bracket: str
    gender: str
    category_of_respondent: str
    cc1: str
    cc2: str
    cc3: str
    service_satisfaction: Annotated[int, AfterValidator(ratings_validator)]
    service_time: Annotated[int, AfterValidator(ratings_validator)]
    service_requirements: Annotated[int, AfterValidator(ratings_validator)]
    service_steps: Annotated[int, AfterValidator(ratings_validator)]
    service_transaction: Annotated[int, AfterValidator(ratings_validator)]
    service_fee: Annotated[str, AfterValidator(ratings_fee_validator)]
    service_fair: Annotated[int, AfterValidator(ratings_validator)]
    service_courtesy: Annotated[int, AfterValidator(ratings_validator)]
    service_request: Annotated[int, AfterValidator(ratings_validator)]
    comments_suggestions: str
    attending_employee: str
    comments_suggestions_for_employee: strI did it this way, is this recommended or noShow more10:29 AMClaude responded: It works, but it's not the recommended way.It works, but it's not the recommended way. Here are the problems with your current approach:

Problem 1 — Validators are still raising HTTPException
As discussed, all your external validator functions still raise HTTPException instead of ValueError. This will still cause 500 errors when validation fails.
Problem 2 — Broken logic still present
pythonif (1 < value > 5) | (value <= 0):
This is still in your code and is still logically wrong, and uses | instead of or.
Problem 3 — Repetition
pythonservice_satisfaction: Annotated[int, AfterValidator(ratings_validator)]
service_time: Annotated[int, AfterValidator(ratings_validator)]
service_requirements: Annotated[int, AfterValidator(ratings_validator)]
# ...and so on
You're repeating AfterValidator(ratings_validator) 8 times. This is exactly what @field_validator with multiple fields solves.

The cleaner recommended approach
Move everything inside the model using @field_validator:
pythonfrom pydantic import BaseModel, Field, field_validator

class SurveyResponse(BaseModel):
    service_id: str
    service_availed: Annotated[str, Field(max_length=50)]
    service_satisfaction: int
    service_time: int
    # ... rest of fields

    @field_validator("service_id")
    @classmethod
    def validate_service_id(cls, value):
        valid_ids = ["SVC001", "SVC002", "SVC003"]
        if value not in valid_ids:
            raise ValueError("Service ID must be one of: SVC001, SVC002, SVC003.")
        return value

    @field_validator("service_satisfaction", "service_time", "service_requirements",
                     "service_steps", "service_transaction", "service_fair",
                     "service_courtesy", "service_request")
    @classmethod
    def validate_ratings(cls, value):
        if value < 1 or value > 5:
            raise ValueError("Rating must be between 1 and 5.")
        return value

    @field_validator("service_fee")
    @classmethod
    def validate_service_fee(cls, value):
        if value != "N/A":
            try:
                int_value = int(value)
                if int_value < 1 or int_value > 5:
                    raise ValueError("Rating must be between 1 and 5 or 'N/A'.")
            except ValueError:
                raise ValueError("service_fee must be an integer between 1 and 5 or 'N/A'.")
        return value

Comparison
Your current wayRecommended wayValidators defined outside the modelEverything contained inside the modelHTTPException causing 500sValueError handled cleanly by PydanticRepeated AfterValidator(...) 8 timesOne @field_validator covers all rating fieldsBroken condition logicClean value < 1 or value > 5You said: when using field validator how do I call itwhen using field validator how do I call it10:30 AMClaude responded: You don't call it manually — that's the beauty of it.You don't call it manually — that's the beauty of it. Pydantic calls it automatically when data is passed into the model.

How it works
When FastAPI receives a request, it automatically feeds the incoming JSON into your model:
python@router.post("/submit_survey_response")
def submit_survey(survey: SurveyResponse):  # <-- Pydantic validates here automatically
    # if data passes validation, code runs here
    # if it fails, Pydantic returns 422 automatically

The flow
Frontend sends JSON
        ↓
FastAPI receives it
        ↓
Pydantic feeds it into SurveyResponse model
        ↓
@field_validators run automatically
        ↓
  ┌─────┴─────┐
Pass          Fail
  ↓             ↓
Route         422 error
function      returned
runs          automatically
So you just define the validators inside the model and forget about them — they run on every request without you doing anything extra.You said: is it okay if I defined the field validator before the basemodelis it okay if I defined the field validator before the basemodel10:37 AMClaude responded: No, the @field_validator must be inside the class — it's a method of the model, not a standalone function.No, the @field_validator must be inside the class — it's a method of the model, not a standalone function.

What you're thinking of
What CAN be defined outside/before the model are standalone validator functions used with AfterValidator — which is what your original code was doing:
python# this can be outside
def ratings_validator(value: int) -> int:
    ...

class SurveyResponse(BaseModel):
    # then referenced here
    service_satisfaction: Annotated[int, AfterValidator(ratings_validator)]

@field_validator must always be inside
pythonclass SurveyResponse(BaseModel):
    service_satisfaction: int

    @field_validator("service_satisfaction")  # inside the class
    @classmethod
    def validate_ratings(cls, value):
        ...

Summary
ApproachWhere it's definedAfterValidator(fn)Function outside the model, referenced inside@field_validatorAlways inside the model, no exceptions
Both work, but @field_validator inside the model is the cleaner and recommended approach.You said: how do you validate a field with multiple age bracket optionhow do you validate a field with multiple age bracket option10:55 AMClaude responded: For a fixed set of allowed values like age brackets, you just check if the incoming value is in a predefined list:For a fixed set of allowed values like age brackets, you just check if the incoming value is in a predefined list:
python@field_validator("age_bracket")
@classmethod
def validate_age_bracket(cls, value):
    valid_brackets = ["18-20", "21-30", "31-40", "41-50", "51 and above"]
    if value not in valid_brackets:
        raise ValueError(f"Age bracket must be one of: {valid_brackets}")
    return value

But actually, for fixed sets of allowed string values like this, Pydantic has an even cleaner built-in way using Literal from typing:
pythonfrom typing import Literal

class SurveyResponse(BaseModel):
    age_bracket: Literal["18-20", "21-30", "31-40", "41-50", "51 and above"]
No validator function needed at all — Pydantic automatically rejects anything not in that list with a 422 error.

Which to use
SituationUseFixed known optionsLiteral[...] — simpler and cleanerDynamic options (e.g. loaded from CSV)@field_validator with a list
For age brackets specifically, Literal is the better choice since the options never change.You said: how do I validate the date with month/date/year valuehow do I validate the date with month/date/year value11:27 AMClaude responded: For date validation, use @field_validator and datetime.For date validation, use @field_validator and datetime.strptime to check if the value matches your expected format:
pythonfrom datetime import datetime

@field_validator("date_of_visit")
@classmethod
def validate_date(cls, value):
    try:
        datetime.strptime(value, "%d/%m/%Y")
    except ValueError:
        raise ValueError("Date must be in DD/MM/YYYY format.")
    return value

How strptime works
Format codeMeansExample%dDay15%mMonth01%YYear (4 digits)2026
So "%d/%m/%Y" expects exactly 15/01/2026 which matches your API contract format.

What it does

If the date is valid like 15/01/2026 → passes through
If the format is wrong like 2026-01-15 or jan/15/2026 → raises ValueError and Pydantic returns 422 automatically


Alternative
If you want Pydantic to handle dates natively without a custom validator, you can also just change the field type to date from datetime — but then your frontend would need to send it in YYYY-MM-DD format which doesn't match your current API contract, so the strptime approach is safer for your case.You said: I want the value error to be like an httpI want the value error to be like an http11:48 AMClaude responded: You can customize how Pydantic validation errors are returned by adding an exception handler in your FastAPI app:You can customize how Pydantic validation errors are returned by adding an exception handler in your FastAPI app:
pythonfrom fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "detail": exc.errors()[0]["msg"]  # shows only the first error message
        }
    )

What this does
Without the handler, Pydantic returns a long nested error like:
json{
    "detail": [
        {
            "type": "value_error",
            "loc": ["body", "age_bracket"],
            "msg": "Value error, Age bracket must be one of...",
            "input": "999"
        }
    ]
}
With the handler, it returns a clean HTTP-style error like:
json{
    "detail": "Value error, Age bracket must be one of: ['18-20', '21-30']"
}

Import to add
pythonfrom fastapi.exceptions import RequestValidationError
This makes your 422 errors look consistent with your other HTTP error responses like your 404s and 401s.You said: for example is this, I want it to have http error    @field_validator("cc1")
    def validate_cc1(cls, value):
        valid_cc1_ans = ["I know what a CC is and I saw this office's CC", "I know what a CC is but I did not see this office's CC", "I learned of the CC only when I saw this office's CC", "I do not know what a CC is and did not see one in this office" ]
        if value not in valid_cc1_ans:
            raise ValueError ("Answer must be in one of the choices.")
        elif value.strip() == "":
            raise ValueError("This field cannot be empty.")
        return valuefor example is this, I want it to have http errorShow more11:50 AMClaude responded: Your elif for empty string will never trigger because if the value is empty it won't be in validcc1ans anyway, so the first if catches it first.Your elif for empty string will never trigger because if the value is empty it won't be in valid_cc1_ans anyway, so the first if catches it first.

But for your main question, you don't need to change anything inside the validator itself. The exception handler we just discussed handles it globally — just raise ValueError as normal and the handler converts it automatically to a clean HTTP response:
python@field_validator("cc1")
@classmethod
def validate_cc1(cls, value):
    valid_cc1_ans = [
        "I know what a CC is and I saw this office's CC",
        "I know what a CC is but I did not see this office's CC",
        "I learned of the CC only when I saw this office's CC",
        "I do not know what a CC is and did not see one in this office"
    ]
    if value not in valid_cc1_ans:
        raise ValueError("Answer must be one of the valid choices.")
    return value
Then your exception handler in main.py takes care of formatting it like:
json{
    "detail": "Value error, Answer must be one of the valid choices."
}

Summary

Keep raising ValueError inside validators — don't change that
The exception handler is the one responsible for making it look like an HTTP error response
You only need to write the handler once and it applies to all your validators automatically
You said: what should be in my main.what should be in my main.py import11:51 AMClaude responded: For your main.For your main.py, here are the imports you need:
pythonfrom fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

What each one does
ImportPurposeFastAPIcreates your app instanceRequestrequired parameter in the exception handler functionJSONResponseformats the return as a JSON HTTP responseRequestValidationErrorthe exception type that Pydantic triggers on validation failureYou said: this is my importsthis is my imports11:52 AMClaude responded: Your imports look good, but a few things to note:Your imports look good, but a few things to note:

app.py — missing one import
pythonfrom fastapi import FastAPI, Request  # Request is needed for the exception handler
You have FastAPI and Request already — ✅ good. JSONResponse and RequestValidationError are there too — ✅ good.
But you're missing the exception handler function itself in app.py. Having the imports isn't enough, you need to actually add:
python@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()[0]["msg"]}
    )

post_res.py — AfterValidator can be removed
pythonfrom pydantic import BaseModel, AfterValidator, Field, field_validator
Since you're moving to @field_validator inside the model, you no longer need AfterValidator — you can clean that up.
Also HTTPException is still imported — make sure you're only using it inside route functions, not inside validators.

Annotated import
Make sure you also have this in post_res.py:
pythonfrom typing import Annotated
You need it if you're still using Annotated for Field(max_length=50) on service_availed.You said: this is my updated codefrom pathlib import Path
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, AfterValidator, Field, field_validator
import csv
from datetime import datetime

router = APIRouter()

DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "Survey_response.csv"



pastedthis is my updated code11:54 AMClaude responded: Your code is looking much better!Your code is looking much better! Here are the remaining issues I can spot:

Problem 1 — Missing @classmethod on all validators
python@field_validator("service_satisfaction", ...)
def validate_rating(cls, value):  # missing @classmethod
Every @field_validator needs @classmethod above it, otherwise Pydantic will throw a warning or error in newer versions:
python@field_validator("service_satisfaction", ...)
@classmethod
def validate_rating(cls, value):

Problem 2 — elif after list check will never trigger
You have this pattern in multiple validators:
pythonif value not in valid_cc1_ans:
    raise ValueError("...")
elif value.strip() == "":  # this will NEVER run
    raise ValueError("...")
If the value is empty, it already fails the first if check. Swap the order — check for empty first:
pythonif value.strip() == "":
    raise ValueError("This field cannot be empty.")
if value not in valid_cc1_ans:
    raise ValueError("Answer must be one of the choices.")
This applies to cc1, cc2, cc3, gender, age_bracket, category_of_respondent, and service_id.

Problem 3 — Service IDs are still wrong
pythonif value != "SV001" and value != "SV002" and value != "SV003":
Your API contract says SVC001, SVC002, SVC003 — still missing the C. Also cleaner to write as:
pythonif value not in ["SVC001", "SVC002", "SVC003"]:

Problem 4 — validate_service_fee swallows the ValueError
pythontry:
    fee_value = int(value)
    if not (1 <= fee_value <= 5):
        raise ValueError("Service fee rating must be between 1 and 5 or 'N/A'.")
except ValueError:
    raise ValueError("Service fee must be an integer between 1 and 5 or 'N/A'.")
The except ValueError catches both the int() conversion failure AND your own raise ValueError inside the try block, so your range error message will never show — it always falls to the generic message. Fix by separating them:
pythonif not value.isdigit():
    raise ValueError("Service fee must be an integer between 1 and 5 or 'N/A'.")
if not (1 <= int(value) <= 5):
    raise ValueError("Service fee rating must be between 1 and 5 or 'N/A'.")

Everything else looks good ✅

Rating logic 1 <= value <= 5 is now correct
date_of_visit format validation is correct
CSV writing logic looks clean
HTTPException is only used in the route function, not in validators
You said: how about now    @field_validator("service_satisfaction", "service_time", "service_requirements", "service_steps", "service_transaction", "service_fair", "service_courtesy", "service_request")
    @classmethod
    def validate_rating(cls, value):
        if not (1 <= value <= 5):
            raise ValueErrorpastedhow about now12:03 PMClaude responded: This is much cleaner!This is much cleaner! Only two remaining issues:

Problem 1 — validate_service_fee still swallows the ValueError
This is the same issue from before, still not fixed:
pythontry:
    fee_value = int(value)
    if not (1 <= fee_value <= 5):
        raise ValueError("Service fee rating must be between 1 and 5 or 'N/A'.")
except ValueError:  # this catches your own ValueError above too
    raise ValueError("Service fee must be an integer between 1 and 5 or 'N/A'.")
Fix it like this:
pythonif not value.isdigit():
    raise ValueError("Service fee must be an integer between 1 and 5 or 'N/A'.")
if not (1 <= int(value) <= 5):
    raise ValueError("Service fee rating must be between 1 and 5 or 'N/A'.")

Problem 2 — Service IDs still missing the C
pythonvalid_service_id = ["SV001", "SV002", "SV003"]
Should be:
pythonvalid_service_id = ["SVC001", "SVC002", "SVC003"]

Everything else looks good now — @classmethod is on all validators, empty checks come before list checks, and the logic is clean. Good job!You said: our get survey response by service responds with thisour get survey response by service responds with this
    Details
200    
Response body
Download
{
  "status": "success",
  "total_responses": 3,
  "data": [
    {
      "service_id": "SV001",
      " service_Availed": "Enrollment form",
      " respondent_name": "Jake",
      " date_of_visit": "15/05/2026",
      " age_bracket": "18-20",
      " gender": "Male",
      " category_of_respondent": "Student",
      " cc1": "yes",
      " cc2": "yes",
      " cc3": "yes",
      " service_satisfaction(1-5)": "4",
      " service_time(1-5)": "4",
      " service_requirements(1-5)": "5",
      " service_steps(1-5)": "2",
      " service_transaction(1-5)": "3",
      " service_fee(1-5 or N/A)": "N/A",
      " service_fair(1-5)": "4",
      " service_courtesy(1-5)": "4",
      " service_request(1-5)": "4",
      " comments_suggestions": "N/A",
      " attending_employee": "Fey",
      " comments_suggestions_for_employee": "mabait"
    },
    {
      "service_id": "SV001",
      " service_Availed": "Enrollment Form.",
      " respondent_name": "Jake Pasaway mode",
      " date_of_visit": "17/05/2026",
      " age_bracket": "17-20",
      " gender": "Male",
      " category_of_respondent": "Student",
      " cc1": "I do not know what a CC is and did not see one in this office",
      " cc2": "N/A",
      " cc3": "N/A",
      " service_satisfaction(1-5)": "4",
      " service_time(1-5)": "3",
      " service_requirements(1-5)": "4",
      " service_steps(1-5)": "1",
      " service_transaction(1-5)": "4",
      " service_fee(1-5 or N/A)": "5",
      " service_fair(1-5)": "2",
      " service_courtesy(1-5)": "4",
      " service_request(1-5)": "1",
      " comments_suggestions": "Lorem ipsum dolor sit amet, consectetuer adipiscing el",
      " attending_employee": "Fey mabait",
      " comments_suggestions_for_employee": "Lorem i,"
    },
    {
      "service_id": "SV001",
      " service_Availed": "Enrollment Form.",
      " respondent_name": "Jake Pasaway mode",
      " date_of_visit": "17/05/2026",
      " age_bracket": "17-20",
      " gender": "Male",
      " category_of_respondent": "Student",
      " cc1": "I learned of the CC only when I saw this office's CC",
      " cc2": "N/A",
      " cc3": "N/A",
      " service_satisfaction(1-5)": "4",
      " service_time(1-5)": "3",
      " service_requirements(1-5)": "4",
      " service_steps(1-5)": "1",
      " service_transaction(1-5)": "4",
      " service_fee(1-5 or N/A)": "5",
      " service_fair(1-5)": "2",
      " service_courtesy(1-5)": "4",
      " service_request(1-5)": "1",
      " comments_suggestions": "Lorem ipsum dolor sit amet, consectetuer adipiscing el",
      " attending_employee": "Fey mabait",
      " comments_suggestions_for_employee": "Lorem i,"
    }
  ]
}is it our responsibility to like format how it is displayed in the front end, like  what we want to happend is like display all the survey forms in the frontend in a like seperate paperShow more1:29 PMClaude responded: Yes!Yes! How the data is displayed is entirely the frontend's responsibility. Your backend's job is done — it returns the data correctly.

How the responsibilities are split
Backend (your FastAPI)Frontend (Streamlit)Returns the raw JSON dataLoops through the data arrayDoesn't care how it looksFormats each response as a "paper/card"Just serves the dataDecides layout, colors, spacing

What Streamlit would do
It would call your /responses?service=Accounting endpoint, get that JSON, then loop through each item in data and display it as a separate card — something like using st.container() or st.expander() per response to make it look like individual paper forms.

One thing to flag though
Looking at your response data, your CSV headers have a leading space before most field names:
json" service_Availed": "Enrollment form",  // notice the space before service_Availed
" respondent_name": "Jake",
That's a CSV formatting issue on the backend side — your CSV columns likely have spaces at the start. That will cause problems when the frontend tries to access fields by name like response["respondent_name"] — it won't find it because the actual key is " respondent_name" with a space.
That's worth fixing on the backend before moving to the frontend.You said: what I want to happen is when the admin logs in it passes a request name and password to the api, the api compares it againts what is in the csv, in the csv th…what I want to happen is when the admin logs in it passes a request name and password to the api, the api compares it againts what is in the csv, in the csv theres an assigned service for each admin accounts registered,. when authentication is successful, it proceeds to the admin dashboard, in the admin dashboard admin_sum api will be called to display the analytics of total respondents, and there will be a tab in the admin dashboard where it will call the get response by service api and the admin can see all the raw respondents formhow should i structure it2:19 PMClaude responded: Here's how to structure it:Here's how to structure it:

Backend Structure
You already have the endpoints needed:
/admin/login          → authenticates, returns assigned_service
/admin/summary        → returns analytics for the dashboard
/responses            → returns raw survey forms for the tab

Frontend Flow
Login Page
    ↓
POST /admin/login
    ↓
Save to session state:
    st.session_state["logged_in"] = True
    st.session_state["service"] = assigned_service
    ↓
Redirect to Dashboard Page

Dashboard Page Structure
Dashboard (uses st.session_state["service"] for all API calls)
    │
    ├── Summary Section
    │       ↓
    │   GET /admin/summary?service={service}
    │   displays: total respondents, average ratings, charts
    │
    └── Tabs
            ├── Tab 1: Analytics  ← summary data displayed here
            └── Tab 2: Responses
                        ↓
                    GET /responses?service={service}
                    loops through data array
                    displays each form as a card/expander

Streamlit File Structure
frontend/
    pages/
        01_login.py       ← login form, calls /admin/login
        02_dashboard.py   ← protected page, calls summary + responses

Key Rules

Every page should check st.session_state["logged_in"] at the top — if not logged in, redirect back to login
Never hardcode the service name — always use st.session_state["service"]
All API calls go through httpx or requests, never direct CSV access
You said: this is the get response is it enoughfrom pathlib import Path
from fastapi import APIRouter, HTTPException
import csv

router = APIRouter()

SURVEY_FILE = Path(__file__).resolve().parents[2] / "data" / "Survey_response.csv"

@router.get("/get_service_responses/{service_id}")
def get_responses_by_service(service_id: str):
    if not SURVEY_FILE.exists():
        raise HTTPException(status_code=500, detail="Survey response data file not found")


    matching_responses = []

    with SURVEY_FILE.open(mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:

            if row.get("service_id", "").strip() == service_id:
                matching_responses.append(row)
    
    if len(matching_responses) == 0:
        raise HTTPException(status_code=404, detail=f"No survey responses found yet for Service/Department")

    return {
        "status": "success",
        "total_responses": len(matching_responses),
        "data": matching_responses
    }this is the get response is it enoughShow more2:21 PMClaude responded: The code works but there are a few things to improve:The code works but there are a few things to improve:

Problem 1 — Route uses service_id but API contract uses service as query parameter
Your current route:
/get_service_responses/{service_id}  ← path parameter
Your API contract says:
/responses?service=Accounting  ← query parameter
These are different. It should be a query parameter, not a path parameter:
python@router.get("/responses")
def get_responses_by_service(service: str):

Problem 2 — Filtering by service_id but contract filters by service name
Your CSV likely has both service_id and service_name. The contract says /responses?service=Accounting — so you should be filtering by service name, not service ID.

Problem 3 — Leading spaces in CSV keys
As mentioned before, your CSV has leading spaces in column names like " service_Availed". Add .strip() when building the response:
pythonclean_row = {key.strip(): value.strip() for key, value in row.items()}
matching_responses.append(clean_row)

Problem 4 — Missing 422 for missing parameter
If someone calls /responses without ?service=, FastAPI handles this automatically if you define it as a query parameter — no extra code needed.

Suggested fix structure
python@router.get("/responses")
def get_responses_by_service(service: str):
    # your existing logic but filter by service name
    # and clean the row keys with strip()You said: this is the adminacc.this is the adminacc.csvusername,salt,pwd_hash,service_id
accAdmin,e106beec85b9070ff98966e723715d72,325ef825986deb2b79fc7673bbddbb07b32ce5e8d0ca6fb37aa7b645c871b405,SV001
registrarAdmin,b320e8da33aa3d2153f6922a57512b91,cb8f31b0d474ebb2c3c44a15056fc2ce6f980dcc04426295b0f1730441cab19f,SV002
clinicAdmin,9695c544b25591c4588f3b728e6ac5a5,eeea6ebe563f71065def504bfaa3dfc03cd567299a380a701cf0949b15b6935a,SV003here is the services.csv2:26 PMClaude responded: BasedBasedClaude's response was interrupted.Try againthis is the adminacc.csv

username,salt,pwd_hash,service_id
accAdmin,e106beec85b9070ff98966e723715d72,325ef825986deb2b79fc7673bbddbb07b32ce5e8d0ca6fb37aa7b645c871b405,SV001
registrarAdmin,b320e8da33aa3d2153f6922a57512b91,cb8f31b0d474ebb2c3c44a15056fc2ce6f980dcc04426295b0f1730441cab19f,SV002
clinicAdmin,9695c544b25591c4588f3b728e6ac5a5,eeea6ebe563f71065def504bfaa3dfc03cd567299a380a701cf0949b15b6935a,SV003
here is the services.csv

service_id,service_name
SV001,Accounting
SV002,Registrar
SV003,Clinic

and survey_response.csv
service_id,service_availed,respondent_name,date_of_visit,age_bracket,gender,category_of_respondent,cc1,cc2,cc3,service_satisfaction(1-5), service_time(1-5),service_requirements(1-5),service_steps(1-5),service_transaction(1-5),service_fee(1-5 or N/A),service_fair(1-5),service_courtesy(1-5),service_request(1-5),comments_suggestions,attending_employee,comments_suggestions_for_employee
SV001,Enrollment form,Jake,15/05/2026,18-20,Male,Student,yes,yes,yes,4,4,5,2,3,N/A,4,4,4,N/A,Fey,mabait
SV003,Enrollment form,JEKJEK,15/05/2026,18-20,Male,Student,yes,yes,yes,5,5,5,5,5,5,5,5,4,N/A,Fey mam,mabait
SV003,Enrollment form,Elijahh,15/05/2026,18-20,Male,Student,yes,yes,yes,5,5,5,5,5,5,5,5,4,N/A,Fey mam,mabait
SV001,Enrollment Form.,Jake Pasaway mode,17/05/2026,17-20,Male,Student,I do not know what a CC is and did not see one in this office,N/A,N/A,4,3,4,1,4,5,2,4,1,"Lorem ipsum dolor sit amet, consectetuer adipiscing el",Fey mabait,"Lorem i,"
SV001,Enrollment Form.,Jake Pasaway mode,17/05/2026,17-20,Male,Student,I learned of the CC only when I saw this office's CC,N/A,N/A,4,3,4,1,4,5,2,4,1,"Lorem ipsum dolor sit amet, consectetuer adipiscing el",Fey mabait,"Lorem i,"


here is the current getresponse api
from pathlib import Path
from fastapi import APIRouter, HTTPException
import csv

router = APIRouter()

SURVEY_FILE = Path(__file__).resolve().parents[2] / "data" / "Survey_response.csv"

@router.get("/responses")
def get_responses_by_service(service: str):
    if not SURVEY_FILE.exists():
        raise HTTPException(status_code=500, detail="Survey response data file not found")

    matching_responses = []

    with SURVEY_FILE.open(mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:

            if row.get("service_id", "").strip() == service.strip():
                matching_responses.append(row)
    
    if len(matching_responses) == 0:
        raise HTTPException(status_code=404, detail=f"No survey responses found yet for Service/Department")

    return {
        "status": "success",
        "total_responses": len(matching_responses),
        "data": matching_responses
    }Show more2:27 PMClaude responded: Looking at your CSVs and current code, here are the issues:Looking at your CSVs and current code, here are the issues:

Problem 1 — Filtering by wrong value
Your API contract says /responses?service=Accounting — so the frontend passes a service name. But your code compares against service_id in the CSV. You need to:

Look up the service_name in services.csv to get the matching service_id
Then filter survey_response.csv using that service_id


Problem 2 — Leading space in CSV headers
Looking at your survey_response.csv:
service_id,service_availed,...,service_satisfaction(1-5), service_time(1-5)
There's a space before service_time(1-5) and likely others. That's why your response was returning " service_time(1-5)" with a leading space. Fix it by stripping keys:
pythonclean_row = {key.strip(): value.strip() for key, value in row.items()}

Problem 3 — 404 when service name doesn't exist vs no responses yet
Right now if someone passes ?service=InvalidName it returns the same 404 as "no responses yet" — these should be different errors. First validate the service name exists, then check for responses.

Suggested structure
pythonSURVEY_FILE = Path(__file__).resolve().parents[2] / "data" / "Survey_response.csv"
SERVICES_FILE = Path(__file__).resolve().parents[2] / "data" / "services.csv"

@router.get("/responses")
def get_responses_by_service(service: str):
    # Step 1 - validate service name and get its service_id
    service_id = None
    with SERVICES_FILE.open(mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["service_name"].strip().lower() == service.strip().lower():
                service_id = row["service_id"].strip()
                break

    if service_id is None:
        raise HTTPException(status_code=404, detail=f"Service '{service}' not found.")

    # Step 2 - filter survey responses by service_id
    matching_responses = []
    with SURVEY_FILE.open(mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            clean_row = {key.strip(): value.strip() for key, value in row.items()}
            if clean_row.get("service_id", "") == service_id:
                matching_responses.append(clean_row)

    if len(matching_responses) == 0:
        raise HTTPException(status_code=404, detail=f"No survey responses found yet for '{service}'.")

    return {
        "status": "success",
        "service": service,
        "total_responses": len(matching_responses),
        "data": matching_responses
    }

Also fix your survey_response.csv
Remove the space before service_time(1-5) in the header row — that's a data quality issue that will keep causing problems.You said: in this code I want to remove the option where you need to input specific date like today lastweekfrom pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from .admin_auth import verify_admin_access

router = APIRouter()

DATA_FILE = Path(__file__).resolve().parents[2] / "data" /pastedin this code I want to remove the option where you need to input specific date like today lastweek3:17 PMClaude responded: You just need to remove the preset_range parameter and all the date filtering logic from both functions.You just need to remove the preset_range parameter and all the date filtering logic from both functions. Here's what to delete:

In both Service_response_summary and Raw_service_responses, remove:
1. The parameter from the function signature:
python# remove this
preset_range: str = Query(None, description="Preset date range. Options: 'today', 'last_week', 'last_month', 'current_year', 'last_year'")
2. The entire date preset logic block:
python# remove all of this
sd_obj = None
ed_obj = None
current_date = datetime.now()

if preset_range:
    preset_range = preset_range.lower().strip()
    
    preset_map = {
        "today": ...
        ...
    }
    
    if preset_range in preset_map:
        sd_obj, ed_obj = preset_map[preset_range]
    else:
        raise HTTPException(...)
3. The date filtering block:
python# remove all of this
if not df.empty and (sd_obj or ed_obj):
    if 'date_of_visit' in df.columns:
        ...
4. In the return statement, remove:
python"active_filter": preset_range if preset_range else "all",  # remove this line

Also clean up imports
Since you're removing date filtering, these are no longer needed:
pythonfrom datetime import datetime, timedelta  # remove timedelta, keep datetime only if used elsewhere
from fastapi import Query  # remove QueryYou said: by default I want it to display the total summary, then have an option to filter it by day or weekfrom pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from .admin_auth import verify_admin_access

router = APIRouter()

DATA_FILE = Path(__file__).resolve().parents[2] / "data" /pastedby default I want it to display the total summary, then have an option to filter it by day or week3:22 PMClaude responded: So you want to keep the filtering but make it optional — defaulting to all data when no filter is selected.So you want to keep the filtering but make it optional — defaulting to all data when no filter is selected. Your code actually already does this since preset_range defaults to None. The issue is just the "today" preset logic is off.

Problem — "today" is wrong
python"today": (current_date - timedelta(days=1), current_date),
This gives you the last 24 hours, not today specifically. It should be:
python"today": (current_date.replace(hour=0, minute=0, second=0, microsecond=0), current_date),
This sets the start to midnight of today instead of 24 hours ago.

What to change in both functions
1. Keep the parameter but make the default behavior clearer:
pythonpreset_range: str = Query(None, description="Options: 'today', 'last_week', 'last_month', 'current_year', 'last_year'. Leave empty for all responses.")
2. Fix the "today" preset in preset_map:
python"today": (current_date.replace(hour=0, minute=0, second=0, microsecond=0), current_date),
3. In the return statement, make active_filter more readable:
python"active_filter": preset_range if preset_range else "all_time",

The flow then becomes
No filter passed  → returns all responses (default)
?preset_range=today       → filters to today only
?preset_range=last_week   → filters to last 7 days
Everything else in your code is already structured correctly for this — the date filtering block only runs if not df.empty and (sd_obj or ed_obj), so when no filter is passed, sd_obj and ed_obj stay None and it skips filtering entirely.You said: is the get services necessary herefrom pathlib import Path
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import csv
import hashlib

router = APIRouter()

# PATH SETUP 
DATA_DIR = Path(__file__).resolve().parents[2] / "data" 
ADMINS_FILE = DATA_DIR / "Admins.csv"
SERVICES_FILE = DATA_DIR / "Services.csv"

# PYDANTIC MODELS
class LoginCredentials(BaseModel):
    username: str
    password: str

# PASSWORD HASHING LOGIC
def _hash_password(password: str, salt: bytes) -> bytes:
    """Hashes the password using PBKDF2 with SHA-256."""
    return hashlib.pbkdf2_hmac(
        'sha256', 
        password.encode('utf-8'), 
        salt, 
        100000
    )

# VALIDATION LOGIC 
def verify_admin_access(credentials: LoginCredentials):
  
    if not ADMINS_FILE.exists() or not SERVICES_FILE.exists():
        raise HTTPException(
            status_code=500, 
            detail="Database Error: CSV files are missing."
        )

    is_authenticated = False
    authorized_service_id = ""

    # 1. Admin Authentication
    with ADMINS_FILE.open(mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row.get("username", "").strip() == credentials.username:
                salt_hex = row.get("salt", "").strip()
                hash_hex = row.get("pwd_hash", "").strip()
                
                if salt_hex and hash_hex:
                    try:
                        stored_salt = bytes.fromhex(salt_hex)
                        stored_hash = bytes.fromhex(hash_hex)
                        login_hash = _hash_password(credentials.password, stored_salt)
                        
                        if stored_hash == login_hash:
                            is_authenticated = True
                            authorized_service_id = row.get("service_id", "").strip()
                    except ValueError:
                        pass 
                
                break 

    if not is_authenticated:
        raise HTTPException(
            status_code=401, 
            detail="Invalid username or password."
        )

    assigned_service_name = "Unknown Service"
    with SERVICES_FILE.open(mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row.get("service_id", "").strip() == authorized_service_id:
                assigned_service_name = row.get("service_name", "").strip()
                break

    return {
        "username": credentials.username,
        "service_id": authorized_service_id,
        "service_name": assigned_service_name
    }

# ENDPOINTS

@router.post("/login")
def login_admin(verified_user: dict = Depends(verify_admin_access)):
    return {
        "message": "Login successful.", 
        **verified_user  
    }

@router.get("/services")
def get_services():
    """Reads Services.csv on the fly and returns the available services."""
    if not SERVICES_FILE.exists():
        raise HTTPException(status_code=500, detail="Database error: Services.csv file not found.")
        
    services = []
    with SERVICES_FILE.open(mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            s_id = row.get("service_id", "").strip()
            s_name = row.get("service_name", "").strip()
            if s_id and s_name:
                services.append({"service_id": s_id, "service_name": s_name})
                
    return {"services": services}is the get services necessary hereShow more3:38 PMClaude responded: No, it's not necessary here.No, it's not necessary here. The /get_available_services endpoint already exists in your get_service.py file which does the exact same thing.
Having it here creates two problems:

Problem 1 — Duplicate endpoint
You'd have two routes doing the same thing:
/get_available_services  ← already exists in get_service.py
/services                ← this one here
That's redundant and confusing to maintain.

Problem 2 — Wrong file to put it in
This file is admin_auth.py — its only responsibility should be authentication. A public endpoint like getting available services doesn't belong here.

What to keep in this file
This file should only have:

verify_admin_access — the dependency function
POST /login — the login endpoint

Just remove the /services endpoint entirely from here and rely on the existing /get_available_services route.You said: isn't it used to map the admin account to a serviceisn't it used to map the admin account to a service3:39 PMClaude responded: No, the mapping between admin and service is already handled inside verifyadminaccess — specifically this part:No, the mapping between admin and service is already handled inside verify_admin_access — specifically this part:
python# looks up the service name using the service_id from Admins.csv
with SERVICES_FILE.open(mode="r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        if row.get("service_id", "").strip() == authorized_service_id:
            assigned_service_name = row.get("service_name", "").strip()
            break
So the flow is already:
Login credentials sent
        ↓
Admins.csv → finds the admin's service_id
        ↓
Services.csv → maps service_id to service_name
        ↓
Returns { service_id, service_name } in the verified_user dict
The /services GET endpoint you have is a completely separate thing — it's for listing all available services publicly, which is already done by /get_available_services. It plays no role in the admin-to-service mapping at all.You said: why use post on the service raw response, when you are just returning the raw responses to the frontendfrom pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from .admin_auth import verify_admin_access

router = APIRouter()

DATA_FILE = Path(__file__).resolve().parents[2] / "data" /pastedwhy use post on the service raw response, when you are just returning the raw responses to the frontend3:48 PMClaude responded: You're right — it should be GET.You're right — it should be GET. The general REST convention is:
MethodWhen to useGETRetrieving/reading dataPOSTCreating/submitting dataPUTUpdating dataDELETEDeleting data
Both /service_summary and /service_raw_responses are just reading and returning data, so both should be GET.

Why it was POST though
The reason it ended up as POST is because both endpoints use Depends(verify_admin_access) which expects a request body (LoginCredentials). GET requests technically shouldn't have a request body — so whoever wrote it used POST as a workaround to pass the credentials.

The cleaner solution
Instead of passing credentials in the body every time, the admin should login once and receive a token, then pass that token in the request header for subsequent calls. That way your summary and raw response endpoints can properly be GET requests.
But that requires implementing token-based authentication which is a bigger change. For now, if you want to keep it simple, you have two options:

Keep POST — it works, just not semantically correct
Switch to GET and pass credentials as query parameters — but that exposes the password in the URL which is worse

So honestly for your current setup, keeping POST is the lesser evil until you implement proper token auth.You said: how do you implement a token authhow do you implement a token auth3:50 PMClaude responded: Here's the concept and flow:Here's the concept and flow:

The Idea
Instead of sending username and password on every request, the admin logs in once, gets a token, then uses that token for all subsequent requests.
Login → receive token → use token for every protected endpoint

The Flow
1. Admin POSTs credentials to /login
        ↓
2. Backend verifies credentials
        ↓
3. Backend generates a token and sends it back
        ↓
4. Frontend saves the token (st.session_state["token"])
        ↓
5. Every protected request includes the token in the header:
   Authorization: Bearer <token>
        ↓
6. Backend verifies the token before processing the request

What to look into
FastAPI has built-in support for this using JWT (JSON Web Tokens). The library you need is called python-jose for generating and verifying tokens, combined with FastAPI's OAuth2PasswordBearer.
The key concepts to research:

JWT — a token that contains encoded data (like service_id, username) and an expiry time
OAuth2PasswordBearer — FastAPI's built-in way to extract the token from the Authorization header
python-jose — generates and verifies JWT tokens


How your endpoints change
Currently:
python# sends credentials every time
@router.post("/service_summary")
def summary(verified_user: dict = Depends(verify_admin_access)):
With token auth:
python# just verifies the token, no credentials needed
@router.get("/service_summary")
def summary(verified_user: dict = Depends(verify_token)):

On the Streamlit side
python# after login, save the token
st.session_state["token"] = response["token"]

# use it in every subsequent request
headers = {"Authorization": f"Bearer {st.session_state['token']}"}
httpx.get("http://localhost:8000/service_summary", headers=headers)

Summary of what to implement
StepWhat to do1Install python-jose and passlib2Create a create_token() function in your auth file3Return the token from /login4Create a verify_token() dependency to replace verify_admin_access5Switch protected endpoints from POST to GET6Save and send token from StreamlitYou said: how much work is that to implement in my codehow much work is that to implement in my code3:52 PMClaude responded: Looking at your current codebase, it's not too much work.Looking at your current codebase, it's not too much work. Here's a realistic breakdown:

Files you need to touch
1. admin_auth.py — most of the work

Add create_token() function
Add verify_token() dependency to replace verify_admin_access
Modify /login to return a token in the response
That's roughly 30-40 lines added

2. admin_sum.py — minor changes

Change @router.post to @router.get on both endpoints
Replace Depends(verify_admin_access) with Depends(verify_token)
That's literally just 2 changes per endpoint

3. Streamlit frontend — wherever you call the API

Save token after login: 1 line
Add Authorization header to every protected request: 1 line per call


What you need to install
pip install python-jose[cryptography]

Realistic time estimate
TaskEffortModifying admin_auth.py~30 minutesUpdating admin_sum.py~5 minutesUpdating Streamlit calls~10 minutes
So roughly 45 minutes to an hour total if you follow a guide alongside it.

My suggestion
Since you're deploying locally and it's a school project, you could also just keep your current POST approach for now and focus on finishing the frontend first. Token auth is cleaner but not strictly necessary for a local deployment. You can always refactor it later.You said: what else do I need to do herefrom datetime import timedelta
from pathlib import Path
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import csv
import hashlib
import jose

router = APIRouter()

# PATH SETUP 
DATA_DIR = Path(__file__).resolve().parents[2] / "data" 
ADMINS_FILE = DATA_DIR / "Admins.csv"
SERVICES_FILE = DATA_DIR / "Services.csv"

# PYDANTIC MODELS
class LoginCredentials(BaseModel):
    username: str
    password: str

# PASSWORD HASHING LOGIC
def _hash_password(password: str, salt: bytes) -> bytes:
    """Hashes the password using PBKDF2 with SHA-256."""
    return hashlib.pbkdf2_hmac(
        'sha256', 
        password.encode('utf-8'), 
        salt, 
        100000
    )

def create_token(data: dict, secret_key: str, algorithm: str = "HS256", expires_in_minutes: int = 60):
    """Creates a JWT token with the given data and expiration."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_in_minutes)
    to_encode.update({"exp": expire})
    return jose.jwt.encode(to_encode, secret_key, algorithm=algorithm)

# VALIDATION LOGIC 
def verify_admin_access(credentials: LoginCredentials):
  
    if not ADMINS_FILE.exists() or not SERVICES_FILE.exists():
        raise HTTPException(
            status_code=500, 
            detail="Database Error: CSV files are missing."
        )

    is_authenticated = False
    authorized_service_id = ""

    # 1. Admin Authentication
    with ADMINS_FILE.open(mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row.get("username", "").strip() == credentials.username:
                salt_hex = row.get("salt", "").strip()
                hash_hex = row.get("pwd_hash", "").strip()
                
                if salt_hex and hash_hex:
                    try:
                        stored_salt = bytes.fromhex(salt_hex)
                        stored_hash = bytes.fromhex(hash_hex)
                        login_hash = _hash_password(credentials.password, stored_salt)
                        
                        if stored_hash == login_hash:
                            is_authenticated = True
                            authorized_service_id = row.get("service_id", "").strip()
                    except ValueError:
                        pass 
                
                break 

    if not is_authenticated:
        raise HTTPException(
            status_code=401, 
            detail="Invalid username or password."
        )

    assigned_service_name = "Unknown Service"
    with SERVICES_FILE.open(mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row.get("service_id", "").strip() == authorized_service_id:
                assigned_service_name = row.get("service_name", "").strip()
                break

    return {
        "username": credentials.username,
        "service_id": authorized_service_id,
        "service_name": assigned_service_name
    }

# ENDPOINTS

@router.post("/login")
def login_admin(verified_user: dict = Depends(verify_admin_access)):
    return {
        "message": "Login successful.", 
        **verified_user  
    }what else do I need to do hereShow more3:57 PMClaude responded: You're close!You're close! Here's what's still missing:

1. Missing imports
pythonfrom datetime import datetime, timedelta  # datetime is missing
from jose import jwt                       # you imported jose but not jwt specifically
from fastapi.security import OAuth2PasswordBearer  # needed for token verification

2. Missing secret key constant
You need a secret key to sign your tokens — define it as a constant:
pythonSECRET_KEY = "your-secret-key-here"  # make this a long random string
ALGORITHM = "HS256"

3. create_token() is defined but never called in /login
Your login endpoint currently still returns the same thing as before — it never generates a token. You need to call create_token() inside /login and return the token:
python@router.post("/login")
def login_admin(verified_user: dict = Depends(verify_admin_access)):
    token = create_token(data=verified_user, secret_key=SECRET_KEY)
    return {
        "message": "Login successful.",
        "token": token,
        **verified_user
    }

4. Missing verify_token() dependency
This is the function your protected endpoints will use instead of verify_admin_access. You still need to write it:
pythonoauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jose.JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")

5. Install the library properly
Make sure you installed it correctly:
pip install python-jose[cryptography]
Plain pip install jose is a different unrelated package — the correct one is python-jose.

Summary of what's left
TaskStatusFix imports❌ missing datetime, fix jose importAdd SECRET_KEY constant❌ missingCall create_token() in /login❌ missingWrite verify_token() dependency❌ missingInstall python-jose[cryptography]❓ double checkYou said: Can you double checkfrom datetime import timedelta
from pathlib import Path
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import csv
import hashlib
from jose import jwt

router = APIRouter()

# PATH SETUP 
DATA_DIR = Path(__file__).resolve().parents[2] / "data" 
ADMINS_FILE = DATA_DIR / "Admins.csv"
SERVICES_FILE = DATA_DIR / "Services.csv"
SECRET_KEY = "your_secret_key"  # In
ALGORITHM = "HS256"

# PYDANTIC MODELS
class LoginCredentials(BaseModel):
    username: str
    password: str

# PASSWORD HASHING LOGIC
def _hash_password(password: str, salt: bytes) -> bytes:
    """Hashes the password using PBKDF2 with SHA-256."""
    return hashlib.pbkdf2_hmac(
        'sha256', 
        password.encode('utf-8'), 
        salt, 
        100000
    )

def create_token(data: dict, secret_key: str, algorithm: str = "HS256", expires_in_minutes: int = 60):
    """Creates a JWT token with the given data and expiration."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_in_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret_key, algorithm=algorithm)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jose.JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")

# VALIDATION LOGIC 
#def verify_admin_access(credentials: LoginCredentials):
  
    if not ADMINS_FILE.exists() or not SERVICES_FILE.exists():
        raise HTTPException(
            status_code=500, 
            detail="Database Error: CSV files are missing."
        )

    is_authenticated = False
    authorized_service_id = ""

    # 1. Admin Authentication
    with ADMINS_FILE.open(mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row.get("username", "").strip() == credentials.username:
                salt_hex = row.get("salt", "").strip()
                hash_hex = row.get("pwd_hash", "").strip()
                
                if salt_hex and hash_hex:
                    try:
                        stored_salt = bytes.fromhex(salt_hex)
                        stored_hash = bytes.fromhex(hash_hex)
                        login_hash = _hash_password(credentials.password, stored_salt)
                        
                        if stored_hash == login_hash:
                            is_authenticated = True
                            authorized_service_id = row.get("service_id", "").strip()
                    except ValueError:
                        pass 
                
                break 

    if not is_authenticated:
        raise HTTPException(
            status_code=401, 
            detail="Invalid username or password."
        )

    assigned_service_name = "Unknown Service"
    with SERVICES_FILE.open(mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row.get("service_id", "").strip() == authorized_service_id:
                assigned_service_name = row.get("service_name", "").strip()
                break

    return {
        "username": credentials.username,
        "service_id": authorized_service_id,
        "service_name": assigned_service_name
    }

# ENDPOINTS

@router.post("/login")
def login_admin(verified_user: dict = Depends(verify_admin_access)):
    token = create_token(
        data={"sub": verified_user["username"]},
        secret_key="your_secret_key",
        expires_in_minutes=60
    )
    return {
        "message": "Login successful.",
        "token": token,
        **verified_user
    }Can you double checkShow more4:00 PMClaude responded: I can see several issues:I can see several issues:

Problem 1 — verify_admin_access is commented out but code below it isn't
python#def verify_admin_access(credentials: LoginCredentials):
  
    if not ADMINS_FILE.exists() ...  # this code is now floating outside any function
You accidentally only commented the def line. Either uncomment the whole function or the code below it will cause a syntax error.

Problem 2 — datetime still not imported
pythonexpire = datetime.utcnow() + timedelta(minutes=expires_in_minutes)
You import timedelta but not datetime. Fix:
pythonfrom datetime import datetime, timedelta

Problem 3 — OAuth2PasswordBearer not imported
pythonoauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")  # will crash, not imported
Add to imports:
pythonfrom fastapi.security import OAuth2PasswordBearer

Problem 4 — jose.JWTError wrong reference
pythonexcept jose.JWTError:  # jose isn't imported as a module
Since you did from jose import jwt, change it to:
pythonfrom jose import jwt, JWTError

# then in verify_token:
except JWTError:

Problem 5 — Token only encodes username, not service_id and service_name
pythondata={"sub": verified_user["username"]}  # missing service info
Your protected endpoints need service_id and service_name from the token. Include them:
pythondata={
    "sub": verified_user["username"],
    "service_id": verified_user["service_id"],
    "service_name": verified_user["service_name"]
}

Summary
ProblemFixverify_admin_access partially commentedUncomment the whole functiondatetime not importedAdd datetime to the importOAuth2PasswordBearer not importedImport from fastapi.securityjose.JWTError wrong referenceImport JWTError directly from joseToken missing service_id and service_nameAdd them to the token dataYou said: where do I store this?SECRET_KEY = "your_secret_key"  # In
ALGORITHM = "HS256"where do I store this? inside the admin_auth ?4:05 PMClaude responded: Yes you can store it in admin_auth.Yes you can store it in admin_auth.py for now since that's where all your auth logic lives. But the proper way is to store it in a .env file so it's not hardcoded in your source code.

Why .env is better
If you hardcode it in admin_auth.py:

It's visible to anyone who sees your code
If you push to GitHub, your secret key is exposed
Harder to change without touching the code


How to do it properly
1. Create a .env file in your project root:
SECRET_KEY=some_long_random_string_here
ALGORITHM=HS256
2. Install python-dotenv:
pip install python-dotenv
3. Load it in admin_auth.py:
pythonimport os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
4. Add .env to your .gitignore:
.env

For your secret key value
Don't use "your_secret_key" — generate a proper random one. You can do it in Python:
pythonimport secrets
print(secrets.token_hex(32))
Copy that output and paste it as your SECRET_KEY value in .env.You said: but the deployment of this app will be locallybut the deployment of this app will be locally4:06 PMClaude responded: Then storing it directly in admin_auth.Then storing it directly in admin_auth.py is perfectly fine for a local deployment. The .env approach is more of a production/security best practice.
Since it's local:

No one outside your machine can access it
You're not pushing to a public GitHub repo (hopefully)
It keeps things simple

Just change the placeholder to an actual random string:
pythonSECRET_KEY = "some_long_random_string_here"
ALGORITHM = "HS256"
Generate a proper one using:
pythonimport secrets
print(secrets.token_hex(32))
Copy that output and use it as your SECRET_KEY. That's all you need for a local deployment.You said: but is it still okay to store it in env when if its local deployement?but is it still okay to store it in env when if its local deployement?4:06 PMClaude responded: Yes, it's still okay and actually still a good habit even for local deployment.Yes, it's still okay and actually still a good habit even for local deployment. There's no downside to using .env locally — it's just a file that sits in your project folder.
The only difference is the reason changes:
ReasonProductionLocalHide from public✅ Critical✅ Still good practiceEasy to change without touching code✅✅Avoid accidentally committing secrets to GitHub✅ Critical✅ Still applies
The last point is actually still relevant even for local projects — if you ever accidentally push your code to GitHub without a .gitignore, your secret key stays safe because .env is excluded.
So the recommendation is: use .env if your team is comfortable with it, but don't stress over it if you just want to keep things simple — hardcoding it in admin_auth.py works fine for a local school project.from datetime import datetime, timedelta
import os
from pathlib import Path
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import csv
import hashlib
from jose import jwt, JWTError # type: ignore
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()

DATA_DIR = Path(__file__).resolve().parents[2] / "data" 
ADMINS_FILE = DATA_DIR / "Admins.csv"
SERVICES_FILE = DATA_DIR / "Services.csv"

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")Show more4:10 PMClaude responded: One issue — you're using os.One issue — you're using os.getenv() but you're not loading the .env file. os.getenv() alone only reads from system environment variables, not from a .env file.

Fix — either use dotenv or hardcode it
Option 1 — Use .env file (add the missing load):
pythonfrom dotenv import load_dotenv
load_dotenv()  # this line is what actually reads the .env file

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
Option 2 — Just hardcode it since it's local:
pythonSECRET_KEY = "your_generated_secret_key_here"
ALGORITHM = "HS256"

Also — SECRET_KEY could be None
If you stick with Option 1, add a safety check:
pythonSECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is not set in the .env file.")
Otherwise if the .env file is missing or the key isn't set, SECRET_KEY will be None and JWT signing will crash silently later.from datetime import datetime, timedelta
import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import csv
import hashlib
from jose import jwt, JWTError # type: ignore
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()

load_dotenv()

DATA_DIR = Path(__file__).resolve().parents[2] / "data" 
ADMINS_FILE = DATA_DIR / "Admins.csv"
SERVICES_FILE = DATA_DIR / "Services.csv"

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is not set.") 
ALGORITHM = os.getenv("ALGORITHM", "HS256")

what are the next steps, Im rebuilding the admin_authShow more4:11 PMClaude responded: Good progress!Good progress! Here's what to build next in order:

Step 1 — Pydantic model (already have this, keep it)
pythonclass LoginCredentials(BaseModel):
    username: str
    password: str

Step 2 — Password hashing function (already have this, keep it)
pythondef _hash_password(password: str, salt: bytes) -> bytes:
    ...

Step 3 — create_token() function (already have this, keep it)
pythondef create_token(data: dict, expires_in_minutes: int = 60):
    ...

Step 4 — verify_admin_access() function (restore this)
The authentication logic that:

Opens Admins.csv and checks credentials
Looks up service name from Services.csv
Returns username, service_id, service_name


Step 5 — oauth2_scheme and verify_token() (new)
pythonoauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def verify_token(token: str = Depends(oauth2_scheme)):
    # decodes and validates the JWT token
    # returns the payload

Step 6 — /login endpoint

Takes LoginCredentials
Calls verify_admin_access()
Calls create_token() with the user data
Returns the token + user info


Order to write them
_hash_password → verify_admin_access → create_token → verify_token → /login endpoint
Which step do you want to tackle first?You said: I have fix the admin auth and added token, but when Im calling the get service raw response and get service response summary it throws Not authenticatedI have fix the admin auth and added token, but when Im calling the get service raw response and get service response summary it throws Not authenticated4:26 PMClaude responded: That's expected behavior — it means the token verification is working.That's expected behavior — it means the token verification is working. The issue is just that you're not passing the token correctly when calling those endpoints.

Why it throws "Not authenticated"
OAuth2PasswordBearer looks for the token in the request header:
Authorization: Bearer <your_token>
If that header is missing or malformed, FastAPI automatically returns "Not authenticated".

How to fix it — depends on where you're calling from
If testing via Swagger UI (/docs):

Click the Authorize button (lock icon) at the top right
Paste your token there
Swagger will automatically attach it to all subsequent requests

If calling from Streamlit:
pythontoken = st.session_state["token"]
headers = {"Authorization": f"Bearer {token}"}

response = httpx.post(
    "http://localhost:8000/service_summary",
    headers=headers
)
If testing via curl:
bashcurl -X GET "http://localhost:8000/service_summary" \
  -H "Authorization: Bearer your_token_here"

Quick checklist

Are you saving the token after login?
Are you passing it in the Authorization header?
Is the format exactly Bearer <token> with a space?

Which of these are you calling from — Swagger, Streamlit, or something else?4:29 PMClaude responded: The problem is Swagger's Authorize button is trying to use the OAuth2 password flow — it's sending username, password, clientid, and clientsecret as a form, no…The problem is Swagger's Authorize button is trying to use the OAuth2 password flow — it's sending username, password, client_id, and client_secret as a form, not JSON. But your /login endpoint expects a JSON body via your LoginCredentials Pydantic model, hence the 422 Unprocessable Entity.

The mismatch
Swagger Authorize sendsYour /login expectsForm dataJSON bodyusername, password, client_id, client_secret{"username": "...", "password": "..."}

Easiest fix for testing in Swagger
Don't use the Authorize button. Instead:
Step 1 — Call /login directly in Swagger:

Find your /login endpoint in Swagger
Click Try it out
Send your credentials as JSON
Copy the token from the response

Step 2 — Manually authorize:

Click the Authorize button
Ignore the username/password fields
Paste your token directly into a curl request or use it in Streamlit


Proper fix if you want Swagger's Authorize button to work
You'd need to change your /login to accept form data instead of JSON using FastAPI's OAuth2PasswordRequestForm. But that's a bigger change and unnecessary since you're testing locally and will ultimately call it from Streamlit anyway.
For now just test via the /login endpoint directly in Swagger and copy the token manually.You said: this is my codefrom pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

from backend.Endpoints.admin_authV2 import verify_token
from .admin_auth import verify_admin_access

router = APIRouter()

pastedthis is my code
and this is for authv2from datetime import datetime, timedelta
import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import csv
import hashlib
from jose import jwt, JWTError # type: ignore
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()

load_dotenv()

DATA_DIR = Path(__file__).resolve().parents[2] / "data" 
ADMINS_FILE = DATA_DIR / "Admins.csv"
SERVICES_FILE = DATA_DIR / "Services.csv"

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is not set.") 
ALGORITHM = os.getenv("ALGORITHM", "HS256")

class LoginCredentials(BaseModel):
    username: str
    password: str

def _hash_password(password: str, salt: bytes) -> bytes:
    """Hashes the password using PBKDF2 with SHA-256."""
    return hashlib.pbkdf2_hmac(
        'sha256', 
        password.encode('utf-8'), 
        salt, 
        100000
    )   

def create_token(data: dict, secret_key: str, algorithm: str = "HS256", expires_in_minutes: int = 60):
    """Creates a JWT token with the given data and expiration."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_in_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret_key, algorithm=algorithm)

def verify_admin_access(credentials: LoginCredentials):
  
    if not ADMINS_FILE.exists() or not SERVICES_FILE.exists():
        raise HTTPException(
            status_code=500, 
            detail="Database Error: CSV files are missing."
        )

    is_authenticated = False
    authorized_service_id = ""

    # 1. Admin Authentication
    with ADMINS_FILE.open(mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row.get("username", "").strip() == credentials.username:
                salt_hex = row.get("salt", "").strip()
                hash_hex = row.get("pwd_hash", "").strip()
                
                if salt_hex and hash_hex:
                    try:
                        stored_salt = bytes.fromhex(salt_hex)
                        stored_hash = bytes.fromhex(hash_hex)
                        login_hash = _hash_password(credentials.password, stored_salt)
                        
                        if stored_hash == login_hash:
                            is_authenticated = True
                            authorized_service_id = row.get("service_id", "").strip()
                    except ValueError:
                        pass 
                
                break 

    if not is_authenticated:
        raise HTTPException(
            status_code=401, 
            detail="Invalid username or password."
        )

    assigned_service_name = "Unknown Service"
    with SERVICES_FILE.open(mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row.get("service_id", "").strip() == authorized_service_id:
                assigned_service_name = row.get("service_name", "").strip()
                break

    return {
        "username": credentials.username,
        "service_id": authorized_service_id,
        "service_name": assigned_service_name
    }


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")
    
@router.post("/loginv2")
def login_adminv2(verified_user: dict = Depends(verify_admin_access)):
    token = create_token(
        data={"sub": verified_user["username"]},
        secret_key=SECRET_KEY,
        expires_in_minutes=60
    )
    return {
        "message": "Login successful.",
        "token": token,
        **verified_user
    }Show more4:33 PMClaude responded: I can see the problem — your token only encodes username but your endpoints need serviceid and servicename from the token payload:I can see the problem — your token only encodes username but your endpoints need service_id and service_name from the token payload:

Problem 1 — Token is missing service_id and service_name
python# current - only encodes username
token = create_token(
    data={"sub": verified_user["username"]},
    ...
)
When verify_token decodes this, the payload only has sub — so when your endpoints do:
pythonservice_id = verified_user.get("service_id")   # returns None
service_name = verified_user.get("service_name")  # returns None
Both come back None, which is why your summary and raw responses return empty data.
Fix:
pythontoken = create_token(
    data={
        "sub": verified_user["username"],
        "service_id": verified_user["service_id"],
        "service_name": verified_user["service_name"]
    },
    secret_key=SECRET_KEY,
    expires_in_minutes=60
)

Problem 2 — You have two auth files being imported
In admin_sum.py you have:
pythonfrom backend.Endpoints.admin_authV2 import verify_token
from .admin_auth import verify_admin_access  # this is unused now
Remove the second import since you're already using verify_token from admin_authV2. The old verify_admin_access import is just dead code now.

Problem 3 — today preset is still wrong in both endpoints
python"today": (current_date - timedelta(days=1), current_date),
Should be:
python"today": (current_date.replace(hour=0, minute=0, second=0, microsecond=0), current_date),

Fix Problem 1 first — that's the one causing your empty responses.You said: it still throws not authenticatedit still throws not authenticated4:37 PMClaude responded: That's because you're testing directly in Swagger without passing the token.That's because you're testing directly in Swagger without passing the token. Looking at the curl command it generated:
bashcurl -X 'GET' \
  'http://127.0.0.1:8000/service_raw_responses?preset_range=today' \
  -H 'accept: application/json'
# missing: -H 'Authorization: Bearer <your_token>'
There's no Authorization header being sent at all.

How to fix it in Swagger
Step 1 — Get your token first:

Find /loginv2 in Swagger
Click Try it out
Send your credentials
Copy the token value from the response

Step 2 — Authorize Swagger:

Click the Authorize button (lock icon, top right of Swagger)
In the field that appears, type only:

Bearer <paste_your_token_here>

Click Authorize then Close

Step 3 — Try the endpoint again

Swagger will now automatically attach the token to all requests


The key thing is you need to do Step 1 first using /loginv2 to get a token, then Step 2 to tell Swagger to use it. The Authorize button in Swagger doesn't automatically log you in — you have to get the token manually first.You said: where do I put it herewhere do I put it here4:38 PMClaude responded: This Authorize dialog won't work for your setup because it expects OAuth2 form-based login, not your JSON-based login.This Authorize dialog won't work for your setup because it expects OAuth2 form-based login, not your JSON-based login.
Ignore this dialog entirely. Here's what to do instead:

Step 1 — Get your token from /loginv2

Find /loginv2 in Swagger
Click Try it out
Enter your credentials:

json{
  "username": "accAdmin",
  "password": "your_password"
}

Click Execute
Copy the token value from the response


Step 2 — Use the token directly in the endpoint

Find /service_raw_responses in Swagger
Click Try it out
You won't see an Authorization field by default, so use the curl command directly in your terminal instead:

bashcurl -X 'GET' \
  'http://127.0.0.1:8000/service_raw_responses' \
  -H 'Authorization: Bearer paste_your_token_here'

Permanent fix for Swagger
If you want Swagger's Authorize button to actually work with your setup, change your tokenUrl in oauth2_scheme to point to your actual login endpoint:
pythonoauth2_scheme = OAuth2PasswordBearer(tokenUrl="/loginv2")
But even then the form/JSON mismatch will still be an issue. The curl approach is the easiest way to test for now.You said: this is my code for calling the summary and raw responsefrom pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from .admin_auth import verify_admin_access

router = APIRouter()

DATA_FILE = Path(__file__).resolve().parents[2] / "data" /pastedthis is my code for calling the summary and raw responseand here is my admin authfrom pathlib import Path
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import csv
import hashlib

router = APIRouter()

# PATH SETUP 
DATA_DIR = Path(__file__).resolve().parents[2] / "data" 
ADMINS_FILE = DATA_DIR / "Admins.csv"
SERVICES_FILE = DATA_DIR / "Services.csv"

# PYDANTIC MODELS
class LoginCredentials(BaseModel):
    username: str
    password: str

# PASSWORD HASHING LOGIC
def _hash_password(password: str, salt: bytes) -> bytes:
    """Hashes the password using PBKDF2 with SHA-256."""
    return hashlib.pbkdf2_hmac(
        'sha256', 
        password.encode('utf-8'), 
        salt, 
        100000
    )

# VALIDATION LOGIC 
def verify_admin_access(credentials: LoginCredentials):
  
    if not ADMINS_FILE.exists() or not SERVICES_FILE.exists():
        raise HTTPException(
            status_code=500, 
            detail="Database Error: CSV files are missing."
        )

    is_authenticated = False
    authorized_service_id = ""

    # 1. Admin Authentication
    with ADMINS_FILE.open(mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row.get("username", "").strip() == credentials.username:
                salt_hex = row.get("salt", "").strip()
                hash_hex = row.get("pwd_hash", "").strip()
                
                if salt_hex and hash_hex:
                    try:
                        stored_salt = bytes.fromhex(salt_hex)
                        stored_hash = bytes.fromhex(hash_hex)
                        login_hash = _hash_password(credentials.password, stored_salt)
                        
                        if stored_hash == login_hash:
                            is_authenticated = True
                            authorized_service_id = row.get("service_id", "").strip()
                    except ValueError:
                        pass 
                
                break 

    if not is_authenticated:
        raise HTTPException(
            status_code=401, 
            detail="Invalid username or password."
        )

    assigned_service_name = "Unknown Service"
    with SERVICES_FILE.open(mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row.get("service_id", "").strip() == authorized_service_id:
                assigned_service_name = row.get("service_name", "").strip()
                break

    return {
        "username": credentials.username,
        "service_id": authorized_service_id,
        "service_name": assigned_service_name
    }

# ENDPOINTS

@router.post("/login")
def login_admin(verified_user: dict = Depends(verify_admin_access)):
    return {
        "message": "Login successful.", 
        **verified_user  
    }

@router.get("/services")
def get_services():
    """Reads Services.csv on the fly and returns the available services."""
    if not SERVICES_FILE.exists():
        raise HTTPException(status_code=500, detail="Database error: Services.csv file not found.")
        
    services = []
    with SERVICES_FILE.open(mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            s_id = row.get("service_id", "").strip()
            s_name = row.get("service_name", "").strip()
            if s_id and s_name:
                services.append({"service_id": s_id, "service_name": s_name})
                
    return {"services": services}when testing it in swagger, when calling the raw responses and summary, why do I need to input user name and password againShow more4:44 PMClaude responded: Because your adminsum.Because your admin_sum.py is still using verify_admin_access as the dependency:
pythonfrom .admin_auth import verify_admin_access

@router.post("/service_summary")
def service_response_summary(
    verified_user: dict = Depends(verify_admin_access),  # this requires credentials every time
verify_admin_access expects a LoginCredentials body — so every endpoint that depends on it will ask for username and password again.

This is exactly why you need token auth
The flow should be:
Login once → get token → use token for all subsequent requests
But right now your admin_sum.py is still using the old verify_admin_access instead of verify_token from your admin_authV2.

Fix
In admin_sum.py change the import and dependency:
python# remove this
from .admin_auth import verify_admin_access

# add this
from .admin_authV2 import verify_token
Then on both endpoints change:
python# from this
verified_user: dict = Depends(verify_admin_access)

# to this
verified_user: dict = Depends(verify_token)
Also change both endpoints from @router.post to @router.get since you're just reading data.
After this, the flow becomes:

Call /loginv2 once with credentials → get token
Use token for /service_summary and /service_raw_responses — no credentials needed again
You said: but will this still work even if I don't use token?but will this still work even if I don't use token?4:50 PMClaude responded: No, once you switch to verify_token as the dependency, the endpoints will require a token.No, once you switch to verify_token as the dependency, the endpoints will require a token. No token = 401 Unauthorized.

Your two options
Option 1 — Keep using verify_admin_access (no token)

Credentials required on every request
Works fine for testing in Swagger
Simpler, no token management needed
Downside: Streamlit would need to send username/password on every API call

Option 2 — Switch to verify_token (token auth)

Login once, get token, use token for all subsequent requests
Cleaner and more realistic
Downside: slightly more setup on the Streamlit side


For your use case
Since this is a local school project and your Streamlit frontend will be the one calling the API, think about it this way:

If you're okay with saving the username and password in st.session_state and sending them on every request → stick with Option 1
If you want to save just the token after login and use that → go with Option 2

Both work. Option 1 is simpler to finish quickly. Option 2 is cleaner but you've already built most of it with admin_authV2.py anyway, so it's not much more work.
Which do you want to go with?You said: I reverted it back to old codeI reverted it back to old code4:50 PMClaude responded: That's fine — the old code works for your use case.That's fine — the old code works for your use case. Just make sure these things are consistent across your files:

What to verify after reverting
1. admin_sum.py import is back to:
pythonfrom .admin_auth import verify_admin_access
2. Both endpoints are back to @router.post with verify_admin_access:
python@router.post("/service_summary")
def service_response_summary(
    verified_user: dict = Depends(verify_admin_access),
3. app.py is not importing anything from admin_authV2:
python# make sure this is removed if it was added
from backend.Endpoints.admin_authV2 import verify_token

How it works now for Streamlit
When calling protected endpoints from Streamlit, you just send credentials every time:
pythonresponse = httpx.post(
    "http://localhost:8000/service_summary",
    json={
        "username": st.session_state["username"],
        "password": st.session_state["password"]
    }
)
So save both username and password in st.session_state after login, and reuse them for every subsequent API call.You said: but when we implement it to the frontend, when get raw survey is called the admin needs to input credentials again?but when we implement it to the frontend, when get raw survey is called the admin needs to input credentials again?4:51 PMClaude responded: Yes, with the old code that's exactly what would happen — but not visibly to the admin.Yes, with the old code that's exactly what would happen — but not visibly to the admin. The frontend handles it silently.

How it works on the Streamlit side
The admin logs in once on the login page:
python# login page - admin types credentials once
username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    response = httpx.post("/login", json={
        "username": username,
        "password": password
    })
    # save to session state
    st.session_state["username"] = username
    st.session_state["password"] = password
    st.session_state["logged_in"] = True
Then every subsequent API call just pulls from session_state silently:
python# dashboard page - admin never sees this happening
response = httpx.post(
    "http://localhost:8000/service_summary",
    json={
        "username": st.session_state["username"],
        "password": st.session_state["password"]
    }
)

So from the admin's perspective
Admin types credentials once on login page
            ↓
Streamlit saves them silently in session_state
            ↓
Every API call reuses them automatically
            ↓
Admin never sees or types credentials again
The admin experience is identical to token auth — the difference is only behind the scenes. For a local school project this is perfectly acceptable.You said: how to make a stated problem out of this TASK: Design a company network with three departments (HR, Sales, IT) on separate VLANs.how to make a stated problem out of this TASK: Design a company network with three departments (HR, Sales, IT) on separate VLANs. Connect at least 15 wired PCs across departments and 5 wireless laptops for mobility. Deploy two core switches connected redundantly to two routers. Configure dynamic routing (OSPF) between routers and set up HSRP for gateway redundancy. Add a server farm containing DHCP, DNS, and Web servers. Connect the network to a simulated ISP router for Internet access. Implement ACLs to restrict inter-departmental access and set up a backup Internet link via a second ISP router, with floating static routes for automatic failover. Test full network functionality under normal and failure scenarios.9:36 PMClaude responded: Here's a stated problem for your task:Here's a stated problem for your task:

Stated Problem
Organizations with multiple departments often face challenges in managing network traffic, ensuring security, and maintaining continuous connectivity. Without proper network segmentation, departments such as HR, Sales, and IT share the same broadcast domain, making sensitive data vulnerable to unauthorized access and increasing network congestion. Additionally, single points of failure in network infrastructure — such as relying on a single router or gateway — pose significant risks to business continuity, as any hardware failure can result in complete network downtime.
This study aims to design and implement a segmented enterprise network for a company with three departments (HR, Sales, and IT) using VLAN-based isolation to separate departmental traffic. The network will support a minimum of 15 wired workstations and 5 wireless laptops distributed across departments. To ensure high availability, two core switches will be connected redundantly to two routers configured with OSPF for dynamic routing and HSRP for gateway redundancy. A centralized server farm providing DHCP, DNS, and Web services will be deployed to support network operations. Internet connectivity will be established through a primary ISP router, with a secondary ISP router serving as a backup link using floating static routes for automatic failover. Access Control Lists (ACLs) will be implemented to restrict unauthorized inter-departmental communication and enforce network security policies. The proposed design will be tested under both normal operating conditions and simulated failure scenarios to validate redundancy, failover mechanisms, and overall network functionality.You said: how to make a stated problem out of this TASK: Design a company network with three departments (HR, Sales, IT) on separate VLANs.how to make a stated problem out of this TASK: Design a company network with three departments (HR, Sales, IT) on separate VLANs. Connect at least 15 wired PCs across departments and 5 wireless laptops for mobility. Deploy two core switches connected redundantly to two routers. Configure dynamic routing (OSPF) between routers and set up HSRP for gateway redundancy. Add a server farm containing DHCP, DNS, and Web servers. Connect the network to a simulated ISP router for Internet access. Implement ACLs to restrict inter-departmental access and set up a backup Internet link via a second ISP router, with floating static routes for automatic failover. Test full network functionality under normal and failure scenarios.9:37 PMClaude responded: Here's a stated problem for your task:Here's a stated problem for your task:

Stated Problem
Organizations with multiple departments often struggle with network security, traffic management, and uninterrupted connectivity. When departments such as HR, Sales, and IT operate on a shared network without proper segmentation, sensitive information becomes vulnerable to unauthorized access from other departments, and excessive broadcast traffic degrades overall network performance. Furthermore, networks that rely on a single gateway or a single Internet connection are highly susceptible to total service disruption whenever a hardware failure or ISP outage occurs, resulting in lost productivity and potential data inaccessibility.
This study addresses these problems by designing and implementing a segmented enterprise network that isolates each department — HR, Sales, and IT — into separate VLANs to control broadcast domains and restrict unauthorized inter-departmental communication through Access Control Lists. The network will accommodate at least 15 wired workstations and 5 wireless laptops to support both fixed and mobile users across all departments. High availability will be achieved by deploying two core switches connected redundantly to two routers, with OSPF configured for dynamic routing between routers and HSRP providing gateway redundancy to eliminate single points of failure at the gateway level. A dedicated server farm hosting DHCP, DNS, and Web servers will centralize essential network services. Primary Internet access will be provided through a main ISP router, while a secondary ISP router will serve as a backup link, with floating static routes enabling automatic failover in the event of a primary link failure. The completed network design will be tested under normal operating conditions and simulated failure scenarios to verify that redundancy mechanisms, failover configurations, and security policies function as intended.You said: pythonfrom pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from .admin_auth import verify_admin_access

router = APIRouter()

DATA_FILE = Path(__file__).resolve().parents[2] / "data" /pastedfrom pathlib import Path
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, field_validator
import csv
from datetime import datetime

router = APIRouter()

DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "Survey_response.csv"

class SuccessResponse(Basepastedfrom pathlib import Path
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import csv
import hashlib

router = APIRouter()

# PATH SETUP 
DATA_DIR = Path(__file__).resolve().parents[2] / "data" 
ADMINS_FILE = DATA_DIR / "Admins.csv"
SERVICES_FILE = DATA_DIR / "Services.csv"

# PYDANTIC MODELS
class LoginCredentials(BaseModel):
    username: str
    password: str

# PASSWORD HASHING LOGIC
def _hash_password(password: str, salt: bytes) -> bytes:
    """Hashes the password using PBKDF2 with SHA-256."""
    return hashlib.pbkdf2_hmac(
        'sha256', 
        password.encode('utf-8'), 
        salt, 
        100000
    )

# VALIDATION LOGIC 
def verify_admin_access(credentials: LoginCredentials):
  
    if not ADMINS_FILE.exists() or not SERVICES_FILE.exists():
        raise HTTPException(
            status_code=500, 
            detail="Database Error: CSV files are missing."
        )

    is_authenticated = False
    authorized_service_id = ""

    # 1. Admin Authentication
    with ADMINS_FILE.open(mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row.get("username", "").strip() == credentials.username:
                salt_hex = row.get("salt", "").strip()
                hash_hex = row.get("pwd_hash", "").strip()
                
                if salt_hex and hash_hex:
                    try:
                        stored_salt = bytes.fromhex(salt_hex)
                        stored_hash = bytes.fromhex(hash_hex)
                        login_hash = _hash_password(credentials.password, stored_salt)
                        
                        if stored_hash == login_hash:
                            is_authenticated = True
                            authorized_service_id = row.get("service_id", "").strip()
                    except ValueError:
                        pass 
                
                break 

    if not is_authenticated:
        raise HTTPException(
            status_code=401, 
            detail="Invalid username or password."
        )

    assigned_service_name = "Unknown Service"
    with SERVICES_FILE.open(mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row.get("service_id", "").strip() == authorized_service_id:
                assigned_service_name = row.get("service_name", "").strip()
                break

    return {
        "username": credentials.username,
        "service_id": authorized_service_id,
        "service_name": assigned_service_name
    }

# ENDPOINTS

@router.post("/login")
def login_admin(verified_user: dict = Depends(verify_admin_access)):
    return {
        "message": "Login successful.", 
        **verified_user  
    }

@router.get("/services")
def get_services():
    """Reads Services.csv on the fly and returns the available services."""
    if not SERVICES_FILE.exists():
        raise HTTPException(status_code=500, detail="Database error: Services.csv file not found.")
        
    services = []
    with SERVICES_FILE.open(mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            s_id = row.get("service_id", "").strip()
            s_name = row.get("service_name", "").strip()
            if s_id and s_name:
                services.append({"service_id": s_id, "service_name": s_name})
                
    return {"services": services}from pathlib import Path
from fastapi import APIRouter, HTTPException
import csv

router = APIRouter()

DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "Services.csv"
    
@router.get("/get_available_services")
def get_services():
    if not DATA_FILE.exists():
        raise HTTPException(status_code=500, detail=f"Services data file not found: {DATA_FILE}")

    services = []
    with DATA_FILE.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            services.append({
                "service_id": row.get("service_id", "").strip(),
                "service_name": row.get("service_name", "").strip(),
            })

    return {"services": services}create an updated api contract based on these apiShow more11:15 PMClaude responded: Here's the updated API contract based on your actual code:Here's the updated API contract based on your actual code:

RTU_SSA - API CONTRACTS
BASE URL: http://localhost:8000

PUBLIC ENDPOINTS
1. Get Available Services

Method: GET
URL: /get_available_services
Description: Returns the list of available school services. Used to populate the service selection in the survey form.
Request Body: None
Response: 200 OK

json{
  "services": [
    { "service_id": "SV001", "service_name": "Accounting" },
    { "service_id": "SV002", "service_name": "Registrar" },
    { "service_id": "SV003", "service_name": "Clinic" }
  ]
}

Error Responses:

500 — Services data file not found




2. Submit Survey Response

Method: POST
URL: /submit_survey_response
Description: Accepts a completed survey form from a student and saves it to the CSV.
Request Body:

json{
  "service_id": "SV001",
  "service_availed": "Enrollment form",
  "respondent_name": "Jake Icasiano",
  "date_of_visit": "15/01/2026",
  "age_bracket": "17-20",
  "gender": "Male",
  "category_of_respondent": "Student",
  "cc1": "I know what a CC is and I saw this office's CC",
  "cc2": "Easy to see",
  "cc3": "Helped very much",
  "service_satisfaction": 4,
  "service_time": 4,
  "service_requirements": 4,
  "service_steps": 4,
  "service_transaction": 4,
  "service_fee": "N/A",
  "service_fair": 4,
  "service_courtesy": 4,
  "service_request": 4,
  "comments_suggestions": "N/A",
  "attending_employee": "Elijah",
  "comments_suggestions_for_employee": "Masungit"
}

Field Rules:

FieldTypeRulesservice_idstringMust be SV001, SV002, or SV003service_availedstringMax 70 characters, cannot be emptyrespondent_namestringMax 60 characters, cannot be emptydate_of_visitstringMust be in DD/MM/YYYY formatage_bracketstringMust be one of: 16-Below, 17-20, 21-25, 26 and upgenderstringMust be Male or Femalecategory_of_respondentstringMust be one of the valid choicescc1stringMust be one of the 4 valid choicescc2stringMust be one of: Easy to see, Somewhat easy to see, Difficult to see, Not visible at all, N/Acc3stringMust be one of: Helped very much, Somewhat helped, Did not help, N/Aservice_satisfactionint1 to 5 onlyservice_timeint1 to 5 onlyservice_requirementsint1 to 5 onlyservice_stepsint1 to 5 onlyservice_transactionint1 to 5 onlyservice_feestringInteger 1-5 or "N/A"service_fairint1 to 5 onlyservice_courtesyint1 to 5 onlyservice_requestint1 to 5 onlycomments_suggestionsstringMax 150 charactersattending_employeestringMax 60 characters, cannot be emptycomments_suggestions_for_employeestringMax 150 characters

Response: 200 OK

json{ "Message": "Survey submitted successfully." }

Error Responses:

422 — Missing or invalid field
500 — Could not save survey response




ADMIN ENDPOINTS
3. Admin Login

Method: POST
URL: /login
Description: Validates admin credentials. On success returns the admin's assigned service. Streamlit must save username, password, and service_id in st.session_state for subsequent calls.
Request Body:

json{
  "username": "accAdmin",
  "password": "password123"
}

Response: 200 OK

json{
  "message": "Login successful.",
  "username": "accAdmin",
  "service_id": "SV001",
  "service_name": "Accounting"
}

Error Responses:

401 — Invalid username or password
500 — CSV files are missing




4. Get Service Summary

Method: POST
URL: /service_summary
Description: Returns computed analytics for the admin's assigned service — average ratings, demographics, citizen charter counts, and feedback. Requires credentials on every call.
Query Parameter:

ParameterRequiredDescriptionpreset_rangeNoOptions: today, last_week, last_month, current_year, last_year. Leave empty for all responses.

Request Body:

json{
  "username": "accAdmin",
  "password": "password123"
}

Response: 200 OK

json{
  "status": "success",
  "service_id": "SV001",
  "service_name": "Accounting",
  "total_responses": 24,
  "active_filter": "all",
  "averages": {
    "service_satisfaction": 4.2,
    "service_time": 3.8,
    "service_requirements": 4.1,
    "service_steps": 3.9,
    "service_transaction": 4.0,
    "service_fee": "N/A",
    "service_fair": 4.3,
    "service_courtesy": 4.5,
    "service_request": 3.7
  },
  "demographics": {
    "gender": { "Male": 10, "Female": 14 },
    "age_bracket": { "17-20": 12, "21-25": 8, "26 and up": 4 },
    "category_of_respondent": { "Student": 20, "Faculty": 4 }
  },
  "citizen_charter": {
    "cc1": { "I know what a CC is and I saw this office's CC": 10 },
    "cc2": { "Easy to see": 8 },
    "cc3": { "Helped very much": 12 }
  },
  "feedback": {
    "general_comments": ["Mainit sa office"],
    "employee_comments": ["Masungit"]
  }
}

Error Responses:

400 — Invalid preset_range value
401 — Invalid username or password
500 — Survey response data file not found




5. Get Raw Survey Responses

Method: POST
URL: /service_raw_responses
Description: Returns all raw survey responses for the admin's assigned service. Used for the responses tab in the admin dashboard.
Query Parameter:

ParameterRequiredDescriptionpreset_rangeNoOptions: today, last_week, last_month, current_year, last_year. Leave empty for all responses.

Request Body:

json{
  "username": "accAdmin",
  "password": "password123"
}

Response: 200 OK

json{
  "status": "success",
  "service_id": "SV001",
  "service_name": "Accounting",
  "total_responses": 24,
  "active_filter": "all",
  "responses": [
    {
      "service_id": "SV001",
      "service_availed": "Enrollment form",
      "respondent_name": "Jake",
      "date_of_visit": "15/05/2026",
      "age_bracket": "17-20",
      "gender": "Male",
      "category_of_respondent": "Student",
      "cc1": "I know what a CC is and I saw this office's CC",
      "cc2": "Easy to see",
      "cc3": "Helped very much",
      "service_satisfaction(1-5)": "4",
      "service_time(1-5)": "4",
      "service_requirements(1-5)": "5",
      "service_steps(1-5)": "2",
      "service_transaction(1-5)": "3",
      "service_fee(1-5 or n/a)": "N/A",
      "service_fair(1-5)": "4",
      "service_courtesy(1-5)": "4",
      "service_request(1-5)": "4",
      "comments_suggestions": "N/A",
      "attending_employee": "Fey",
      "comments_suggestions_for_employee": "mabait"
    }
  ]
}

Error Responses:

400 — Invalid preset_range value
401 — Invalid username or password
500 — Survey response data file not found




Additional Notes

Streamlit must never read or write CSV files directly — all data goes through the API
After a successful /login, save to session state:

pythonst.session_state["username"] = response["username"]
st.session_state["password"] = password  # save original password input
st.session_state["service_id"] = response["service_id"]
st.session_state["service_name"] = response["service_name"]

Pass credentials on every protected endpoint call:

pythonjson={"username": st.session_state["username"], "password": st.session_state["password"]}

Both servers must be running simultaneously:

Terminal 1: uvicorn main:app --reload (inside /backend)
Terminal 2: streamlit run app.py (inside /frontend)


You said: make it into a md filemake it into a md file11:17 PMClaude responded: There's your API contract as a markdown file.Created a file, read a fileCreated a file, read a fileThere's your API contract as a markdown file. It includes all 5 endpoints with their request bodies, field rules, valid choices, response structures, error codes, and the Streamlit usage notes at the bottom.Api contractDocument · MD DownloadYou said: how should we write the read.how should we write the read.me file or the documentation of our web app 
can you list all the things that we need to include11:29 PMClaude responded: Here's everything you should include in your README:Here's everything you should include in your README:

1. Project Overview

What the app is (RTU SSA — School Service Survey System)
Purpose and goals
Who it's for (students as respondents, admins as viewers)


2. Features

Student survey submission (no account needed)
Admin login with assigned service
Dashboard with analytics and charts
Raw response viewer per service
Date filtering for responses
PDF export (if implemented)


3. Tech Stack

Backend: FastAPI
Frontend: Streamlit
Data storage: CSV files
Authentication: PBKDF2 password hashing
Libraries used: pandas, numpy, python-jose, etc.


4. Project Structure

Folder tree showing where everything is
What each file does


5. Prerequisites

Python version required
List of dependencies
How to install them (pip install -r requirements.txt)


6. Setup and Installation

How to clone the repo
How to set up the .env file and what variables are needed
How to run the backend server
How to run the frontend server


7. Environment Variables

What goes in .env
Example .env file


8. CSV File Setup

List of required CSV files
Location of each file
Column headers for each CSV
Note that these should already exist before running


9. Admin Accounts

How admin accounts are structured in Admins.csv
How passwords are hashed (brief explanation)
Default admin credentials for testing (if any)


10. API Documentation

Brief summary of all endpoints
Link to or reference the full API_CONTRACT.md


11. How to Use

Student side: how to access and fill the survey
Admin side: how to log in and navigate the dashboard


12. Known Limitations

CSV-based storage limitations
No token auth (credentials sent per request)
Local deployment only
No user registration for admins


13. Future Improvements (optional)

Token-based authentication
Database migration from CSV
PDF export
Super admin role


14. Contributors

Team members and their roles
You said: how do you implement rate limitinghow do you implement rate limiting11:08 AMClaude responded: Rate limiting controls how many requests a client can make in a given time period.Rate limiting controls how many requests a client can make in a given time period. Here's how to implement it in FastAPI:

The concept
Client makes request
        ↓
Check: how many requests has this IP made in the last X seconds?
        ↓
  ┌─────┴─────┐
Under limit    Over limit
     ↓              ↓
Allow request   Return 429 Too Many Requests

Easiest approach — slowapi library
It's the most straightforward rate limiting library for FastAPI:
bashpip install slowapi

How to set it up in main.py
pythonfrom slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# creates the limiter using the client's IP address as the key
limiter = Limiter(key_func=get_remote_address)

app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

How to apply it to endpoints
pythonfrom slowapi import Limiter
from fastapi import Request

@router.post("/submit_survey_response")
@limiter.limit("5/minute")  # max 5 submissions per minute per IP
def post_response(request: Request, response: SurveyResponse):
    ...

@router.post("/login")
@limiter.limit("10/minute")  # max 10 login attempts per minute per IP
def login_admin(request: Request, ...):
    ...
Note that request: Request is required as a parameter when using slowapi — even if you don't use it in the function body.

Limit format options
FormatMeaning"5/minute"5 requests per minute"100/hour"100 requests per hour"1/second"1 request per second"200/day"200 requests per day

What to rate limit in your project
EndpointSuggested LimitReason/submit_survey_response5/minutePrevent spam submissions/login5/minutePrevent brute force attacks/service_summary30/minuteReasonable for dashboard use/service_raw_responses30/minuteSame as above/get_available_services60/minutePublic endpoint, more lenient

One thing to note
slowapi uses memory-based storage by default — meaning rate limit counts reset if you restart the server. For a local school project this is perfectly fine. Production apps would use Redis for persistent rate limit tracking, but that's overkill for your use case.You said: will this work on local deploymentwill this work on local deployment11:08 AMClaude responded: Yes, it works perfectly on local deployment.Yes, it works perfectly on local deployment. Since slowapi uses IP address as the key by default, and all your users are on the same local network, here's what to expect:

How it behaves locally
Student survey page:

Each device on the network has its own IP address
Rate limit is tracked per device
So each student PC/laptop gets their own separate limit

Admin dashboard:

Same thing — each admin machine has its own IP
One admin hitting the limit won't affect another


One potential issue — same IP
If multiple students are behind a shared network router doing NAT (which is common in school computer labs), all their traffic might appear to come from the same IP address. In that case:

All students in the lab share the same rate limit counter
One student submitting quickly could block others temporarily


For your use case
Since it's a school survey system deployed locally, this is acceptable because:

Students only submit once anyway
Admins are few (only 3 based on your CSV)
The main purpose of rate limiting here is just to prevent accidental spam or repeated submissions

So yes — go ahead and implement it, it will work fine for your deployment scenario.You said: can you explain me how it works in local deployementcan you explain me how it works in local deployement11:10 AMClaude responded: Sure!Sure! Here's how it works step by step:

Your local network setup
School Network
        │
   Network Router
        │
    ┌───┴───┐
    │       │
Student   Admin
  PCs     PCs
    │       │
    └───┬───┘
        │
  Your Server PC
  (runs FastAPI + Streamlit)

What happens when a request comes in
Student PC (192.168.1.10) submits survey
                ↓
FastAPI receives the request
                ↓
slowapi checks: "how many requests has 192.168.1.10 made?"
                ↓
        ┌───────┴───────┐
     Under limit      Over limit
        ↓                  ↓
   Process request    Return 429
   Save to CSV        "Too many requests"

Each device is tracked separately
DeviceIP AddressRequests this minuteStatusStudent PC 1192.168.1.103/5✅ AllowedStudent PC 2192.168.1.115/5✅ At limitStudent PC 3192.168.1.121/5✅ AllowedAdmin PC192.168.1.202/5✅ Allowed

Where the counts are stored
slowapi stores the counts in your server's memory — meaning:
Server Memory (while running)
├── 192.168.1.10 → 3 requests this minute
├── 192.168.1.11 → 5 requests this minute
└── 192.168.1.12 → 1 request this minute

Counts reset automatically after the time window (e.g. every minute)
Counts reset completely if you restart the FastAPI server
Nothing is written to disk — it's all in RAM


The NAT problem in school labs
In many school computer labs, all PCs go through one router that gives them all the same external IP:
Lab PC 1 ─┐
Lab PC 2 ─┤→ Router (NAT) → 192.168.1.1 → Your Server
Lab PC 3 ─┘
Your server only sees 192.168.1.1 for all of them — so they share one rate limit counter. If your limit is 5/minute and 5 students submit at the same time, the 6th student gets blocked even though they haven't submitted before.

How to check if this affects you
It depends on your network setup:

Each PC has its own IP visible to the server → No problem, rate limiting works perfectly per device
All PCs share one IP through NAT → They share the rate limit counter

For a survey system where students submit once, even the NAT scenario is unlikely to cause real problems — the 5 submissions would happen within seconds and the counter resets after a minute anyway.You said: thonthonfrom slowapi import Limiter
from fastapi import Request

@router.post("/submit_survey_response")
@limiter.limit("5/minute")  # max 5 submissions per minute per IP
def post_response(request: Request, response: SurveyResponse):
    ...what code to implement after this11:19 AMClaude responded: After adding the decorator and request: Request parameter, the rest of your function stays exactly the same.After adding the decorator and request: Request parameter, the rest of your function stays exactly the same. You just add those two things and leave everything else untouched:
python@router.post("/submit_survey_response", response_model=SuccessResponse)
@limiter.limit("5/minute")
def post_response(request: Request, response: SurveyResponse):
    try:
        with DATA_FILE.open("a", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=CSV_HEADERS)
            writer.writerow({
                "service_id": response.service_id,
                "service_availed": response.service_availed,
                # ... rest of your existing writerow code
            })
        return {"Message": "Survey submitted successfully."}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Could not save survey response: {exc}")

The only things that actually change
1. Add the decorator above the route:
python@limiter.limit("5/minute")
2. Add request: Request as the first parameter:
pythondef post_response(request: Request, response: SurveyResponse):
That's it — everything inside the function body stays exactly as it is. slowapi intercepts the request before your function even runs, so you don't need to add any checking logic inside the function itself.You said: why is limiter being flagged and request is like not being usedwhy is limiter being flagged and request is like not being used11:20 AMClaude responded: Two issues:Two issues:

Problem 1 — limiter is not defined in this file
You created the limiter in main.py but you're using it in post_res.py. You need to either import it or access it through the app state.
The cleanest fix is to create the limiter in a separate file and import it wherever needed:
Create a new file limiter.py:
pythonfrom slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
In main.py import from it:
pythonfrom .limiter import limiter
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
In post_res.py import from it:
pythonfrom .limiter import limiter

Problem 2 — Request is not imported
Add this to your imports in post_res.py:
pythonfrom fastapi import APIRouter, HTTPException, Request
Request needs to be explicitly imported from fastapi — Pylance is flagging it because it's being used as a type hint but was never imported.You said: I imported this to my postres and in my app.from slowapi import Limiter
from fastapi import RequestI imported this to my postres and in my app.py I coded thisfrom slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)

app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)Show more11:23 AMClaude responded: The problem is you created limiter in app.The problem is you created limiter in app.py but you're trying to use it in post_res.py — they're separate files so post_res.py has no idea that limiter exists, hence the "not defined" error.

Fix — create a separate limiter.py file
Step 1 — Create limiter.py in your Endpoints folder:
pythonfrom slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
Step 2 — Update app.py to import from it:
pythonfrom slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from backend.Endpoints.limiter import limiter  # import from limiter.py

app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
Step 3 — In post_res.py import from it:
pythonfrom .limiter import limiter
from fastapi import APIRouter, HTTPException, Request

Why this works
By defining limiter in its own file, both app.py and post_res.py import the same instance of the limiter — so when app.py registers it with FastAPI, it's the same object that post_res.py uses on the decorator.You said: what seems to be the problemwhat seems to be the problem11:27 AMClaude responded: Looking at your import on line 6:Looking at your import on line 6:
pythonfrom .backend.rate_lim import limiter  # wrong
The dot . means "current package" — but you're already inside the Endpoints folder, so .backend.rate_lim doesn't exist from there.
Your rate_lim.py is in the same Endpoints folder as user_postrespo.py, so the correct import is just:
pythonfrom .rate_lim import limiter  # correct
Just one dot, then directly rate_lim — no backend in between.You said: is it normal for the request to be darkis it normal for the request to be dark11:28 AMClaude responded: Yes, that's completely normal.Yes, that's completely normal. The request parameter appears darker because Pylance detects that you never directly use it inside the function body — it's flagging it as an unused variable.
But it's still required to be there because slowapi needs it to work — it reads the request object behind the scenes to get the client's IP address for rate limiting.
You can safely ignore that warning. The code will work correctly.You said: can I just put the rate_lim contents to the app.can I just put the rate_lim contents to the app.py11:29 AMClaude responded: Yes, absolutely.Yes, absolutely. Since app.py is where you set up the FastAPI app, you can just define the limiter there and import it in your endpoint files directly from app.py.
But there's actually a circular import problem if you do that:
app.py creates limiter
    ↓
user_postrespo.py imports limiter from app.py
    ↓
app.py imports router from user_postrespo.py
    ↓
circular import — app.py imports user_postrespo.py 
which imports app.py which imports user_postrespo.py...

That's exactly why rate_lim.py exists
It's a neutral file that neither app.py nor user_postrespo.py depends on — both just import from it without creating a loop:
rate_lim.py (no imports from your project)
    ↑           ↑
app.py    user_postrespo.py

So the answer is
Technically you can try, but you'll likely hit a circular import error. The separate rate_lim.py file is the standard way to solve this and it's only 3 lines — it's worth keeping it as its own file.You said: I moved it to the app.from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

app = FastAPI()
app.state.limiter = limiter  
app.add_exception_handler(429, limiter._rate_limit_exceeded_handler)I moved it to the app.py is there anything wrong?11:37 AMClaude responded: Yes, a few things to fix:Yes, a few things to fix:

Problem 1 — FastAPI not shown as imported
Make sure FastAPI is in your imports:
pythonfrom fastapi import FastAPI

Problem 2 — Wrong exception handler reference
pythonapp.add_exception_handler(429, limiter._rate_limit_exceeded_handler)  # wrong
limiter._rate_limit_exceeded_handler doesn't exist. The handler comes from slowapi directly:
pythonfrom slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # correct

Problem 3 — Circular import when endpoint files import from app.py
As discussed, importing limiter from app.py into your endpoint files will cause a circular import because app.py also imports those endpoint routers.

The cleanest solution for your setup
Keep limiter in app.py but pass it through the router files is not straightforward. The rate_lim.py approach is still the safest. It's literally just:
python# rate_lim.py
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
Then in app.py:
pythonfrom .Endpoints.rate_lim import limiter
And in user_postrespo.py:
pythonfrom .rate_lim import limiter
No circular imports, clean and simple.from fastapi import FastAPI, Request
from backend.Endpoints import admin_auth, admin_getdashboard, user_getservice, user_postrespo
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

app = FastAPI()
app.state.limiter = limiter  
app.add_exception_handler(429, limiter._rate_limit_exceeded_handler)  

app.include_router(admin_auth.router)
app.include_router(admin_getdashboard.router)
app.include_router(user_postrespo.router)
app.include_router(user_getservice.router)

this is the full code for app.pyShow more11:37 AMClaude responded: Here are the issues:Here are the issues:

Problem 1 — Wrong exception handler
pythonapp.add_exception_handler(429, limiter._rate_limit_exceeded_handler)  # wrong
Fix:
pythonfrom slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # correct

Problem 2 — Circular import will happen
Your app.py imports user_postrespo which imports limiter from rate_lim.py. If you move limiter to app.py, then user_postrespo would need to import from app.py, but app.py already imports user_postrespo — circular import.

Problem 3 — Request is imported but unused
pythonfrom fastapi import FastAPI, Request  # Request not needed here
Remove Request from this import — it's only needed in the endpoint files.

Correct app.py should look like:
pythonfrom fastapi import FastAPI
from backend.Endpoints import admin_auth, admin_getdashboard, user_getservice, user_postrespo
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from backend.Endpoints.rate_lim import limiter

app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(admin_auth.router)
app.include_router(admin_getdashboard.router)
app.include_router(user_postrespo.router)
app.include_router(user_getservice.router)
Keep rate_lim.py as its own file — it's the cleanest solution and avoids all circular import issues.You said: The error shows when you exceed 5 request per minute but it still records when exceeding the limitThe error shows when you exceed 5 request per minute but it still records when exceeding the limit11:49 AMClaude responded: That's because your rate limiter is rejecting the request after the CSV write already happened.That's because your rate limiter is rejecting the request after the CSV write already happened. The issue is the order of operations — slowapi should intercept the request before your function runs, but something is off.

Most likely cause — decorator order is wrong
The order of decorators matters in Python. It should be:
python# correct order
@router.post("/submit_survey_response", response_model=SuccessResponse)
@limiter.limit("5/minute")
def post_response(request: Request, response: SurveyResponse):
If it's the other way around:
python# wrong order
@limiter.limit("5/minute")
@router.post("/submit_survey_response", response_model=SuccessResponse)
def post_response(request: Request, response: SurveyResponse):
The rate limiter won't intercept correctly and the function body runs first before the limit is checked.

Double check your current code
Look at your user_postrespo.py and confirm the decorator order matches the correct version above — @router.post first, then @limiter.limit second, then the function definition.

If decorator order is already correct
Then the issue might be that app.state.limiter isn't being recognized properly. Make sure your app.py has:
pythonfrom backend.Endpoints.rate_lim import limiter

app.state.limiter = limiter  # this line must be present
Without app.state.limiter = limiter, FastAPI doesn't know to enforce the limits even if the decorator is there.You said: its proper but the request still goes through@router.post("/submit_survey_response", response_model=SuccessResponse)
@limiter.limit("5/minute")
def post_response(request: Request, response: SurveyResponse):
    try:

        with DATA_FILE.open("a", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=CSV_HEADERS)

            writer.writerow({
                "service_id": response.service_id,
                "service_availed": response.service_availed,
                "respondent_name": response.respondent_name,
                "date_of_visit": response.date_of_visit,
                "age_bracket": response.age_bracket,
                "gender": response.gender,
                "category_of_respondent": response.category_of_respondent,
                "cc1": response.cc1,
                "cc2": response.cc2,
                "cc3": response.cc3,
                "service_satisfaction(1-5)": response.service_satisfaction,
                "service_time(1-5)": response.service_time,
                "service_requirements(1-5)": response.service_requirements,
                "service_steps(1-5)": response.service_steps,
                "service_transaction(1-5)": response.service_transaction,
                "service_fee(1-5 or N/A)": response.service_fee,
                "service_fair(1-5)": response.service_fair,
                "service_courtesy(1-5)": response.service_courtesy,
                "service_request(1-5)": response.service_request,
                "comments_suggestions": response.comments_suggestions,
                "attending_employee": response.attending_employee,
                "comments_suggestions_for_employee": response.comments_suggestions_for_employee,
            })

        return { "Message": "Survey submitted successfully."}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Could not save survey response: {exc}")its proper but the request still goes throughShow more11:51 AMClaude responded: The issue is your broad except Exception is catching the rate limit exception before it can block the request.The issue is your broad except Exception is catching the rate limit exception before it can block the request.
When slowapi tries to raise the RateLimitExceeded exception, your try/except catches it and instead tries to write to the CSV, then raises a 500 error.

Fix — import and exclude RateLimitExceeded from your except block
pythonfrom slowapi.errors import RateLimitExceeded

@router.post("/submit_survey_response", response_model=SuccessResponse)
@limiter.limit("5/minute")
def post_response(request: Request, response: SurveyResponse):
    try:
        with DATA_FILE.open("a", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=CSV_HEADERS)
            writer.writerow({
                # ... your existing code
            })
        return {"Message": "Survey submitted successfully."}
    except RateLimitExceeded:
        raise  # re-raise it so slowapi handles it properly
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Could not save survey response: {exc}")

What this does
Request comes in
        ↓
Rate limit exceeded?
        ↓
RateLimitExceeded raised
        ↓
except RateLimitExceeded → re-raises it
        ↓
slowapi handles it → returns 429
        ↓
CSV never gets written
By catching RateLimitExceeded first and re-raising it, you let slowapi handle it properly before the broad except Exception swallows it.You said: how do I change the Error: unprocessable entity to my custom error messagehow do I change the Error: unprocessable entity to my custom error message11:54 AMClaude responded: You already have the exception handler in main.You already have the exception handler in main.py for this — the issue is it's returning the full Pydantic error format instead of your custom one.
Check your app.py — you should have this:
pythonfrom fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import Request

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()[0]["msg"]}
    )
If that's already there but still showing the full error, the problem is likely that the handler is defined after app.include_router(...) calls. Make sure it's defined before the routers:
pythonapp = FastAPI()

# exception handlers first
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()[0]["msg"]}
    )

# routers after
app.include_router(admin_auth.router)
app.include_router(admin_getdashboard.router)
app.include_router(user_postrespo.router)
app.include_router(user_getservice.router)
This should return your clean custom message like:
json{
    "detail": "Value error, Service ID must be one of SV001, SV002, SV003."
}You said: what do I need to do in frontend to send a request to the backend using streamlit and pythonwhat do I need to do in frontend to send a request to the backend using streamlit and python3:33 PMClaude responded: Here's everything you need to know:Here's everything you need to know:

Install the HTTP library
bashpip install httpx
httpx is the recommended library for making HTTP requests in Streamlit — it works the same as requests but supports async.

Basic concept
pythonimport httpx

response = httpx.post("http://localhost:8000/endpoint", json={...})
data = response.json()

The 4 things you always need to handle
1. Making the request:
pythonresponse = httpx.post(
    "http://localhost:8000/submit_survey_response",
    json={"service_id": "SV001", ...}
)
2. Checking if it succeeded:
pythonif response.status_code == 200:
    st.success("Survey submitted!")
elif response.status_code == 422:
    st.error(response.json()["detail"])
elif response.status_code == 429:
    st.error("Too many requests. Please wait a minute.")
else:
    st.error("Something went wrong.")
3. Reading the response:
pythondata = response.json()
service_name = data["service_name"]
4. Handling connection errors (backend not running):
pythontry:
    response = httpx.post("http://localhost:8000/login", json={...})
except httpx.ConnectError:
    st.error("Cannot connect to the server. Make sure the backend is running.")

For each of your endpoints
GET request (no body):
pythonresponse = httpx.get("http://localhost:8000/get_available_services")
data = response.json()
services = data["services"]
POST with JSON body:
pythonresponse = httpx.post(
    "http://localhost:8000/login",
    json={
        "username": username,
        "password": password
    }
)
POST with credentials + query parameter:
pythonresponse = httpx.post(
    "http://localhost:8000/service_summary",
    json={
        "username": st.session_state["username"],
        "password": st.session_state["password"]
    },
    params={"preset_range": "last_week"}  # optional query parameter
)

Session state flow for your app
python# after successful login
if response.status_code == 200:
    data = response.json()
    st.session_state["logged_in"] = True
    st.session_state["username"] = data["username"]
    st.session_state["password"] = password  # save original input
    st.session_state["service_id"] = data["service_id"]
    st.session_state["service_name"] = data["service_name"]
    st.switch_page("pages/dashboard.py")  # redirect to dashboard

Protecting the dashboard page
Add this at the top of every protected page:
pythonif "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.error("You must log in first.")
    st.stop()

Summary of what to remember
ThingHowGET requesthttpx.get(url)POST requesthttpx.post(url, json={...})Query parametersparams={"key": "value"}Read responseresponse.json()Check statusresponse.status_codeConnection errorwrap in try/except httpx.ConnectErrorPass credentialsalways use st.session_stateYou said: how do I call the backend using request this was my initial idea    with st.form("survey_form"):
        st.subheader("I. Profile")
        col1, col2 = st.columns(2)
        with col1:
            service = st.selectbox("Service Availed", ["Clinic","Accounting","MISU","Library","Registrar"])
            name = st.text_input("Respondent Name")
            date_visit = st.date_input("Date Visited")
        with col2:
            gender = st.selectbox("Gender Upon Birth", ["Male","Female","Prefer not to say"])
            age = st.selectbox("Age Bracket", ["Below 18","18-30","31-45","46-60","60+"])
            category = st.selectbox("Category", ["Student","Faculty","Staff","Visitor"])how do I call the backend using request this was my initial ideaimport streamlit as st 
import requests


r = requests.get('http://localhost:8000/get_available_services')

st.selectbox("Service Availed", [service['service_name'] for service in r.json()])Show more3:55 PMClaude responded: Your idea is correct!Your idea is correct! But there are a few things to improve:

Problems with your current approach
1. API call inside the form will re-call on every interaction
Every time the user clicks anything on the page, Streamlit reruns and calls the API again. Fix this by caching the API call:
python@st.cache_data
def get_services():
    r = requests.get("http://localhost:8000/get_available_services")
    return r.json()["services"]
2. No error handling if backend is down
pythontry:
    services = get_services()
except requests.exceptions.ConnectionError:
    st.error("Cannot connect to the server. Make sure the backend is running.")
    st.stop()
3. You need both service_name for display and service_id for submission
When you submit the form you need to send service_id not service_name. So store the mapping:
pythonservices = get_services()
service_names = [s["service_name"] for s in services]
service_map = {s["service_name"]: s["service_id"] for s in services}

Putting it all together
pythonimport streamlit as st
import requests

@st.cache_data
def get_services():
    r = requests.get("http://localhost:8000/get_available_services")
    return r.json()["services"]

# fetch services before the form
try:
    services = get_services()
    service_names = [s["service_name"] for s in services]
    service_map = {s["service_name"]: s["service_id"] for s in services}
except requests.exceptions.ConnectionError:
    st.error("Cannot connect to server.")
    st.stop()

with st.form("survey_form"):
    st.subheader("I. Profile")
    col1, col2 = st.columns(2)
    with col1:
        selected_service = st.selectbox("Service Availed", service_names)
        name = st.text_input("Respondent Name")
        date_visit = st.date_input("Date Visited")
    with col2:
        gender = st.selectbox("Gender", ["Male", "Female"])
        age = st.selectbox("Age Bracket", ["16-Below", "17-20", "21-25", "26 and up"])
        category = st.selectbox("Category", ["Student", "Alumni", "Faculty"])

    submitted = st.form_submit_button("Submit")

    if submitted:
        service_id = service_map[selected_service]  # get the ID from the name
        # use service_id when sending to backend

Key things to note

@st.cache_data — calls the API once and caches the result, no repeated calls on every rerender
service_map — lets you display friendly names but send IDs to the backend
Make sure your selectbox options match exactly what your validators accept — gender for example only accepts Male or Female in your backend, not Prefer not to say
You said: how do you write a post request , for example in a survey form, how do you create the json and payloadhow do you write a post request , for example in a survey form, how do you create the json and payload4:20 PMClaude responded: Here's how you build and send the POST request from your survey form:Here's how you build and send the POST request from your survey form:

Step 1 — Collect all form values on submit
pythonsubmitted = st.form_submit_button("Submit Survey")

if submitted:
    # build the payload from form inputs
    payload = {
        "service_id": service_map[selected_service],
        "service_availed": service_availed,
        "respondent_name": name,
        "date_of_visit": date_visit.strftime("%d/%m/%Y"),  # convert date to string
        "age_bracket": age,
        "gender": gender,
        "category_of_respondent": category,
        "cc1": cc1,
        "cc2": cc2,
        "cc3": cc3,
        "service_satisfaction": int(service_satisfaction),
        "service_time": int(service_time),
        "service_requirements": int(service_requirements),
        "service_steps": int(service_steps),
        "service_transaction": int(service_transaction),
        "service_fee": service_fee,
        "service_fair": int(service_fair),
        "service_courtesy": int(service_courtesy),
        "service_request": int(service_request),
        "comments_suggestions": comments,
        "attending_employee": employee,
        "comments_suggestions_for_employee": employee_comments
    }

Step 2 — Send the POST request
python    try:
        response = requests.post(
            "http://localhost:8000/submit_survey_response",
            json=payload  # automatically sets Content-Type to application/json
        )

        if response.status_code == 200:
            st.success("Survey submitted successfully!")

        elif response.status_code == 422:
            st.error(response.json()["detail"])

        elif response.status_code == 429:
            st.error("Too many submissions. Please wait a minute.")

        else:
            st.error("Something went wrong. Please try again.")

    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to server. Make sure the backend is running.")

Important things to watch out for
Date formatting — Streamlit's date_input returns a Python date object, your backend expects a string in DD/MM/YYYY:
python"date_of_visit": date_visit.strftime("%d/%m/%Y")
Ratings as integers — if you use sliders or selectboxes for ratings, make sure they're sent as int not str:
python"service_satisfaction": int(service_satisfaction)
service_fee — this is the only rating sent as a string since it can be "N/A":
python"service_fee": service_fee  # already a string, no int() needed

Full structure of the submit block
Form submitted
      ↓
Build payload dict
      ↓
POST to /submit_survey_response with json=payload
      ↓
Check response.status_code
      ↓
200 → st.success()
422 → st.error(response.json()["detail"])
429 → st.error("Too many requests")
else → st.error("Something went wrong")You said: where would you call the payload after, like how should the post request look likewhere would you call the payload after, like how should the post request look like4:23 PMClaude responded: Here's exactly how it looks all together:Here's exactly how it looks all together:
pythonif submitted:
    # Step 1 - build the payload
    payload = {
        "service_id": service_map[selected_service],
        "service_availed": service_availed,
        "respondent_name": name,
        "date_of_visit": date_visit.strftime("%d/%m/%Y"),
        "age_bracket": age,
        "gender": gender,
        "category_of_respondent": category,
        "cc1": cc1,
        "cc2": cc2,
        "cc3": cc3,
        "service_satisfaction": int(service_satisfaction),
        "service_time": int(service_time),
        "service_requirements": int(service_requirements),
        "service_steps": int(service_steps),
        "service_transaction": int(service_transaction),
        "service_fee": service_fee,
        "service_fair": int(service_fair),
        "service_courtesy": int(service_courtesy),
        "service_request": int(service_request),
        "comments_suggestions": comments,
        "attending_employee": employee,
        "comments_suggestions_for_employee": employee_comments
    }

    # Step 2 - send the payload
    try:
        response = requests.post(
            "http://localhost:8000/submit_survey_response",
            json=payload
        )

        # Step 3 - handle the response
        if response.status_code == 200:
            st.success("Survey submitted successfully!")
        elif response.status_code == 422:
            st.error(response.json()["detail"])
        elif response.status_code == 429:
            st.error("Too many submissions. Please wait a minute.")
        else:
            st.error("Something went wrong. Please try again.")

    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to server. Make sure the backend is running.")

The key thing to understand
json=payload is all you need — requests automatically:

Converts your Python dict to a JSON string
Sets the Content-Type: application/json header
Sends it in the request body

So you never need to manually call json.dumps() or set headers yourself when using json=payload.You said: is this correct for calling the services available?def get_services():
    r = requests.get("http://127.0.0.1:8000/get_available_services")
    if r.status_code == 200:
        return r.json().get("services", [])
    else:
        st.error("Failed to load services.")
        return ["services"]

try:
    services = get_services()
    service_names = [service["service_name"] for service in services]
    service_map = {service["service_name"]: service["service_id"] for service in services}
except requests.exceptions.ConnectionError:
    st.error("Cannot connect to server.")
    st.stop()



    with st.form("survey_form"):
        st.subheader("I. Profile")
        col1, col2 = st.columns(2)
        with col1:
            service = st.selectbox("Service Availed", service_names)is this correct for calling the services available?Show more5:39 PMClaude responded: Almost correct, but there are two issues:Almost correct, but there are two issues:

Problem 1 — Indentation of st.form is wrong
Your with st.form(...) block is indented inside the except block, which means the form only shows when there's a connection error. It should be at the top level:
pythontry:
    services = get_services()
    service_names = [service["service_name"] for service in services]
    service_map = {service["service_name"]: service["service_id"] for service in services}
except requests.exceptions.ConnectionError:
    st.error("Cannot connect to server.")
    st.stop()

# form is outside and after the try/except
with st.form("survey_form"):
    st.subheader("I. Profile")
    ...

Problem 2 — Missing @st.cache_data
Without caching, every interaction on the page (clicking, typing) triggers a full rerun and calls the API again:
python@st.cache_data
def get_services():
    r = requests.get("http://127.0.0.1:8000/get_available_services")
    if r.status_code == 200:
        return r.json().get("services", [])
    else:
        st.error("Failed to load services.")
        return []
Also change return ["services"] to return [] in your error case — returning a list with the string "services" in it would break your service_names and service_map logic.

Everything else looks correct — the service_map pattern and the selectbox usage are good.You said: Correct the indentationdef get_services():
    r = requests.get("http://127.0.0.1:8000/get_available_services")
    if r.status_code == 200:
        return r.json().get("services", [])
    else:
        st.error("Failed to load services.")
        return ["services"]
    try:
        services = get_services()
        service_names = [service["service_name"] for service in services]
        service_map = {service["service_name"]: service["service_id"] for service in services}
    except requests.exceptions.ConnectionError:
    st.error("Cannot connect to server.")
    st.stop()Correct the indentationShow more5:41 PMClaude responded: Here's the corrected code:Here's the corrected code:
python@st.cache_data
def get_services():
    r = requests.get("http://127.0.0.1:8000/get_available_services")
    if r.status_code == 200:
        return r.json().get("services", [])
    else:
        st.error("Failed to load services.")
        return []

try:
    services = get_services()
    service_names = [service["service_name"] for service in services]
    service_map = {service["service_name"]: service["service_id"] for service in services}
except requests.exceptions.ConnectionError:
    st.error("Cannot connect to server.")
    st.stop()

What changed

try/except block is outside the function — it was accidentally inside it before, which means it would never run
return [] instead of return ["services"]
Added @st.cache_data so it doesn't call the API on every rerender
except block is properly unindented to match the try
You said: this is the frontend code, how im I able to call the get servicesdef survey_page():
    if st.button("← Back to Home"):
        st.session_state.current_page = "home"
        st.rerun()

    st.title("Service Satisfaction Survey")
    office = st.selectbox("Office/Department", list(OFFICE_CREDS.keys()))
    st.divider()
    st.header("I. Profile Informatipastedthis is the frontend code, how im I able to call the get services6:00 PMClaude responded: Looking at your frontend code, here's how to integrate the API call for services:Looking at your frontend code, here's how to integrate the API call for services:

What needs to change
Right now your code has:
pythonoffice = st.selectbox("Office/Department", list(OFFICE_CREDS.keys()))
and
pythonservice = st.selectbox("Service Availed (Required)", service_names)
service_names isn't defined anywhere in your code yet — that's what you need to add.

Add this at the top of your file
pythonimport requests
import streamlit as st
from datetime import date

BASE_URL = "http://127.0.0.1:8000"

@st.cache_data
def get_services():
    try:
        r = requests.get(f"{BASE_URL}/get_available_services")
        if r.status_code == 200:
            return r.json().get("services", [])
        else:
            st.error("Failed to load services.")
            return []
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to server. Make sure the backend is running.")
        return []

Then at the start of survey_page() before the form:
pythondef survey_page():
    if st.button("← Back to Home"):
        st.session_state.current_page = "home"
        st.rerun()

    # fetch services from backend
    services = get_services()
    if not services:
        st.stop()  # stop if services failed to load

    service_names = [s["service_name"] for s in services]
    service_map = {s["service_name"]: s["service_id"] for s in services}

    st.title("Service Satisfaction Survey")
    # remove the office selectbox since service comes from the API now
    ...

Then update the selectbox:
python# replace this
service = st.selectbox("Service Availed (Required)", service_names)

# with this — same thing, service_names now comes from the API
selected_service = st.selectbox("Service Availed (Required)", service_names)

Then when submitting, use service_map to get the service_id:
pythonif st.button("Submit Survey"):
    service_id = service_map[selected_service]  # get ID from name

    payload = {
        "service_id": service_id,  # send ID not name
        "service_availed": selected_service,
        # ... rest of your fields
    }

    try:
        response = requests.post(f"{BASE_URL}/submit_survey_response", json=payload)
        if response.status_code == 200:
            st.success("Survey submitted successfully!")
        elif response.status_code == 422:
            st.error(response.json()["detail"])
        elif response.status_code == 429:
            st.error("Too many submissions. Please wait a minute.")
        else:
            st.error("Something went wrong.")
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to server.")questions = [
        "I am satisfied with the service that I availed",
        "I spent a reasonable amount of time for my transaction",
        "The office followed the transaction’s requirements and steps based on the information provided",
        "The steps (including payment) I needed to do for my transaction were easy and simple",
        "I easily found information about my transaction from the office or its website",
        "I paid a reasonable amount of fees for my transaction. (If service was free, mark the N/A column)",
        "I feel the office was fair to everyone, or “walang palakasan” during my transaction.",
        "I was treated courteously by the staff, and if (If assisted for help) the staff was helpful",
        "I got what I needed from the government office, or it (if needed) denial of request was sufficiently explained to me"
    ]


can you give me an example how I can this individually like
 service_satisfaction = st.radio (
        "I am satisfied with the service that I availed?",
        standard_scale,                       
                                     )
    ratings = {}
    standard_scale = ["1", "2", "3", "4", "5"]
    fees_scale = ["1", "2", "3", "4", "5", "N/A"]

    for q in questions:
        scale = fees_scale if "fees for my transaction" in q else standard_scale
        ratings[q] = st.radio(q, scale, horizontal=True)Show more6:27 PMClaude responded: Here's how to define each rating individually instead of using the loop:Here's how to define each rating individually instead of using the loop:
pythonstandard_scale = ["1", "2", "3", "4", "5"]
fees_scale = ["1", "2", "3", "4", "5", "N/A"]

service_satisfaction = st.radio(
    "I am satisfied with the service that I availed.",
    standard_scale,
    horizontal=True
)

service_time = st.radio(
    "I spent a reasonable amount of time for my transaction.",
    standard_scale,
    horizontal=True
)

service_requirements = st.radio(
    "The office followed the transaction's requirements and steps based on the information provided.",
    standard_scale,
    horizontal=True
)

service_steps = st.radio(
    "The steps (including payment) I needed to do for my transaction were easy and simple.",
    standard_scale,
    horizontal=True
)

service_transaction = st.radio(
    "I easily found information about my transaction from the office or its website.",
    standard_scale,
    horizontal=True
)

service_fee = st.radio(
    "I paid a reasonable amount of fees for my transaction. (If service was free, mark the N/A column)",
    fees_scale,  # this one uses fees_scale since it has N/A
    horizontal=True
)

service_fair = st.radio(
    "I feel the office was fair to everyone, or 'walang palakasan' during my transaction.",
    standard_scale,
    horizontal=True
)

service_courtesy = st.radio(
    "I was treated courteously by the staff, and if assisted for help, the staff was helpful.",
    standard_scale,
    horizontal=True
)

service_request = st.radio(
    "I got what I needed from the government office, or denial of request was sufficiently explained to me.",
    standard_scale,
    horizontal=True
)

Then in your payload map them directly:
pythonpayload = {
    ...
    "service_satisfaction": int(service_satisfaction),
    "service_time": int(service_time),
    "service_requirements": int(service_requirements),
    "service_steps": int(service_steps),
    "service_transaction": int(service_transaction),
    "service_fee": service_fee,  # no int() since it can be "N/A"
    "service_fair": int(service_fair),
    "service_courtesy": int(service_courtesy),
    "service_request": int(service_request),
    ...
}

Why individual over the loop
Loop approachIndividual approachLess codeMore code but clearerHarder to map to specific payload keysEach variable maps directly to its payload fieldEasy to make mistakes in key mappingNo ambiguity — variable name matches payload key    # --- III. SERVICE QUALITY ---
    st.divider()
    st.header("III. Service Quality")
    st.caption("Please rate your experience from 1 (Strongly Disagree) to 5 (Strongly Agree).")

    ratings = {}
    standard_scale = ["1", "2", "3", "4", "5"]
    fees_scale = ["1", "2", "3", "4", "5", "N/A"]

    service_satisfaction = st.radio (
        "I am satisfied with the service that I availed?",
        standard_scale,   
        horizontal=True                    
    )

    service_time = st.radio (
        "I spent a reasonable amount of time for my transaction",
        standard_scale,   
        horizontal=True                    
    )

    service_requirements = st.radio (
        "The office followed the transaction’s requirements and steps based on the information provided",
        standard_scale,   
        horizontal=True                    
    )

    service_steps = st.radio (
        "The steps (including payment) I needed to do for my transaction were easy and simple",
        standard_scale,
        horizontal=True
    )

    service_transaction = st.radio (
        "I easily found information about my transaction from the office or its website",
        standard_scale,
        horizontal=True
    )

    service_fee = st.radio (
        "I paid a reasonable amount of fees for my transaction. (If service was free, mark the N/A column)",
        fees_scale,
        horizontal=True
    )

    service_fair = st.radio (
        "I feel the office was fair to everyone, or “walang palakasan” during my transaction.",
        standard_scale,
        horizontal=True
    )

    service_courtesy = st.radio (
        "I was treated courteously by the staff, and if (If assisted for help) the staff was helpful",
        standard_scale,
        horizontal=True
    )

    service_request = st.radio (
        "I got what I needed from the government office, or it (if needed) denial of request was sufficiently explained to me",
        standard_scale,
        horizontal=True
    )


    for q in questions:
        scale = fees_scale if "fees for my transaction" in q else standard_scale
        ratings[q] = st.radio(q, scale, horizontal=True) what is this forShow more6:33 PMClaude responded: The for q in questions loop at the bottom is leftover code from the old approach — it's now redundant since you've already defined each rating individually abo…The for q in questions loop at the bottom is leftover code from the old approach — it's now redundant since you've already defined each rating individually above it.
It's basically doing the same thing twice — creating duplicate radio buttons for the same questions. You should delete it entirely:
python# DELETE this entire block
for q in questions:
    scale = fees_scale if "fees for my transaction" in q else standard_scale
    ratings[q] = st.radio(q, scale, horizontal=True)
Also the ratings = {} dictionary at the top is no longer needed either since you're not using it anymore — you can remove that too.

Also — syntax error in service_fair
pythonservice_fair = st.radio (
    "I feel the office was fair to everyone, or "walang palakasan" during my transaction.",
The double quotes around walang palakasan are breaking the string. Use single quotes inside:
pythonservice_fair = st.radio (
    "I feel the office was fair to everyone, or 'walang palakasan' during my transaction.",
    standard_scale,
    horizontal=True
)You said: where is the submit button heredef survey_page():
    if st.button("← Back to Home"):
        st.session_state.current_page = "home"
        st.rerun()


    # fetch services from backend
    services = get_services()
    if not services:
        st.stop()  # stop if services failed to load

    service_names = [s["serpastedwhere is the submit button here6:45 PMClaude responded: The submit button is already there at the bottom of your code:The submit button is already there at the bottom of your code:
pythonif st.button("Submit Survey"):
But there are a few issues to fix:

Problem 1 — service_id is wrong
pythonservice_id = st.selectbox("Office/Department", service_names)
This stores the service name not the service ID. Fix:
pythonselected_service = st.selectbox("Office/Department", service_names)
Then in the payload:
python"service_id": service_map[selected_service],  # get ID from the map

Problem 2 — Date format is wrong
python"date_of_visit": str(date_visit),  # gives "2026-05-18" (wrong format)
Your backend expects DD/MM/YYYY:
python"date_of_visit": date_visit.strftime("%d/%m/%Y"),  # correct

Problem 3 — Not actually calling the API
Your submit button currently just appends to st.session_state — it never sends anything to the backend:
python# remove this
st.session_state.survey_submissions.append(submission_payload)

# replace with this
try:
    response = requests.post(
        "http://127.0.0.1:8000/submit_survey_response",
        json=submission_payload
    )
    if response.status_code == 200:
        st.success("Survey submitted successfully!")
    elif response.status_code == 422:
        st.error(response.json()["detail"])
    elif response.status_code == 429:
        st.error("Too many submissions. Please wait a minute.")
    else:
        st.error("Something went wrong.")
except requests.exceptions.ConnectionError:
    st.error("Cannot connect to server.")

Problem 4 — cc1 options have "Option A/B/C/D" prefix
Your backend validator expects exact strings like:
"I know what a CC is and I saw this office's CC"
But your frontend sends:
"Option A: I know what a CC is and I saw this office's CC"
Either remove the prefix from your cc1_options list, or strip it before sending:
python"cc1": cc1.split(": ", 1)[1],  # removes "Option A: " prefixYou said: why does it errorwhy does it error6:49 PMClaude responded: Looking at your code, the st.Looking at your code, the st.error on line 389 is not indented inside the except block — it's outside it:
python# wrong - st.error is outside the except block
except requests.exceptions.ConnectionError:
st.error("Cannot connect to server.")  # should be indented
Fix:
python# correct
except requests.exceptions.ConnectionError:
    st.error("Cannot connect to server.")  # indented inside except

Also looking more carefully at your code, the entire try block starting at line 375 appears to be outside the if st.button("Submit Survey"): block — it should be indented inside it:
pythonif st.button("Submit Survey"):
    if not service_availed.strip() ...:
        st.error("Please complete all required fields.")
    else:
        submission_payload = { ... }
        
        try:                                          # indented inside else
            response = requests.post(...)
            if response.status_code == 200:
                st.success("Survey submitted successfully!")
            elif response.status_code == 422:
                st.error(response.json()["detail"])
            elif response.status_code == 429:
                st.error("Too many submissions. Please wait a minute.")
            else:
                st.error("Something went wrong.")
        except requests.exceptions.ConnectionError:   # same level as try
            st.error("Cannot connect to server.")     # indented inside except            submission_payload = {
                "service_id": str(service_id),
                "service_availed": str(service_availed),
                "respondent_name": str(name),
                "date_of_visit": str(date_visit),
                "age_bracket": str(age),
                "gender": str(gender),
                "category_of_respondent": str(final_category),
                "cc1": cc1.split(": ", 1)[1],
                "cc2": str(cc2),
                "cc3": str(cc3),
                "service_satisfaction": int(service_satisfaction),
                "service_time": int(service_time),
                "service_requirements": int(service_requirements),
                "service_steps": int(service_steps),
                "service_transaction": int(service_transaction),
                "service_fee": str(service_fee),
                "service_fair": int(service_fair),
                "service_courtesy": int(service_courtesy),
                "service_request": int(service_request),
                "comments_suggestions": str(comments_suggestions),
                "attending_employee": str(attending_employee),
                "comments_suggestions_for_employee": str(comments_suggestions_for_employee)
            }

is the payload correct?Show more6:52 PMClaude responded: Almost, but there are a few issues:Almost, but there are a few issues:

Problem 1 — service_id is still the service name
python"service_id": str(service_id),  # this is actually the service name
You need to use service_map to get the actual ID:
python"service_id": service_map[selected_service],

Problem 2 — Date format is wrong
python"date_of_visit": str(date_visit),  # gives "2026-05-18"
Backend expects DD/MM/YYYY:
python"date_of_visit": date_visit.strftime("%d/%m/%Y"),  # gives "18/05/2026"

Problem 3 — age has wrong options
Your selectbox has:
python["Below 16", "17-20", "21-25", "26 and up"]
But your backend validator expects:
python["16-Below", "17-20", "21-25", "26 and up"]
Either fix the selectbox options or the validator — they need to match exactly.

Problem 4 — cc1 split could fail
python"cc1": cc1.split(": ", 1)[1],
This works for "Option A: I know..." but if the format ever changes it will throw an IndexError. It's safer to use a mapping:
pythoncc1_map = {
    "Option A: I know what a CC is and I saw this office's CC": "I know what a CC is and I saw this office's CC",
    "Option B: I know what a CC is but I did not see this office's CC": "I know what a CC is but I did not see this office's CC",
    "Option C: I learned of the CC only when I saw this office's CC": "I learned of the CC only when I saw this office's CC",
    "Option D: I do not know what a CC is and did not see one in this office": "I do not know what a CC is and did not see one in this office"
}
# then in payload
"cc1": cc1_map[cc1],

Everything else looks correct ✅

Ratings as int() ✅
service_fee as str() ✅
Comments as str() ✅
cc2 and cc3 as str() ✅
You said: can you double check and correct the mistakes it should be able to pass the post request to the backenddef survey_page():
    if st.button("← Back to Home"):
        st.session_state.current_page = "home"
        st.rerun()


    # fetch services from backend
    services = get_services()
    if not services:
        st.stop()  # stop if services failed to load

    service_names = [s["serpastedcan you double check and correct the mistakes it should be able to pass the post request to the backend6:59 PMClaude responded: Here's the corrected full survey_page() function:Here's the corrected full survey_page() function:
pythondef survey_page():
    if st.button("← Back to Home"):
        st.session_state.current_page = "home"
        st.rerun()

    # fetch services from backend
    services = get_services()
    if not services:
        st.stop()

    service_names = [s["service_name"] for s in services]
    service_map = {s["service_name"]: s["service_id"] for s in services}

    st.title("Service Satisfaction Survey")
    selected_service = st.selectbox("Office/Department", service_names)
    st.divider()
    st.header("I. Profile Information")

    col1, col2 = st.columns(2)
    with col1:
        service_availed = st.text_input("Service Availed (Required)")
        name = st.text_input("Respondent Name (Required)")
        date_visit = st.date_input("Date Visited", value=date.today())
    with col2:
        gender = st.selectbox("Gender", ["Male", "Female"])
        age = st.selectbox("Age Bracket", ["16-Below", "17-20", "21-25", "26 and up"])

        categories = [
            "Student", "Alumni", "Employee", "Visitor", "Parent/s", "Supplier",
            "LGU / Government Agency Representative", "Industry Practitioners",
            "Administrative Employee", "Faculty", "Other"
        ]
        selected_category = st.selectbox("Category", categories)

        final_category = selected_category
        custom_category = ""  # initialize here to avoid NameError later
        if selected_category == "Other":
            custom_category = st.text_input("Please specify your category (Required)")
            final_category = f"Other ({custom_category})"

    # --- II. CITIZEN'S CHARTER ---
    st.divider()
    st.header("II. Citizen's Charter (CC)")
    st.caption("INSTRUCTIONS: Choose your answer to the Citizen's Charter (CC) questions...")

    cc1_options = [
        "Option A: I know what a CC is and I saw this office's CC",
        "Option B: I know what a CC is but I did not see this office's CC",
        "Option C: I learned of the CC only when I saw this office's CC",
        "Option D: I do not know what a CC is and did not see one in this office"
    ]

    cc1_map = {
        "Option A: I know what a CC is and I saw this office's CC": "I know what a CC is and I saw this office's CC",
        "Option B: I know what a CC is but I did not see this office's CC": "I know what a CC is but I did not see this office's CC",
        "Option C: I learned of the CC only when I saw this office's CC": "I learned of the CC only when I saw this office's CC",
        "Option D: I do not know what a CC is and did not see one in this office": "I do not know what a CC is and did not see one in this office"
    }

    cc1 = st.radio(
        "CC1: Which of the following best describes your awareness of a CC?",
        cc1_options,
        horizontal=False
    )

    cc2 = "N/A"
    cc3 = "N/A"

    if "Option D" not in cc1:
        st.write("")
        cc2 = st.radio(
            "CC2: If aware of CC, would you say that the CC of this office was?",
            ["Easy to see", "Somewhat easy to see", "Difficult to see", "Not visible at all", "N/A"],
            horizontal=True
        )
        st.write("")
        cc3 = st.radio(
            "CC3: If aware of CC, how much did the CC help you in your transaction?",
            ["Helped very much", "Somewhat helped", "Did not help", "N/A"],
            horizontal=True
        )

    # --- III. SERVICE QUALITY ---
    st.divider()
    st.header("III. Service Quality")
    st.caption("Please rate your experience from 1 (Strongly Disagree) to 5 (Strongly Agree).")

    standard_scale = ["1", "2", "3", "4", "5"]
    fees_scale = ["1", "2", "3", "4", "5", "N/A"]

    service_satisfaction = st.radio(
        "I am satisfied with the service that I availed.",
        standard_scale, horizontal=True
    )
    service_time = st.radio(
        "I spent a reasonable amount of time for my transaction.",
        standard_scale, horizontal=True
    )
    service_requirements = st.radio(
        "The office followed the transaction's requirements and steps based on the information provided.",
        standard_scale, horizontal=True
    )
    service_steps = st.radio(
        "The steps (including payment) I needed to do for my transaction were easy and simple.",
        standard_scale, horizontal=True
    )
    service_transaction = st.radio(
        "I easily found information about my transaction from the office or its website.",
        standard_scale, horizontal=True
    )
    service_fee = st.radio(
        "I paid a reasonable amount of fees for my transaction. (If service was free, mark the N/A column)",
        fees_scale, horizontal=True
    )
    service_fair = st.radio(
        "I feel the office was fair to everyone, or 'walang palakasan' during my transaction.",
        standard_scale, horizontal=True
    )
    service_courtesy = st.radio(
        "I was treated courteously by the staff, and if assisted for help, the staff was helpful.",
        standard_scale, horizontal=True
    )
    service_request = st.radio(
        "I got what I needed from the government office, or denial of request was sufficiently explained to me.",
        standard_scale, horizontal=True
    )

    # --- IV. ADDITIONAL FEEDBACK & PERSONNEL ---
    st.divider()
    st.header("IV. Feedback & Attending Personnel")

    comments_suggestions = st.text_area("Comments/Suggestions")

    col_emp1, col_emp2 = st.columns(2)
    with col_emp1:
        attending_employee = st.text_input("Attending Employee (format: Surname, Name)")
    with col_emp2:
        comments_suggestions_for_employee = st.text_area("Comments/Suggestions to the attending employee")

    if st.button("Submit Survey"):
        if not service_availed.strip() or not name.strip() or (selected_category == "Other" and not custom_category.strip()):
            st.error("Submission Failed! Please complete all required profile fields.")
        else:
            submission_payload = {
                "service_id": service_map[selected_service],
                "service_availed": service_availed.strip(),
                "respondent_name": name.strip(),
                "date_of_visit": date_visit.strftime("%d/%m/%Y"),  # fixed format
                "age_bracket": age,
                "gender": gender,
                "category_of_respondent": final_category,
                "cc1": cc1_map[cc1],  # use map instead of split
                "cc2": cc2,
                "cc3": cc3,
                "service_satisfaction": int(service_satisfaction),
                "service_time": int(service_time),
                "service_requirements": int(service_requirements),
                "service_steps": int(service_steps),
                "service_transaction": int(service_transaction),
                "service_fee": service_fee,
                "service_fair": int(service_fair),
                "service_courtesy": int(service_courtesy),
                "service_request": int(service_request),
                "comments_suggestions": comments_suggestions.strip(),
                "attending_employee": attending_employee.strip(),
                "comments_suggestions_for_employee": comments_suggestions_for_employee.strip()
            }

            try:
                response = requests.post(
                    "http://127.0.0.1:8000/submit_survey_response",
                    json=submission_payload
                )
                if response.status_code == 200:
                    st.success("Survey submitted successfully!")
                elif response.status_code == 422:
                    st.error(response.json()["detail"])
                elif response.status_code == 429:
                    st.error("Too many submissions. Please wait a minute.")
                else:
                    st.error("Something went wrong. Please try again.")
            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to server. Make sure the backend is running.")

What was fixed

custom_category = "" initialized before the if selected_category == "Other" block to avoid NameError
date_visit.strftime("%d/%m/%Y") for correct date format
cc1_map instead of .split() for safer cc1 mapping
try/except is now properly indented inside the else block
requests.post(...) has the actual URL filled in
Removed unused ratings = {} dict
You said: how to remove the value error texthow to remove the value error text    
    @field_validator("attending_employee")
    @classmethod
    def validate_attending_employee(cls, value):
        if value.strip() == "":
            raise ValueError("Attending Employee name cannot be empty")
        if len(value) > 60:
            raise ValueError("Attending Employee name cannot exceed 60 characters.")
        return valueShow more9:30 PMClaude responded: The "Value error," prefix comes from Pydantic automatically prepending it to your error message.The "Value error," prefix comes from Pydantic automatically prepending it to your error message. You need to strip it in your exception handler in app.py.
Change your exception handler to remove the prefix:
python@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    raw_msg = exc.errors()[0]["msg"]
    # remove "Value error, " prefix that Pydantic adds
    clean_msg = raw_msg.replace("Value error, ", "")
    return JSONResponse(
        status_code=422,
        content={"detail": clean_msg}
    )
This will turn:
"Value error, Comments and suggestions cannot be empty."
Into:
"Comments and suggestions cannot be empty."You said: what should be on the docs of our project?what should be on the docs of our project?10:28 PMClaude responded: Here's everything that should be in your project documentation:Here's everything that should be in your project documentation:

1. Project Overview

What the system is (RTU School Service Survey System)
Purpose and goals
Who it's for (students as respondents, admins as viewers)
Scope and limitations


2. Features

Student survey submission without an account
Admin login with assigned service
Dashboard with analytics and charts
Raw response viewer per service
Date filtering for responses
Rate limiting on submissions


3. Tech Stack

Backend: FastAPI
Frontend: Streamlit
Data storage: CSV files
Password hashing: PBKDF2 with SHA-256
Libraries: pandas, numpy, slowapi, python-jose, etc.


4. Project Structure
RTU-SURVEYSYS/
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

5. Prerequisites

Python version (3.10+)
pip
Virtual environment setup


6. Installation and Setup

Clone the repo
Create and activate virtual environment
Install dependencies
Set up .env file
Verify CSV files exist


7. Environment Variables
SECRET_KEY=your_generated_secret_key
ALGORITHM=HS256

How to generate the secret key
What each variable does


8. CSV File Setup

Required files and their location
Headers for each CSV:

Survey_response.csv
Admins.csv
Services.csv


Note that files must exist before running


9. Running the Application
bash# Terminal 1 - Backend
cd backend
uvicorn app:app --reload

# Terminal 2 - Frontend
cd frontend
streamlit run app.py

10. Admin Accounts

How accounts are structured in Admins.csv
How passwords are hashed
Default test credentials
Which admin maps to which service


11. API Reference

Brief summary of all endpoints
Link to API_CONTRACT.md for full details


12. How to Use
Student side:

How to access the survey
How to fill and submit the form
What happens after submission

Admin side:

How to log in
How to navigate the dashboard
How to filter responses
How to view raw responses


13. Validation Rules

Summary of what each field accepts
Rating scale explanation
Date format requirement
Rate limiting behavior


14. Known Limitations

CSV-based storage has no concurrent write protection
Credentials sent on every admin API call
Local deployment only
No admin registration — accounts are premade
Rate limiting resets on server restart


15. Future Improvements

Token-based authentication
Database migration from CSV to SQL
Super admin role
Online deployment
PDF export feature


16. Contributors

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
