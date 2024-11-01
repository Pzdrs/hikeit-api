FROM python:3.11-alpine

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5000

CMD [ "gunicorn", "app:app", "--bind=0.0.0.0:5000"]