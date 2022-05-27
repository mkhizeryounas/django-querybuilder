FROM python:3.8

RUN apt-get -y update \
  && apt-get clean

COPY requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py makemigrations && python manage.py migrate

CMD python manage.py runserver


