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
6. Save and close the file by pressing CTRL-O, enter, then CTRL-X.
7. Create an upstart script for uWSGI by typing `sudo nano /etc/init/uwsgi.conf`.
8. Paste the following content into the file, replacing `user` with your login username:
    ```conf
    description "uWSGI application server in Emperor mode"

    start on runlevel [2345]
    stop on runlevel [!2345]

    setuid user
    setgid www-data

    exec /usr/local/bin/uwsgi --emperor /etc/uwsgi/sites
    ```
9. Install Nginx with the following command:
    ```shell
    sudo apt-get install nginx
    ```
10. Create a server configuration file by typing `sudo nano /etc/nginx/sites-available/your.url.com`, replacing
the example URL with your own. We recommend something like `sign.myorg.com`.
11. Paste in the following content:
    ```
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
12. Close and save the file like before.
13. Run the following command:
    ```shell
    sudo ln -s /etc/nginx/sites-available/your.url.com /etc/nginx/sites-enabled
    ```
14. Check the Nginx config using the following command:
    ```shell
    sudo service nginx configtest
    ```
15. Restart Nginx and start the uWSGI server:
    ```shell
    sudo service nginx restart
    sudo service uwsgi start
    ```
TODO: Add static and media file stuff, test

## Additional Configuration with [Apache](https://httpd.apache.org/) and mod_wsgi

1. Install Apache and mod_wsgi with `sudo apt-get install apache2 libapache2-mod-wsgi-py3`
2. Edit a virtual host file to set up the site. If you just installed Apache, run the following:
    ```bash
    sudo nano /etc/apache2/sites-available/000-default.conf
    ```
3. Add the following content, replacing `. . .` with existing content, `user` with your username, `python3.5` with the
python version you are using, and the path in the Alias and Directory instructions with the path to the
`signew` installation:
    ```
        <VirtualHost *:80>
            . . .

            Alias /static /home/user/signew/static
            <Directory /home/user/signew/static>
                Require all granted
            </Directory>
            <Directory /home/user/signew/signew>
                <Files wsgi.py>
                    Require all granted
                </Files>
            </Directory>

            WSGIDaemonProcess signew python-path=/home/user/signew:/home/user/signew/signewenv/lib/python3.5/site-packages
            WSGIProcessGroup signew
            WSGIScriptAlias / /home/user/signew/signew/wsgi.py
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
TODO: Add media file stuff, test

## Running

To start the Django server, type in the following command (you must be in the application directory):

```shell
python manage.py runserver
```
To access the administrative portion of the website, you can go to something like `http://yoursite.com/admin/`,
depending on where you installed the software.
