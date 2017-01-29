## Run code as follows
```bash
python manage.py runserver $IP:$PORT
``` 
This project uses Socket.IO provided by Django Channels, therefore WSGI is not supported. ASGI is supported

## Celery (Optional Worker but needed if you are handling large problem submissions)
```bash
sudo service redis-server start
celery -A csc worker -l debug
``` 

## Sheduler (Doesn't work without a Worker "Celery". Needed If you need a Periodic Programming Contest)
```bash
celery -A csc beat -l debug -S django --max-interval 1
```

## Pupulate with data
```bash
python manage.py loaddata --app=contest Contest_Settings Django_Celery_Beat
python manage.py loaddata --app=acm  Schools
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

The fixtures Generated
python manage.py dumpdata --indent=4 django_celery_beat > contest/fixtures/Django_Celery_Beat.json
python manage.py dumpdata --indent=4 contest.contestsetting > contest/fixtures/Contest_Settings.json
python manage.py dumpdata --indent=4 acm.school > acm/fixtures/Schools.json
--->
