import os
import ast

from flask import Flask, request
import redis

from sentry_sdk.integrations.flask import FlaskIntegration
import sentry_sdk

# Configure Redis
redis_host = os.environ.get('REDIS_HOST', 'localhost')
redis_port = os.environ.get('REDIS_PORT', 6379)
redis_db = redis.StrictRedis(host=redis_host, 
    port=redis_port, db=0, charset="utf-8", decode_responses=True)

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