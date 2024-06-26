### Backend Setup

Setup an virtual environment

`python -m venv venv`

After creating it, activate it:

`venv/Scripts/Activate` (on Windows)

Then, install all required dependencies from reqs.txt

`pip install -r reqs.txt`

You will also need an .env file that describes path to your PostgreSQL database and your Password Encryption parameters

Create it with following data:

```
LOGIN = 'login'
PASSWORD = 'password'
URL = 'localhost:5432'
DATABASE_NAME = 'database_name'
AUTH_ENCRYPTION_KEY = 'your-key'
AUTH_ENCRYPTION_METHOD = 'HS256'
```

After that, everything should be set up. Start the backend using this command:

`uvicorn main:app --reload`
