crear entorno virtual

python -m venv venv

pip install django
django-admin startproject server .
python manage.py runserver
pip install djangorestframework

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


