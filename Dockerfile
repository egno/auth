FROM gitlab.unosalon.ml:4567/containers/flask:latest

COPY . /app

WORKDIR /app

VOLUME ["/app"]

EXPOSE 5000

CMD ["gunicorn", "--reload", "-b", "0.0.0.0:5000", "app:app"]