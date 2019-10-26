FROM python:3.6.8-stretch

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE mose.settings

WORKDIR /code

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /code/

CMD ["python3.6", "manage.py", "runserver", "0.0.0.0:8000"]
