# Ushahidi Platform API USSD Service

[Demo](https://ushahidi-ussd.herokuapp.com/)

## Features
- Fetches list of all Forms(Surveys on a Ushahi Platform) with PLATFORM_URL 
- Provides Payload URL for USSD Provider Webhook setup at */ussd/*
- Manages the USSD Interaction *service* and *interactivity*

## How to Use

- Configure enviroment variables as follows:
```bash
DATABASE_URL=postgres://postgres:password@localhost:5432/ussd
PLATFORM_URL=https://ussd.ushahidi.io
PLATFORM_EMAIL=admin@ushahidi.com
PLATFORM_PASSWORD=*************
```
- Install dependencies using: `pipenv install`
- Migrate DB using: `python manage.py migrate`
- Runserver using: `python manage.py runserver`

## Technologies
- Python 3.X
- Django 2.1
- PostgreSQL
- [Requests](https://2.python-requests.org/en/master/)
