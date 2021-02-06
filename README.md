# Olympiad-helper
Online judge sytem for helping students to prepare for olympiads in computer science using Django 3 and PostgreSQL database.
To run needed: 
  Linux with python3, g++ 8.3.0 or later
  Linux user judge
  Docker and redis
  docker run -d -p 6379:6379 redis
  python3 -m pip install -r requirements
  from directory with manage.py:
	celery -A config worker -l info
	python3 -m manage runserver
  
