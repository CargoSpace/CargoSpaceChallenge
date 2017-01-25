## Run code as follows
```bash
python3 manage.py runserver $IP:$PORT
``` 
This project uses Socket.IO provided by Django Channels, therefore WSGI is not supported. ASGI is supported

## Celery (Optional Worker)
```bash
sudo service redis-server start
celery -A csc worker -l info
``` 

<!---
### Start new App as follows
django-admin startapp dashboard

#Migrate Model Changes
python3 manage.py makemigrations

### Install new module by adding an entry in requirements.txt then
sudo pip3 install -r requirements.txt

### The template used in this project can be found here.
http://flatfull.com/themes/aside/index.html

## Celery **
celery -A csc worker -l info


## Start the celery beat service using the django scheduler:
celery -A csc beat -l info -S django
celery -A csc beat
celery -A csc worker -B (my guess is with beat in one process)

## Install RabbitMQ
http://www.rabbitmq.com/install-debian.html
### Setup RabbitMQ
NB: reuse your system hostname
sudo rabbitmqctl status
daemonizing: sudo rabbitmq-server -detached
stopping, not killing: sudo rabbitmqctl stop
http://docs.celeryproject.org/en/latest/getting-started/brokers/rabbitmq.html?highlight=rabbit

## Setting up virtual env for python3
Install Python 3 and virtualenv apt-get install -y python3 python-virtualenv
Create a Python 3 virtualenv: virtualenv -p $(which python3) testDir
source testDir/bin/activate

We are using celery and redis since our move to django channels 

sudo service redis-server start
settings all reconfigured to use redis instead of rabbitMQ

These articles were useful in setting up channels
https://blog.heroku.com/in_deep_with_django_channels_the_future_of_real_time_apps_in_django
https://www.sourcelair.com/blog/articles/115/django-channels-chat
--->
