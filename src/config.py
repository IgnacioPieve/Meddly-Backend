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

FIREBASE_JSON_PATH = "credentials/firebase.json"
FIREBASE_KEY = os.getenv("FIREBASE_KEY")
if os.path.exists(FIREBASE_JSON_PATH):
    firebase_admin.initialize_app(
        firebase_admin.credentials.Certificate(FIREBASE_JSON_PATH)
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
