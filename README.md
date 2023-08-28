# e-ballot
A simulated application intended to undertake the process of balloting when medical students are applying for their preferred internship centers.

# Intro
This is a backend API service built with FastAPI web framework handling server-side logic including database CRUD operations.

# Project Navigation
- # Regular user:
  - ## User sign-up and login:
      - Sign-up: Both regular and admin users sign up with their email and password credentials.
      - Logi-in: On login, every user is granted a unique access token that authorizes them to perform specific actions.
  - ## User choosing hospital preferences:
    - Each user queries the db for all or specific hospital and then updates their choices according to established rules.
- # Admin user:
  - ## Hospital Management:
    - Responsible for adding, removing and updating the number of slots each hospital has.
  - ## Hospital Allocation:
    - After all users have registered, the admin runs all the necessary logic to perform the allocation.
  - ## Generate final list:
    - Generates a final list that shows each user and their allocated hospital. Runs after every successful allocation in the previous step.

  This logic flow can be visualized in the [admin.py file](app/routers/admin.py). It runs in three phases as seen in the [magic_maker function](app/routers/admin.py)

  > [!IMPORTANT]
  > [Postman](https://www.postman.com/) was used to simulate the client-side requests to this API so you can download it as well.

# Project Set-up
 - **Install Python 3.10:** You can download it from the official Python website: https://www.python.org/downloads/
 - ***OPTIONAL:*** Create a virtual environment by running `python -m venv venv` the activate it by navigating to `venv\Scripts\activate`
 - **Upgrade pip:** run `python -m pip install --upgrade pip`
 - **Install all required dependencies:** run `pip install -r requirements.txt`
 - **Set-up database:** Update the sample_env file with your credentials and update the env_file variable in [config.py file](app/config.py) to point to sample_env file
 - **Apply alembic migrations to new db:** run `alembic upgrade head`. If there are no revisions, create one by running `alembic revision --autogenerate -m "Creae all db tables."`
 - **Initiate uvicorn server:** run `uvicorn app.main:app --reload`
 <!-- - **From Postman app:** Simuate a request to `http://127.0.0.1:8000/admin/` to run the admin logic -->
- **To run function tests:** Install pytest by running `pip install pytest`, then run `pytest -v -s`. If you get any import errors, run `export PYTHONPATH="${PYTHONPATH}:/path/to/your/project/"` substituting the path to your project
# Tech Stack
* Languages: Python
* DB: Postgresql
* Frameworks: FastAPI, Pydantic, SQLAlchemy, Alembic, Pytest

# Contact Info
* email: [limzyon@gmail.com](mailto:limzyon@gmail.com)
* phone: +254729458728
