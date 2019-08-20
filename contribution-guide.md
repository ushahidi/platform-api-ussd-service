---
description: Ushahidi Platform USSD Service Contribution Guide.
---

# Contribution Guide

## Source Codes

Clone from GitHub

```text
git clone https://github.com/ushahidi/platform-api-ussd-service
```

Change directory into source code

```text
cd platform-api-ussd-service
```

Checkout to new branch e.g. feat/new-feature

```text
git checkout -b feat/new-feature
```

## Setup Local Development

* Create [Python Virtual Environment](https://docs.python.org/3/tutorial/venv.html)
* [Install Redis](https://redis.io/topics/quickstart) \(Optional if using hosted Redis\)
* [Configure environment variables](https://docs.ushahidi.com/platform-api-ussd-service/usage#configure-environment-variables)
* Install dependencies using: `pip install -r requirements.txt`
* Run server using: `python app.py`
* [Expose **localhost** using **Ngrok**](https://ngrok.com/) \(for use by USSD Provider\)

## Report or Feature Request

To report an issue or request for a feature, kindly create an issue with useful tags [here](https://github.com/ushahidi/platform-api-ussd-service/issues)

