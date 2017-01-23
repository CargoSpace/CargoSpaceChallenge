## Run code as follows
python3 manage.py runserver $IP:$PORT

<!---
### Start new App as follows
django-admin startapp dashboard

#Migrate Model Changes
python3 manage.py makemigrations

### Install new module by adding an entry in requirements.txt then
sudo pip3 install -r requirements.txt

### The template used in this project can be found here.
http://flatfull.com/themes/aside/index.html

## Celery
celery -A csc worker -l info

## Start the celery beat service using the django scheduler:
celery -A csc beat -l info -S django
celery -A csc beat
celery -A csc worker -B

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
--->
