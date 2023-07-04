import os

import firebase_admin
from dotenv import load_dotenv
from twilio.rest import Client

# ---------- CONFIG VARIABLES ----------

if os.path.exists("credentials/.env"):
    load_dotenv("credentials/.env")

ENVIRONMENT = os.getenv("ENVIRONMENT", "DEV")
PROD = ENVIRONMENT == "PROD"
TEST = ENVIRONMENT == "TEST"
DEV = ENVIRONMENT == "DEV"

DB_URL = os.getenv(
    "DB_URL", "postgresql+psycopg2://meddly:meddly@meddly-database:5432/app"
)

SENDGRID_CONFIG = {
    "api_key": os.getenv("SENDGRID_API_KEY"),
    "email": os.getenv("SENDGRID_EMAIL"),
}

FIREBASE_KEY = os.getenv("FIREBASE_KEY")
if os.environ.get("FIREBASE_PROJECT_ID"):
    firebase_admin.initialize_app(
        credential=firebase_admin.credentials.Certificate(
            {
                "type": "service_account",
                "project_id": os.environ.get("FIREBASE_PROJECT_ID"),
                "private_key_id": os.environ.get("PRIVATE_KEY_ID"),
                "private_key": os.environ.get("FIREBASE_PRIVATE_KEY").replace(
                    "\\n", "\n"
                ),
                "client_email": os.environ.get("FIREBASE_CLIENT_EMAIL"),
                "client_id": os.environ.get("CLIENT_ID"),
                "auth_uri": os.environ.get("AUTH_URI"),
                "token_uri": os.environ.get("TOKEN_URI"),
                "auth_provider_x509_cert_url": os.environ.get(
                    "AUTH_PROVIDER_X509_CERT_URL"
                ),
                "client_x509_cert_url": os.environ.get("CLIENT_X509_CERT_URL"),
            }
        )
    )

TWILIO_NUMBER = os.getenv("TWILIO_NUMBER")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
WhatsappClient = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


IMAGES_FOLDER = os.getenv("IMAGES_FOLDER", "store/images")
if not os.path.exists(IMAGES_FOLDER):
    os.makedirs(IMAGES_FOLDER)

# ---------- METADATA ----------
title = "Meddly"
version = 0.91
description = f"""
# Welcome to MeddlyApi!
![Environment](https://badgen.net/static/Environment/{ENVIRONMENT}/blue)

Welcome to the **Meddly project API**! This API serves as the backbone for our mobile application designed to assist individuals facing health challenges. It was meticulously crafted as the culmination of the Software Engineering career at UTN FRC.

Our dedicated team of talented individuals brought this vision to life:

- **Sofía Florencia Cibello**: A proficient _Frontend Developer_ and _UX/UI Designer_.
- **Ignacio Pieve Roiger**: A skilled _Team Leader_ and _Backend Developer_.
- **Lorenzo Sala**: An accomplished _Frontend Developer_.
- **Leila Spini**: A meticulous _Analyst_.

Together, we strived to create a seamless experience for our users, ensuring that Meddly becomes a reliable companion on their health journeys.
"""
contact_email = "ignacio.pieve@gmail.com"

metadata = {
    "title": title,
    "version": version,
    "contact": {
        "name": f"{title} Team",
        "email": contact_email,
    },
    "description": description,
    "docs_url": "/",
}
