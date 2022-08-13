import json
import os
from fastapi import HTTPException
from starlette import status

# ---------- CONFIG VARIABLES ----------
ENV_NAME = os.getenv("ENV_NAME")

if ENV_NAME == "prod":
    DB_URL = "postgresql://ufgbchph:cTqNG9causgSbi-eEXhsDt32FdsWwY4B@kesavan.db.elephantsql.com/ufgbchph"
elif ENV_NAME == "dev":
    DB_URL = "postgres://zwvcehpe:1W85KcjdhU7AAs8sbXWlKxbIXlen97dk@kesavan.db.elephantsql.com/zwvcehpe"
else:
    # Environ variables for local development
    DB_URL = "sqlite:///database.db"
    ENV_NAME = "local-dev"

SENDGRID_CONFIG = {
    "api_key": "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",
    "email": "meddly.health@gmail.com",
}

FIREBASE_JSON = {
    "type": "service_account",
    "project_id": "meddly-fbcf7",
    "private_key_id": "e944fe1256c597a40b1385510ae056ecde133d62",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDu2eqvePIJTori\nM5Z0jW6aWffEUazUS5Sosupr6dJmG+Bs2M+6iaY4a/xls0LxXV/8cVoB7ZIo35Km\nkgPfgqnzTRVhp/kNUUU23Q213XF91aB75mi4tmlJuYuOhQtlXhsGWY/A6CLW3CSB\nNKtNbYwQmgf5308S9QOYxowAWGR/lV45pVcld09VZ7MiylcGZ4ofKtOQP93VEVSJ\nJODK9dBww6/iRZvlJPl1/wiRNeZrjmhS2QQaP8hRSSgDAkp3ucwWvghL8QMMA3ou\n8abdhMsjUoQ5zpegzl5TJ/4bRzhzFy+02P223sh0ALqgdDzJs8FPb8B69zm8DHLq\nqCzW3q9zAgMBAAECggEAcrtBpK1Tkg3k37hJDs57MPCDeA2Fl+qAS7K5sUF9e+fr\nG03gJqoFKrgQYufDgb5JI7FtO1zbZv/R6WpdKumQalr+KM0vcGq39R0k/1WSNRA/\nSRTJ++Q/WhcjBsA406XrFFdEGrVHOu8/J8Ndf9FdxQHAUBIo4SHJawMAcBAFolR3\ndNTZ/DKj4uCQvCxeNBOySEijX7QqAelwvFr+x1QPoHmlWMSLdahGl6CMC268PP7N\nDOYdY42elxLBi9VL88zgzs3ZAjcLXsYd+fLDclXGZucqji/AbGcsD4PVKQIRZEGx\nDmML1Wq4i1N+mnlxxw1ZhlOGTMhoRFvdvDFG7Eb8ZQKBgQD8VqP0j4tsa2OC9HMa\nJKO9SlBtUGSsA36PAwNxpimt/Ti9061mUoOWIQbKcrlLs3lq5Wq4LUHh+LlNgVyj\nNSKDzdOhTQ5MYa1ArQCZFaoeODMzqNOXRLITeMXqjcCeu/yjo2NvA31bQxD5fhIO\neSO99x6xnoWEZgTsPF56ct0nLwKBgQDyUSzs6COhdI7RYEIh1dLj5ekiIw5ux5qY\n8iV1Wp3Md5ccy6ggN2lihP4AtuHul0Cx8tGp10/P/EK9nutoUUhmoc0oNCl+cja7\nOqA9GqowwNbe96DhqQGQECpCxtnAS4MpuytmVnWp0rbvxILch/DIkLlWhJirHr0d\nATfVe+Lq/QKBgDpCWqpNNfh7Nsd2XtjLWs6KSNVkOUoJqH+mR3ZG0dqs2xvgsmks\nZdsUlvfI0wUqU78dZq1NLafZgBbn5hZ8XxKlQ9Y67zEtYA3No5S0jslZWmDz+p4z\nKxYZzUAhKDa92k+BmqR33spiSpn/xHV4/IqQcpK5scPmtf5A1eNZf7vbAoGAAKxF\nCatjXfFq7B3uURW87jEXQqcCRUB8p2wUuoyz33t9ifDu2JgOzN09r1bSrczxuwzH\nlEcqy5MRxGEKmlGPd+l/Hlt2ugkrKb3x7/mA+32tmxTo93d2r6W72E+hDy2mgZkp\nd7FJxlz1cRkEnAQsoQH14c2gdukw8UGtnAQqDykCgYEA87dbjvi1jhQw2sTkAFbL\nvxzckKog6SyAzOiUjtrk/OcnFFeYDXFfJgOmY2wkx20Q7+TtqNl7QsTcHCBNJJIo\n7FQBnCoiY1pzYXT5Ez7NVwjIOjuICUrpT9SJExSXvH7+nhQhm/PNSAWg1Bvgn/Jh\n6BpHv3DqES4kRcPzQPWBF4E=\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-g73bu@meddly-fbcf7.iam.gserviceaccount.com",
    "client_id": "116799592510386491122",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-g73bu%40meddly-fbcf7.iam.gserviceaccount.com",
    "key": "AIzaSyBWeIdwEe2rS3fMvrbayV0gQeWY9zpnAxo",
}

# ---------- METADATA ----------
title = "Meddly"
version = 0.1
description = f"""
# Welcome to MeddlyApi!
![version](https://img.shields.io/badge/version-{version}-blue)  ![version](https://img.shields.io/badge/enviroment-{ENV_NAME.replace("-", "_")}-orange)

Created by:
- Cibello, Sofía Florencia
- Pieve Roiger, Ignacio
- Sala, Lorenzo
- Spini, Leila
"""

metadata = {
    "title": title,
    "version": version,
    "contact": {
        "name": f"{title} Team",
        "email": "ignacio.pieve@gmail.com",
    },
    "description": description,
    "docs_url": "/",
}

# ----- TRANSLATIONS -----
translations = {
    "errors": {
        "notifications": {
            "not_valid": HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "en": "The selected preference is not valid",
                    "es": "La preferencia seleccionada no es válida",
                },
            ),
            "notification_preference_already_exists": HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "en": "The selected preference already exists",
                    "es": "La preferencia seleccionada ya existe",
                },
            ),
            "notification_preference_not_found": HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "en": "The selected preference does not exist",
                    "es": "La preferencia seleccionada no existe",
                },
            ),
        },
        "supervisors": {
            "already_supervised": HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "en": "You are already being supervised by this user",
                    "es": "Ya estás siendo supervisado por este usuario",
                },
            ),
            "code_not_valid": HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "en": "The invitation code is not valid",
                    "es": "El código de invitación no es válido",
                },
            ),
            "supervised_not_found": HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "en": "User not found (maybe you are not being supervised by this user)",
                    "es": "Usuario no encontrado (puede que no estés siendo supervisado por este usuario)",
                },
            ),
            "supervisor_not_found": HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "en": "User not found (maybe you are not supervising this user)",
                    "es": "Usuario no encontrado (puede que no estés supervisando este usuario)",
                },
            ),
        },
    }
}
