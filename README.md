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
- [x] Логин (вход в систему)
- [x] Регистрация нового пользователя
- [ ] Создание нового желания
- [x] Просмотр желаний пользователем
- [ ] Регистрация нового "gifted" пользователя
    1. Добавить всех gifted пользователей.
    2. Добавить их модели в админскую панель.
- [ ] Просмотр списка желаний в очереди
    * Частично: пока не все пользователи добавлены
- [ ] Выполнение желания
- [x] Просмотр заказчиком желания
- [ ] Отмена желания
- [ ] Оплата желания
- [ ] Редактирование профиля пользователя
- [x] Деавторизация пользователя (выход из системы)
- [ ] Реактивация желания
- [ ] Закрытие желания
- [ ] Обработка желания
