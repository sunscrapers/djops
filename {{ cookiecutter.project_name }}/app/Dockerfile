FROM python:3.6.5

RUN apt-get update && apt-get install -y ca-certificates netcat-openbsd postgresql-client-9.6

WORKDIR /app

RUN pip install --upgrade pip
COPY requirements/ /app/requirements
RUN pip install -r requirements/dev.txt

COPY . /app

EXPOSE 8000
CMD ["sh", "entrypoints/runserver.sh"]
