FROM python:3.14-slim

WORKDIR /app

COPY app ./app

ENV APP_NAME=opshub
ENV APP_ENV=container
ENV APP_PORT=8000
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["python3", "-m", "app.app"]
