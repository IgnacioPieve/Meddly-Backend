import os

from fastapi import HTTPException
from starlette import status

# ---------- CONFIG VARIABLES ----------

DB_URL = "postgresql+psycopg2://meddly:meddly@meddly-database:5432/app"

SENDGRID_CONFIG = {
    "api_key": "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",
    "email": "meddly.health@gmail.com",
}

FIREBASE_JSON = {
    "type": "service_account",
    "project_id": "meddly-da2c2",
    "private_key_id": "e8c285c6d99afc292d70a5e526fc15112743d65a",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC9y6IZvQp8nXe0\newNjlveMCa2AQswlFqHdqAgdZY/4z59edUWv7WQXjMTbKkYiEeAbG5qx8OXCSPXk\nOs8zgozlY2mQKdL5Kk/rRZueJ2TqiJp1hPbclKQrQY8J8PqrMGJlkNWPHSqav8cW\niVtVnZ4agBLtVI0Cd6my1TS24Stn3zvyh0YoZ4J9/l2qY06IFXaMS6LOjk+1Ddy6\nX3DowUHjrqKMQWbRByo72JTmXu2Oc8x1Jdjy37dzjVS9XlNREnFWxnDLdjJBZNtN\n5Yms7OKduGYMqoYB64zvxNA9ZFHGRoFFfaFSbs+zgd2LvbmUpYW9gLvfom87Zz0R\nVYXVxCpPAgMBAAECggEAFPT5wrbNhCINGDgnESWX0vY0mr+FdCjyGZwWvUw8IACo\n+9CeL8VaMoGAMSUTVmq74LJlG/XaIOBWimt1+p2VOjUGcH01xv6FkZh/jPCTo5QO\n3iAe9A9Tq1UTWskpnKJ8kvNxqVpSnIDFlnb3R1ZeoVV4AY2+/kFBUzZYmkL1vIPI\nYCFyU7HrYmftUz4kbDFALfGrZA9fp3pY1Dk6V+qAnzV5EUwrZ1vDt8eqoIKkyjtJ\nm8YdMqO7B1euBHl5Y1lQ9b2CNgUFg5NCPnsv5dbsF57ZYySKCOcZQQfVLmxpswOQ\nRy/bzXwVRp1s0ZWYqR9OJ+58xX58lPjtpD7K1FtG1QKBgQDyZ7xVTxSg6WFpoA56\ngmEy0Ol6JCEN3haCF4sv9Y7bdhvjTjadS7/1q/Y3kQv8y3PhFKsqdMwhEWVVUiUd\nvXaEF1f5ti/Y5QRYTngMUboFuJxcJlmu5Xo7VWqtW9KKuIyRO3DgVP3r0ayIzskg\n020KDC19aiPshjzms19PmGew0wKBgQDIcJFL+Rm+6wIslU7YAgld2bTJLVzMtty9\ngpTpBG44TsHXN8WsMVeU8Wcig5qsPg2ZFvEfR9RhwjsNgsRCp4THn4g4hO59tNxn\n1okEQzPI+gTZarbAvNn0wOQzvxwTl7g6sSB5+lBw4n+U1ugrxUW9Shwn8VHK11sr\nksfiUnETFQKBgHaX1+Uotl/vLhBeFRdMuD8DRGbUTDObpwloeVkyWvz1sLkpZ8DW\n8YhA5EnVNbcs1nmVAhTYZZH8D8aJVM1TByuivBDYWFpV2SVW5paoWUk5Q4412QSf\nEoj6xiEgXkYt+d+H5DZsfnoj77RS7sWXiq4yvQKxrfemyR7ZPNUVLA2vAoGAVCDD\nK0MTZkmXMQU+AXXhXo3IzoOGprm9rqEHRUJBzMppm55iDmLrYq1r31WjbtXguTei\n3sE0SA/Q31vaaiuLlInGEArjWsm1lLO78JkQPDOMI4Eh0YWyaYMohPuamjKc9a1w\ndyHz711xtRP6gJydJ9TaOn2UGfIH5yMFWF3H7f0CgYEAhj9sQc/7MLguGV5+/wba\ndNF1zl5so5D4dUEIsbTG8zdehZQRxOrhakcIJStlB6aY4disJ4lSJgdL7ak9z2lr\nOIJV7LKyxKJUjZOWvLC7mM1tliKprqjuz6AMgWVnyNHjVYrO+LpnwAW6STj/RodZ\nrlwEpfOrVfZMsrOW2qSN/V8=\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-8s7sw@meddly-da2c2.iam.gserviceaccount.com",
    "client_id": "106963874780694461433",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-8s7sw%40meddly-da2c2.iam.gserviceaccount.com",
    "key": "AIzaSyDdCUkmev0t2iy3oTJw60w5Z-TCY36IR48"
}

WHATSAPP_API_KEY = "EAAIZAuL7Po9kBABNLP30eVWiW8xQup6JJvrshPMXfZC8dHPCORXm5qhJGKzrCjFV4GmcIK9JCEyglmAispSdAz4JJYmaiXrZA85aQI5nlZAWerlCH4RDpbATfuhy4tDolwMuayYQLwRuJABQamIVrWZAC1UraFpgQXMiWqYg9NwZDZD"

# ---------- METADATA ----------
title = "Meddly"
version = 0.1
description = f"""
# Welcome to MeddlyApi!
![version](https://img.shields.io/badge/version-{version}-blue)

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
        "treatments": {
            "treatment_not_found": HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "en": "Treatment not found",
                    "es": "Tratamiento no encontrado",
                },
            ),
            "treatment_expired": HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "en": "Treatment expired",
                    "es": "Tratamiento expirado",
                },
            ),
            "consumption_before_treatment_start": HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "en": "Consumption date is before the start of the treatment",
                    "es": "Fecha de consumo antes de la fecha de inicio del tratamiento",
                },
            ),
            "incorrect_time": HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "en": "Consumption date is not on the correct time",
                    "es": "La fecha de consumo no está en el horario correcto",
                },
            ),
            "incorrect_date": HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "en": "Consumption date is not on the correct date",
                    "es": "La fecha de consumo no está en la fecha correcta",
                },
            ),
            "consumption_already_exists": HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "en": "The consumption has already been registered",
                    "es": "El consumo ya ha sido registrado",
                },
            ),
        },
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
    }
}
