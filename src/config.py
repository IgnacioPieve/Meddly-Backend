import os

import firebase_admin
from dotenv import load_dotenv

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

WHATSAPP_API_KEY = os.getenv("WHATSAPP_API_KEY")
WA_NUMBER_ID = os.getenv("WA_NUMBER_ID")

IMAGES_FOLDER = os.getenv("IMAGES_FOLDER", "store/images")
if not os.path.exists(IMAGES_FOLDER):
    os.makedirs(IMAGES_FOLDER)

# ---------- METADATA ----------
title = "Meddly"
version = 0.9
description = f"""
# Welcome to MeddlyApi!
![Environment](https://badgen.net/static/Environment/{ENVIRONMENT}/blue)


This is the API for the Meddly project, a mobile application that aims to help people with health issues.
The project was developed as part of the final project for the UTN FRC's Software Engineering career.


Created by:
- Cibello, Sofía Florencia (Frontend Developer and UX/UI Designer)
- Pieve Roiger, Ignacio (Team Leader and Backend Developer)
- Sala, Lorenzo (Frontend Developer)
- Spini, Leila (Analyst)
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
