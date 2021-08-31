# DOCKER IMAGE
# Official Python 3.9.1 image based on buster Debian
FROM python:3.9.1-slim

# Copy project's source code
RUN mkdir -p /opt/minesweeper-django
COPY . /opt/minesweeper-django/

RUN pip install -r /opt/minesweeper-django/requirements.pip

WORKDIR /opt/minesweeper-django

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
