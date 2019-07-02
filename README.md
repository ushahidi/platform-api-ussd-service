# Ushahidi Platform API USSD Service

[Demo](https://ushahidi-ussd.herokuapp.com/)

## Features
- Fetches list of all Forms(Surveys on a Ushahi Platform) with PLATFORM_URL and Admin Credentials
- Provides Payload URL for USSD Provider e.g. Africa's Talking Webhook setup at *<service-url>/ussd/*
- Manages the USSD Interaction *service* and *interactivity* with Ushahidi Deployment

## How to Use

- Configure enviroment variables as follows:
```bash
PLATFORM_API=https://ussd.api.ushahidi.io #Ensure it is <deployment-url>.api.ushahidi.io
PLATFORM_EMAIL=admin@ushahidi.com
PLATFORM_PASSWORD=*************
```
- Install dependencies using: `pip install -r requirements.txt`
- Runserver using: `python app.py`

## Technologies
- Python 3.X
- Flask
- [Requests](https://2.python-requests.org/en/master/)
