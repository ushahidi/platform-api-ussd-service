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
- Install dependencies using: `pip install -r requirements.txt`
- Runserver using: `python app.py`

## Technologies
- Python 3.X
- Flask
- MySQL
- [Requests](https://2.python-requests.org/en/master/)
