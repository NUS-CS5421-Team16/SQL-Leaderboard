# SQL-Leaderboard

## Reference Structure
```bash
.
├── client/  # Frontend - vue
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
├── server/  # Django
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
│   └── server
│       ├── __init__.py
│       ├── settings.py
│       ├── urls.py
│       └── wsgi.py
├── spiders/
├── templates/  
└── VERSION
```
