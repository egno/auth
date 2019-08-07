FROM python:3.7-alpine

COPY . /app

WORKDIR /app

VOLUME ["/app"]

EXPOSE 5000

CMD ["gunicorn", "--reload", "-b", "0.0.0.0:5000", "app:app"]