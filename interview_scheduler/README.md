# CSV Uploader API

This project provides an API for scheduling interview easily based on the availability of candidate and interviewer:

1. API for candidates/interviewers to register their available time slots
2. API which will return interview schedulable time slots as a list which will
take candidate id and interviewer id as input.

## Installation

Follow these steps to set up the project locally:
1. Clone project from the github link:


2. Create and activate a virtual environment (if you haven't already):

For macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r req.txt
```
4. Make migrations:

Run the following commands to apply database migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Running the Application

Once you've installed the dependencies and set up your environment, you can start the local development server:
1. Run the development server:
```bash
python manage.py runserver
```

2. Access the API:
The API will be available at http://127.0.0.1:8000/.
You can also access the Django admin interface at http://127.0.0.1:8000/admin/ if you created a superuser.

API documentation is here: https://documenter.getpostman.com/view/39560800/2sAYX8KMU3
