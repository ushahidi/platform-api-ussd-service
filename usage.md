---
description: Ushahidi Platform USSD Service Usage.
---

# Usage

## Deployment

Build the Docker 

```text
docker build -t ussd_service .
```

Deploy to any container environment. Examples are:

* [AWS Fargate](https://aws.amazon.com/fargate/)
* [Google Cloud Run](https://cloud.google.com/run/)

You would also need to deploy Redis server or use a managed one.

## Configure Environment Variables

You are required to the following environment variables.

```bash
PLATFORM_API=https://ussd.api.ushahidi.io # Ushahidi deployment API URL
PLATFORM_EMAIL=admin@account.com # Ushahidi Admin Account Email
PLATFORM_PASSWORD=************* # Ushahidi Admin Account Password
REDIS_HOST=localhost # Redis Server Host
REDIS_PORT=6379 # Redis Server Port
DSN_CODE=https://***** # https://sentry.io Flask Integration Code (Optional)
```

