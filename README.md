# Olympiad-helper
Online judge sytem for helping students to prepare for olympiads in computer science using Django 3 and PostgreSQL database.
# To run

1)  Linux with:
    
    - python3 (tested with 3.9.0), 
    
    -g++ 8.3.0 or later, 
    
    - go (tested with 1.16.4)

2) Linux user judge

3) Redis on port 6379

4)  python3 -m pip install -r requirements

# from directory with manage.py
    
1) celery -A config worker -l info

2) python3 -m manage runserver (on localhost)
