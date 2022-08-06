import json
import os


# ---------- UTIL FUNCTIONS ----------
def env_variable_to_dict(env_variable):
    try:
        return json.loads(env_variable)
    except json.JSONDecodeError:
        env_variable = env_variable.split(",")
        env_variable[0] = env_variable[0].replace("{", "")
        env_variable[-1] = env_variable[-1].replace("}", "")
        new_dict = {}

        for key_value in env_variable:
            key_value = key_value.split(":", 1)
            new_dict[key_value[0].strip()] = key_value[1].strip()

        return new_dict


# ---------- ENV VARIABLES ----------
# ENV_NAME is the name of the environment. It can be "local-dev", "dev" or "prod"
env_name = os.getenv("ENV_NAME")
db_url = os.getenv("DB_URL")

# ---------- METADATA ----------
title = "Meddly"
version = 0.1
description = f"""
# Welcome to MeddlyApi!
![version](https://img.shields.io/badge/version-{version}-blue)  ![version](https://img.shields.io/badge/enviroment-{env_name.replace("-", "_")}-orange)

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
}
