FROM python:3.7-buster

RUN pip install flask

RUN pip install peewee

RUN pip install psycopg2-binary

RUN pip install redis

RUN pip install rq

EXPOSE 5000

COPY * .

ENV FLASK_DEBUG=True \
    FLASK_APP=api8inf349 \
    REDIS_URL=redis://localhost \
    DB_HOST=localhost \
    DB_USER=user \
    DB_PASSWORD=pass \
    DB_PORT=5432 \
    DB_NAME=api8inf349

CMD python /mon_app.py