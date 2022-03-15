# SQL-Leaderboard

## Setup

In the root path, run ``python3 -m venv env_lb``.

Then, run ``source ./env_lb/bin/activate``.

Then, install Django ``pip install django`` and VUE ``npm install --global vue-cli``.

## Reference Structure

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
