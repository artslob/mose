## METHODOLOGY OF SOFTWARE ENGINEERING (mose)

Проект по предмету "Методология программной инженерии".

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
- [ ] 5\. Регистрация нового "gifted" пользователя
    1. Добавить всех gifted пользователей.
    2. Добавить их модели в админскую панель.
- [ ] 6\. Просмотр списка желаний в очереди
    * Частично: пока не все пользователи добавлены
- [ ] 7\. Выполнение желания
    1. Описать state машину - как могут изменять состояние желания разные
    типы пользователей на всём его жизненном цикле.
    2. Реализовать смену состояний.
- [x] 8\. Просмотр заказчиком желания
- [ ] 9\. Отмена желания
- [ ] 10\. Оплата желания
- [ ] 11\. Редактирование профиля пользователя
- [x] 12\. Деавторизация пользователя (выход из системы)
- [ ] 13\. Реактивация желания
- [ ] 14\. Закрытие желания
- [ ] 15\. Обработка желания

## Useful links:
1. [How to add permission to user on his creation](https://stackoverflow.com/questions/31334332/giving-default-permissions-or-a-default-group-to-new-users).
2. [Right way to query for Permission objects](https://stackoverflow.com/questions/46560651/django-why-is-a-permissions-code-name-different-from-checking-if-it-has-a-permis).
3. [How to create groups and assign permission during project setup](https://stackoverflow.com/questions/42743825/how-to-create-groups-and-assign-permission-during-project-setup-in-django).
4. [How to create custom permissions without binding to specific model](https://stackoverflow.com/questions/13932774).
5. [Using Django auth UserAdmin for a custom user model](https://stackoverflow.com/questions/15012235/using-django-auth-useradmin-for-a-custom-user-model).
