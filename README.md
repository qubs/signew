<img src="/signew/display/static/signew-logo.png?raw=true" alt="signew" width="300">

A muscular and lightweight digital signage slideshow software written with [Django](https://www.djangoproject.com/).

## Installation

This installation guide is currently only for Linux.

1. If you do not already have it, install [Python 3](https://www.python.org/downloads/).
2. Download the source code of `signew` and place it in a directory that is not directly web-accessible.
3. Change directories to the application directory in a command line shell.
4. Run the following commands in order:

```shell
pip install -r requirements.txt

python manage.py syncdb --noinput
python manage.py migrate
python manage.py collectstatic --noinput
```

## Configuration with [nginx](https://www.nginx.com/)

TODO

## Configuration with [apache2](https://httpd.apache.org/)

TODO

## Running

TODO
