# minesweeper-django

Old school game implemented for Deviget test.

Play it at [minesweeper-heroku](https://minesweeper-django-demo.herokuapp.com/).

## Installation

Dillinger requires Python 3 to Run.

Create a virtual environment and run the fallowing commands.

```sh
pip install -r requirements.pip
python manage.py migrate
```

With that you can start a local server.

## Run

To start a development server run

```sh
python manage.py runserver
```

Check you local server at [localhost](http://localhost:8000/).

## Tests

To run the tests with coverage run

```sh
coverage run manage.py test
```

And to see the coverage report

```sh
coverage report -m
```
