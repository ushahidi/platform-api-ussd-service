import os
import ast

from flask import Flask, request

from sentry_sdk.integrations.flask import FlaskIntegration
import sentry_sdk

# Sentry Integration
SENTRY_DSN = str(os.environ.get('DSN_CODE', ''))

sentry_sdk.init(
    dsn=SENTRY_DSN,
    integrations=[FlaskIntegration()]
)

# Get Ushahidi Deployment
USHAHIDI_DEPLOYMENT = os.environ.get('PLATFORM_API', '').replace('.api', '')
deployment_title = USHAHIDI_DEPLOYMENT.replace(
    'https://', '').replace('.ushahidi.io', '')


# Initialize Flask App
app = Flask(__name__)