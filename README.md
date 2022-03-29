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
   # [2022-03-28 22:18:22,525: INFO/MainProcess] celery@vincent ready.
   # run beat
   celery -A backend beat -l info
   ```

7. Start your server.

   ```shell
   python manage.py runserver 0.0.0.0:8000
   ```

## Reference Website (Internal Review)

[Django Docs](https://docs.djangoproject.com/en/4.0/intro/)

[Django QuerySet](https://docs.djangoproject.com/en/4.0/ref/models/querysets/#select-for-update)

[Django with Postgresql](https://stackoverflow.com/questions/5394331/how-to-set-up-a-postgresql-database-in-django)

[VUE + Django](https://blog.logrocket.com/how-to-build-vue-js-app-django-rest-framework/)

## Reference Structure (Internal Review)

```bash
.
├── env_lb/    # Python Virtual Environment
├── frontend/  # Frontend - vue
│   ├── build/
│   ├── server/
│   ├── src/  
│   │   ├── App.vue
│   │   ├── components/  
│   │   ├── favicon.ico
│   │   ├── index.html  
│   │   ├── main.js
│   │   ├── pages/
│   ├── static/
│   ├── theme/
│   └── twistd.pid
├── __init__.py
├── backend/  # Backend - Django
│   ├── core  # Django（app）
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── build.py
│   │   ├── config.py
│   │   ├── encoder.py
│   │   ├── __init__.py
│   │   ├── middlewares.py
│   │   ├── migrations/
│   │   ├── models.py
│   │   ├── parser.py
│   │   ├── response.py
│   │   ├── scheduler.py
│   │   ├── templates  # fontend template from vue
│   │   │   ├── favicon.ico
│   │   │   ├── index.html
│   │   │   └── static
│   │   │       ├── css
│   │   │       ├── fonts
│   │   │       ├── images
│   │   │       └── js
│   │   ├── tests.py
│   │   ├── time.py
│   │   ├── urls.py
│   │   ├── utils.py
│   │   └── views.py
│   ├── __init__.py
│   ├── manage.py
│   └── backend
│       ├── __init__.py
│       ├── settings.py
│       ├── urls.py
│       └── wsgi.py
├── templates/  
└── README.md
```
