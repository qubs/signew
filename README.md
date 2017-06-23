<img src="/display/static/signew-logo.png?raw=true" alt="signew" width="300">

A 'muscular' and lightweight digital signage slideshow software written with
[Django](https://www.djangoproject.com/), originally for use at the
[Queen's University Biological Station](https://qubs.ca).

## Installation

This installation guide is currently only for Linux.

1. If you do not already have it, install [Python 3](https://www.python.org/downloads/).
    * On Ubuntu or similar, required packages can be installed with the following command:
    `sudo apt-get install python3 python-pip3`
2. Download the source code of Signew and place it in a directory that is not directly web-accessible. For example,
the software could be placed in the user's home directory.
3. Open the file `/path/to/signew/settings.py` in a text editor (replace `/path/to` with the path to your installation).
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
This last step will prompt you to create an administrative user with a password. This will be used to sign into the
administrative portion of the site once configuration is complete.
3. Finish up the initial configuration with the following:
    ```
    python manage.py collectstatic --noinput
    ```

## Additional Configuration with [NGINX](https://www.nginx.com/) and [uWSGI](http://uwsgi-docs.readthedocs.io/)

1. Install the Python dev packages with `sudo apt-get install python-dev`.
2. Install uWSGI globally through `pip` with `sudo pip install uwsgi`.
3. Create a directory in `/etc/uwsgi` called `sites`.
    ```shell
    sudo mkdir -p /etc/uwsgi/sites
    cd /etc/uwsgi/sites
    ```
4. Create a configuration file for Signew by typing `sudo nano /etc/uwsgi/sites/signew.ini`.
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
Save and close the file by pressing CTRL-O, enter, then CTRL-X.
6. Create an upstart script for uWSGI by typing `sudo nano /etc/init/uwsgi.conf`.
7. Paste the following content into the file, replacing `user` with your login username:
    ```conf
    description "uWSGI application server in Emperor mode"

    start on runlevel [2345]
    stop on runlevel [!2345]

    setuid user
    setgid www-data

    exec /usr/local/bin/uwsgi --emperor /etc/uwsgi/sites
    ```
8. Install NGINX with the following command:
    ```shell
    sudo apt-get install nginx
    ```
9. Create a server configuration file by typing `sudo nano /etc/nginx/sites-available/your.url.com`, replacing
the example URL with your own. We recommend something like `sign.myorg.com`.
10. Paste in the following content:
    ```nginx
    server {
        listen 80;
        server_name your.url.com www.your.url.com;
        location = /favicon.ico { access_log off; log_not_found off; }

        location / {
            include     uwsgi_params;
            uwsgi_pass  unix:/home/user/firstsite/firstsite.sock;
        }
    }
    ```
Close and save the file like before.
11. Run the following command:
    ```shell
    sudo ln -s /etc/nginx/sites-available/your.url.com /etc/nginx/sites-enabled
    ```
12. Check the NGINX config using the following command:
    ```shell
    sudo service nginx configtest
    ```
13. Restart NGINX and start the uWSGI server:
    ```shell
    sudo service nginx restart
    sudo service uwsgi start
    ```

TODO: Add static and media file stuff, test

## Additional Configuration with [Apache](https://httpd.apache.org/) and mod_wsgi

1. Install Apache and mod_wsgi with `sudo apt-get install apache2 libapache2-mod-wsgi-py3`
2. Edit a virtual host file to set up the site. If you just installed Apache, run the following:
    ```shell
    sudo nano /etc/apache2/sites-available/000-default.conf
    ```
3. Add the following content, replacing `. . .` with existing content, `/path/to` with your installation path,
`python3.5` with the python version you are using, and the path in the Alias and Directory instructions with the path
to the Signew installation:
    ```apache
    <VirtualHost *:80>
        . . .

        Alias /static /path/to/signew/static
        <Directory /path/to/signew/static>
            Require all granted
        </Directory>
        <Directory /path/to/signew/signew>
            <Files wsgi.py>
                Require all granted
            </Files>
        </Directory>

        WSGIDaemonProcess signew python-path=/path/to/signew:/path/to/signew/signewenv/lib/python3.5/site-packages
        WSGIProcessGroup signew
        WSGIScriptAlias / /path/to/signew/signew/wsgi.py
    </VirtualHost>
    ```
4. Save and close the file by pressing CTRL-O, enter, then CTRL-X.
5. Fix permissions on the site by typing the following commands:
    ```shell
    chmod 664 ~/signew/db.sqlite3
    sudo chown :www-data ~/signew/db.sqlite3
    sudo chown :www-data ~/signew
    ```
6. Restart Apache with the following command:
    ```shell
    sudo service apache2 restart
    ```

TODO: Add media file stuff, test, alternate vhost

## Running

To start the Django server, type in the following command (you must be in the application directory):

```shell
python manage.py runserver
```
To access the administrative portion of the website, you can go to something like `http://sign.yoursite.com/admin/`,
depending on where you installed the software.
