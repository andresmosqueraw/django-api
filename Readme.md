crear entorno virtual

python -m venv venv
source venv/bin/activate

pip install django
pip install djangorestframework
django-admin startproject server .
python manage.py migrate
python manage.py runserver 0.0.0.0:8081
nohup python manage.py runserver 0.0.0.0:8081 &

agregar:

'rest_framework',
'rest_framework.authtoken',

en installed apps de settings.py del server

crear views.py
editar urls.py

python manage.py makemigrations
python manage.py migrate

crear serializerpython manage.py showmigrations

python manage.py makemigrations server




Si solo cambio codigo python: docker compose restart web
