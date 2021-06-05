FROM python:3.8.2

    ENV PYTHONBUFFERED 1
    ENV PYTHONWRITEBYTECODE 1

    RUN apt-get update \
        && apt-get install -y netcat

    ENV APP=/app

    # Change the workdir.
    WORKDIR $APP

    # Install the requirements
    COPY requirements.txt $APP
    RUN pip install --upgrade pip
    RUN pip install -r requirements.txt

    # Copy the rest of the files
    COPY . $APP

    EXPOSE 8000

    RUN chmod +x /app/entrypoint.sh
    ENTRYPOINT ["/app/entrypoint.sh"]

    CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "djangobackend.wsgi"]
    #!/bin/sh

    if [ "$DATABASE" = "postgres" ]; then
        echo "Waiting for postgres..."

        while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
        sleep 0.1
        done

        echo "PostgreSQL started"
    fi

    # Make migrations and migrate the database.
    echo "Making migrations and migrating the database. "
    python manage.py makemigrations main --noinput 
    python manage.py migrate --noinput 
    exec "$@"