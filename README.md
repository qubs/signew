<img src="/signew/display/static/signew-logo.png?raw=true" alt="signew" width="300">

A 'muscular' and lightweight digital signage slideshow software written with
[Django](https://www.djangoproject.com/), originally for use at the
[Queen's University Biological Station](https://qubs.ca).

## Installation

This installation guide is currently only for Linux.

1. If you do not already have it, install [Python 3](https://www.python.org/downloads/).
    * On Ubuntu or similar, required packages can be installed with the following command:
    `sudo apt-get install python3 python-pip3`
2. Download the source code of `signew` and place it in a directory that is not directly web-accessible.
3. Open the file `/signew/settings.py` in a text editor.
4. Add your own secret key, and make sure debug mode is set to `False` (capitalization is important here).

## Initial Configuration

1. Change directories to the application directory in a command line shell.
2. Run the following commands in order:
    ```shell
    pip install -r requirements.txt

    python manage.py syncdb --noinput
    python manage.py migrate
    python manage.py createsuperuser
    ```
This last step will prompt you to create an administrative user with a password. THis will be used to sign into the
administrative portion of the site once configuration is complete.
3. Finish up the initial configuration with the following:
    ```
    python manage.py collectstatic --noinput
    ```

## Additional Configuration with [nginx](https://www.nginx.com/) and [uWSGI](http://uwsgi-docs.readthedocs.io/)

1. Install the Python dev packages with `sudo apt-get install python-dev`.
2. Install uWSGI globally through `pip` with `sudo pip install uwsgi`.
3. Create a directory in `/etc/uwsgi` called `sites`.
    ```shell
    sudo mkdir -p /etc/uwsgi/sites
    cd /etc/uwsgi/sites
    ```
4. Create a configuration file for Signew by typing `sudo nano signew.ini`.
5. Paste the following content into the file:
    ```ini
    [uwsgi]
    project = signew
    base = /path/to/signew/parent/folder

    chdir = %(base)/%(project)
    home = %(base)/venv/%(project)

    master = true
    processes = 5

    socket = %(base)/%(project)/%(project).sock
    chmod-socket = 644
    vacuum = true
    ```

TODO

## Additional Configuration with [Apache](https://httpd.apache.org/) and mod_wsgi

1. Install Apache and mod_wsgi with `sudo apt-get install apache2 libapache2-mod-wsgi-py3`
2. Edit a virtual host file to set up the site. If you just installed Apache, run the following:
```bash
sudo nano /etc/apache2/sites-available/000-default.conf
```

TODO

## Running

To start the Django server, type in the following command (you must be in the application directory):

```shell
python manage.py runserver
```
To access the administrative portion of the website, you can go to something like `http://yoursite.com/admin/`,
depending on where you installed the software.
