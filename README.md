## METHODOLOGY OF SOFTWARE ENGINEERING (mose)

Проект по предмету "Методология программной инженерии"

## Installation
Dependencies:
* docker
* docker-compose

To run project execute following commands:
```bash
cd <project-dir>/docker
docker-compose up --build  # add -d flag to run in detached mode
docker-compose run --rm web ./manage.py migrate
# optional: populate database with initial data
docker-compose run --rm web ./manage.py populate_db
```

Now you can access these endpoints:
* http://127.0.0.1:8000/wizuber
* http://127.0.0.1:8000/admin
