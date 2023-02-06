import os

# ---------- CONFIG VARIABLES ----------

db_name = os.getenv("DB_NAME", "meddly-database")
DB_URL = f"postgresql+psycopg2://meddly:meddly@{db_name}:5432/app"

SENDGRID_CONFIG = {
    "api_key": "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",
    "email": "meddly.it@gmail.com",
}

FIREBASE_JSON = {
    "type": "service_account",
    "project_id": "meddly-da2c2",
    "private_key_id": "e8c285c6d99afc292d70a5e526fc15112743d65a",
    "private_key": "-----BEGIN PRIVATE KEY-----\n"
    "MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC9y6IZvQp8nXe0\n"
    "ewNjlveMCa2AQswlFqHdqAgdZY/4z59edUWv7WQXjMTbKkYiEeAbG5qx8OXCSPXk\n"
    "Os8zgozlY2mQKdL5Kk/rRZueJ2TqiJp1hPbclKQrQY8J8PqrMGJlkNWPHSqav8cW\n"
    "iVtVnZ4agBLtVI0Cd6my1TS24Stn3zvyh0YoZ4J9/l2qY06IFXaMS6LOjk+1Ddy6\n"
    "X3DowUHjrqKMQWbRByo72JTmXu2Oc8x1Jdjy37dzjVS9XlNREnFWxnDLdjJBZNtN\n"
    "5Yms7OKduGYMqoYB64zvxNA9ZFHGRoFFfaFSbs+zgd2LvbmUpYW9gLvfom87Zz0R\n"
    "VYXVxCpPAgMBAAECggEAFPT5wrbNhCINGDgnESWX0vY0mr+FdCjyGZwWvUw8IACo\n"
    "+9CeL8VaMoGAMSUTVmq74LJlG/XaIOBWimt1+p2VOjUGcH01xv6FkZh/jPCTo5QO\n"
    "3iAe9A9Tq1UTWskpnKJ8kvNxqVpSnIDFlnb3R1ZeoVV4AY2+/kFBUzZYmkL1vIPI\n"
    "YCFyU7HrYmftUz4kbDFALfGrZA9fp3pY1Dk6V+qAnzV5EUwrZ1vDt8eqoIKkyjtJ\n"
    "m8YdMqO7B1euBHl5Y1lQ9b2CNgUFg5NCPnsv5dbsF57ZYySKCOcZQQfVLmxpswOQ\n"
    "Ry/bzXwVRp1s0ZWYqR9OJ+58xX58lPjtpD7K1FtG1QKBgQDyZ7xVTxSg6WFpoA56\n"
    "gmEy0Ol6JCEN3haCF4sv9Y7bdhvjTjadS7/1q/Y3kQv8y3PhFKsqdMwhEWVVUiUd\n"
    "vXaEF1f5ti/Y5QRYTngMUboFuJxcJlmu5Xo7VWqtW9KKuIyRO3DgVP3r0ayIzskg\n"
    "020KDC19aiPshjzms19PmGew0wKBgQDIcJFL+Rm+6wIslU7YAgld2bTJLVzMtty9\n"
    "gpTpBG44TsHXN8WsMVeU8Wcig5qsPg2ZFvEfR9RhwjsNgsRCp4THn4g4hO59tNxn\n"
    "1okEQzPI+gTZarbAvNn0wOQzvxwTl7g6sSB5+lBw4n+U1ugrxUW9Shwn8VHK11sr\n"
    "ksfiUnETFQKBgHaX1+Uotl/vLhBeFRdMuD8DRGbUTDObpwloeVkyWvz1sLkpZ8DW\n"
    "8YhA5EnVNbcs1nmVAhTYZZH8D8aJVM1TByuivBDYWFpV2SVW5paoWUk5Q4412QSf\n"
    "Eoj6xiEgXkYt+d+H5DZsfnoj77RS7sWXiq4yvQKxrfemyR7ZPNUVLA2vAoGAVCDD\n"
    "K0MTZkmXMQU+AXXhXo3IzoOGprm9rqEHRUJBzMppm55iDmLrYq1r31WjbtXguTei\n"
    "3sE0SA/Q31vaaiuLlInGEArjWsm1lLO78JkQPDOMI4Eh0YWyaYMohPuamjKc9a1w\n"
    "dyHz711xtRP6gJydJ9TaOn2UGfIH5yMFWF3H7f0CgYEAhj9sQc/7MLguGV5+/wba\n"
    "dNF1zl5so5D4dUEIsbTG8zdehZQRxOrhakcIJStlB6aY4disJ4lSJgdL7ak9z2lr\n"
    "OIJV7LKyxKJUjZOWvLC7mM1tliKprqjuz6AMgWVnyNHjVYrO+LpnwAW6STj/RodZ\n"
    "rlwEpfOrVfZMsrOW2qSN/V8=\n"
    "-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-8s7sw@meddly-da2c2.iam.gserviceaccount.com",
    "client_id": "106963874780694461433",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/"
    "firebase-adminsdk-8s7sw%40meddly-da2c2.iam.gserviceaccount.com",
    "key": "AIzaSyDdCUkmev0t2iy3oTJw60w5Z-TCY36IR48",
}

WHATSAPP_API_KEY = (
    "EAAIZAuL7Po9kBANjsVcKJIVwR9V6WTuwWyaMpW325sVotcnZCCzPvO2AP0SLzV"
    "FjZArsFjWFRpZAZC8EA8I29cOUcZC1h6C1EJjULlEGTwr9GZCuefgZBRbMJTvdt"
    "jjZBk41EdUt3rDfSvHKjFN4lHeZBadsnKAswRBV79mosZBaXBZCfOnc6Rii2ZAr"
    "DwacZB4yvKjdIY9Kke3r5darTzqaDhp1Na"
)

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
