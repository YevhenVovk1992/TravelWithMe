# Travel With Me - this is a travel service.
### Create your routes if you are professional guide. Or read-made itineraries if you want to relax or challenge yourself.
Link - 
___
screen
___
### What we do?
Technologies used: Djando, Django Unittest, Django crispy forms, DjangoORM, MongoDB, SQLlite, Docker, Jinja2, JavaScripts, HTML5, CSS 
___
### How to start project?
1. pip install -r requerements.txt;
2. Create .env file and write to it enviroment variables:
	- SECRET_KEY
	- MONGO_CONNECTION_STRING ('mongodb://user:password@host:port')
	- MONGO_INITDB_ROOT_USERNAME
	- MONGO_INITDB_ROOT_PASSWORD
3. Run 'docker-compose up -d';
4. Run 'python manage.py migrate';
5. Create superuser 'python manage.py createsuperuser' and add user's groups: guide and traveler in admin panel;

