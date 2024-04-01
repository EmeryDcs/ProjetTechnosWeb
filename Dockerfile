FROM python:3.7-buster

RUN pip install flask

RUN pip install peewee

RUN pip install psycopg2-binary

RUN pip install redis

EXPOSE 5000

COPY * .

CMD python /mon_app.py