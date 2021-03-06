## METHODOLOGY OF SOFTWARE ENGINEERING (mose)

[![pipeline status](https://gitlab.com/artslob/mose/badges/master/pipeline.svg)](https://gitlab.com/artslob/mose/commits/master)
[![Coverage Status](https://coveralls.io/repos/gitlab/artslob/mose/badge.svg?branch=HEAD)](https://coveralls.io/gitlab/artslob/mose?branch=HEAD)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Проект по предмету "Методология программной инженерии", Университет ИТМО,
2-3 семестр магистратуры, 2019 год.

Преподавательский состав:
* Клименков Сергей Викторович
* Цопа Евгений Алексеевич
* Исаев Илья Владимирович

Бригада 19:
* Слободкин Артем Юрьевич
* Корзухин Сергей Владиславович
* Осадчая Алиса Олеговна

## Описание проекта
В мире, описанном в серии книг "Трилогия Бартимеуса" писателя Джонатана Страуда, отсутствует
удобный способ коммуникации между волшебником и людьми, которые хотели бы купить у него магическую
услугу. Клиенты вынуждены лично обращаться за помощью к волшебнику, что в свою очередь ограничивает
количество заявок, которые может обработать волшебник.  
Проект представляет новый подход к организации выполнения магических услуг. Данная система будет
решать административные задачи по обработке заявок, их хранению и обработке, а также повысит качество
обслуживания клиентов волшебника, что позволит повысить прибыль, а у клиентов появится удобный способ
оставлять заявки. Система будет хранить файлы окружения (информация о заклинаниях, благовониях и
пентаклях), и обеспечивать интерфейс для демонов и администраторов.  
Проект позволит открыть новое направление бизнеса для волшебников, сделать сферу оказания магических
услуг более понятной и доступной. На рынке появятся новые игроки - агрегаторы, которые будут
способствовать развитию данного направления бизнеса.

## Installation
Dependencies:
* docker
* docker-compose

To run project execute following commands:
```bash
cd <project-dir>/docker
# build images and run in detached mode
docker-compose up --build -d
# run django migrations and (optional step) populate database with initial data
docker-compose exec web bash -c "./manage.py migrate && ./manage.py populate_db"
```

Now you can access these endpoints:
* http://127.0.0.1:8000/wizuber
* http://127.0.0.1:8000/admin

## Use cases
- [x] 1\. Логин (вход в систему)
- [x] 2\. Регистрация нового пользователя
- [x] 3\. Создание нового желания
- [x] 4\. Просмотр желаний пользователем
- [x] 5\. Регистрация нового "gifted" пользователя
    1. Добавлены модели `Wizard`, `Student`, `Spirit`.
    2. В админской панели можно создавать и редактировать данные модели.
- [x] 6\. Просмотр списка желаний в очереди
    1. Customer: 
        * wishes created by him;
        * wishes created by him and closed;
    2. Wizard:
        * wishes owned by him;
        * wishes in active status and without owner;
    3. Student: wishes assigned to him;
    4. Spirit: wishes assigned to him;
- [x] 7\. Выполнение желания
    1. Описать state машину - как могут изменять состояние желания разные
    типы пользователей на всём его жизненном цикле.
    2. Реализовать смену состояний.
- [x] 8\. Просмотр заказчиком желания
- [x] 9\. Отмена желания
- [x] 10\. Оплата желания
- [x] 11\. Деавторизация пользователя (выход из системы)
- [x] 12\. Закрытие желания
- [x] 13\. Обработка желания

## Testing
Start database and install requirements for python >= 3.6:
```bash
docker-compose -f docker/docker-compose.yml up --build -d db
python3 -m pip install -r requirements.txt -r requirements-tests.txt
```
Run **unit** tests with coverage report:
```bash
coverage run manage.py test --exclude-tag=selenium && coverage report
```
Run **functional** tests with selenium (`firefox` and `geckodriver` in `$PATH` are required):
```bash
python3 manage.py test --tag=selenium
```
Run **load** tests on _populated_ database (go to http://127.0.0.1:8089/ after `locust` launch):
```bash
docker-compose -f docker/docker-compose.yml run --rm web bash -c "./manage.py migrate && ./manage.py populate_db"
python3 manage.py runserver 8000
locust -f wizuber/tests/load_testing.py --host="http://127.0.0.1:8000"
```

## Deployment
Generate ssh keys and copy to server to allow access from CI to deployment server:
```bash
mkdir "${HOME}/mose-deploy/"
ssh-keygen -t rsa -b 4096 -C "key for deployment" -f "${HOME}/mose-deploy/id_rsa"
ssh-copy-id -i "${HOME}/mose-deploy/id_rsa.pub" user@target
```
Now you can use gitlab interface to deploy code or run deploy with local `gitlab-runner`:
```bash
gitlab-runner exec docker deploy-to-helios \
    --env MOSE_DEPLOY_SSH_PRIVATE_KEY="$(cat $HOME/mose-deploy/id_rsa)" \
    --env MOSE_DEPLOY_HELIOS_PORT="..." \
    --env MOSE_DEPLOY_HELIOS_IP="..."
```
To start server run commands below on `helios`
(university server under 32-bit `Solaris 10` aka `SunOS 5.10`):
```bash
source "source-me.sh"
python mose/manage.py migrate
python mose/manage.py populate_db
python mose/manage.py runserver 55671
```
Create [ssh-tunnel](https://unix.stackexchange.com/a/115906/309121) on local machine
and then go to http://localhost:8001/wizuber/:
```bash
ssh -L 8001:localhost:55671 helios
```

## Links to docs:
1. [django-polymorphic](https://django-polymorphic.readthedocs.io)
2. [locust.io](https://docs.locust.io/)

## Useful links:
1. [How to add permission to user on his creation](https://stackoverflow.com/questions/31334332/giving-default-permissions-or-a-default-group-to-new-users).
2. [Right way to query for Permission objects](https://stackoverflow.com/questions/46560651/django-why-is-a-permissions-code-name-different-from-checking-if-it-has-a-permis).
3. [How to create groups and assign permission during project setup](https://stackoverflow.com/questions/42743825/how-to-create-groups-and-assign-permission-during-project-setup-in-django).
4. [How to create custom permissions without binding to specific model](https://stackoverflow.com/questions/13932774).
5. [Using Django auth UserAdmin for a custom user model](https://stackoverflow.com/questions/15012235/using-django-auth-useradmin-for-a-custom-user-model).
6. [Run Firefox Headless Browser tests on GitLab CI](https://grauwoelfchen.at/posts/run-firefox-headless-browser-tests-on-gitlab-ci/)
6. [How to Install PostgreSQL 10 Using Source Code in Linux](https://www.tecmint.com/install-postgresql-from-source-code-in-linux/)
7. [Error while loading shared libraries: libpq.so.5](https://stackoverflow.com/a/12781602)
8. [Psycopg runtime requirements](http://initd.org/psycopg/docs/install.html#runtime-requirements)

## Conventions
`Model` is name of a model as singular, e.g. `Wish` or `Wizard`.

| Permission Name | Action | View Name   | Template Name     | Url Name     |
| --------------- | ------ | ----------- | ----------------- | ------------ |
|                 | List   | ListModel   | model/list.html   | list-model   |
| Add             | Create | CreateModel | model/create.html | create-model |
| View            | Detail | DetailModel | model/detail.html | detail-model |
| Change          | Update | UpdateModel | model/update.html | update-model |
| Delete          | Delete | DeleteModel | model/delete.html | delete-model |
