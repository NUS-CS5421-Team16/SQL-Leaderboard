# SQL-Leaderboard

## Setup

In the project root path, run ``python3 -m venv env_lb``.

Then, run ``source ./env_lb/bin/activate``.

Then, install Django ``pip install django`` and VUE ``npm install --global vue-cli``.

To support Postgresql, intall Psycopg2 ``pip install psycopg2``.

Update the ``DATABASES`` in ``backend/backend/settings.py``.

Run ``python manage.py makemigrations``. Then run ``python manage.py migrate``.

Run ``python manage.py runserver``.

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
