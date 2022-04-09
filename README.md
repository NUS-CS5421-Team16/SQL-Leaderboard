# SQL-Leaderboard

## Setup Developing Environment

### Backend
1. Install `python3.9`.

2. Run your favourite python environment management tool to create an env based on `requirements.txt`. `cd` to `/backend`
   ```
   # venv
   python3 -m venv env_lb
   source ./env_lb/bin/activate
   pip install -r requirements.txt
   
   # pipenv
   pipenv --python 3.9
   pipenv shell
   pip install -r requirements.txt
   ```
   
3. Configure your database in `/backend/backend/settings.py`, remember to create databases(`Leaderboard`,`PrivateDataset`,`PublicDataset`) in postgresql in advance.
   ```python
   # /backend/backend/settings.py
   ...
   PRIVATE_DATABASE = "private"
   PUBLIC_DATABASE = "public"
   
   DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'Leaderboard',
        'USER': 'youruser',
        'PASSWORD': 'yourpassword',
        'HOST': 'localhost',
        'PORT': '5432',
    },
    PRIVATE_DATABASE: {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'PrivateDataset',
        'USER': 'youruser',
        'PASSWORD': 'yourpassword',
        'HOST': 'localhost',
        'PORT': '5432',
    },
    PUBLIC_DATABASE: {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'PublicDataset',
        'USER': 'youruser',
        'PASSWORD': 'yourpassword',
        'HOST': 'localhost',
        'PORT': '5432',
    },
    }
   ...
   ```
   
4. Run migrate if necessary.

   ```shell
   python manage.py migrate
   ```

5. Celery prerequisite: install&run redis service and configure redis url in celery.py
   ```
   # /backend/backend/celery.py
   ...
   app.conf.broker_url = 'redis://localhost:6379/0'
   ...
   ```

6. Start celery before starting the server. Celery beat and celery worker should run in 2 terminals.

   ```
   # run worker first
   celery -A backend worker -l info -P solo
   
   # after the worker is ready(the following output is shown)
   # [2022-XX-XX 22:18:22,525: INFO/MainProcess] celery@User ready.
   # run beat
   celery -A backend beat -l info
   ```

7. Start your server.

   ```shell
   python manage.py runserver 0.0.0.0:8000
   ```
   
### Frontend

To combine frontend and backend and run them together, there are some additional steps:

1. Install `npm` and `node`.
2. `cd frontend`.
3. Run `npm install`
4. Run build: `npm run build`. Then you will see `static/` in `backend/template`.
5. If you get an error in step 4 because `vue-cli-service: command not found`, try `npm ci && npm run build`.
6. Then start django as described above.