## Run code as follows
python3 manage.py runserver $IP:$PORT

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