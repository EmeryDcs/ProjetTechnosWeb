FROM python:3.7-buster

RUN pip install flask

RUN pip install peewee

EXPOSE 5000

COPY * .

CMD python /mon_app.py