# Meddly ❤️‍🩹
[![Push image to DockerHub](https://github.com/Meddly-Health/Backend/actions/workflows/BuildAndPushDockerImage.yml/badge.svg)](https://github.com/Meddly-Health/Backend/actions/workflows/BuildAndPushDockerImage.yml)
[![Tests](https://github.com/Meddly-Health/Backend/actions/workflows/Tests.yaml/badge.svg)](https://github.com/Meddly-Health/Backend/actions/workflows/Tests.yaml)
> Welcome to the **Meddly project API**! This API serves as the backbone for our mobile application designed to assist individuals facing health challenges. It was meticulously crafted as the culmination of the Software Engineering career at UTN FRC.

Our dedicated team of talented individuals brought this vision to life:

- **Sofía Florencia Cibello**: A proficient _Frontend Developer_ and _UX/UI Designer_.
- **Ignacio Pieve Roiger**: A skilled _Team Leader_ and _Backend Developer_.
- **Lorenzo Sala**: An accomplished _Frontend & backend Developer_.


Together, we strived to create a seamless experience for our users, ensuring that Meddly becomes a reliable companion on their health journeys.

The application is built using Python, FastApi, and Docker.

## Requirements
- Docker ([see installation guide](https://docs.docker.com/engine/install/ubuntu/))
- git

## Installation
1. Clone the repository from GitHub.
    ```
    git clone git@github.com:Meddly-Health/Backend.git meddly-backend
    ```

2. Navigate to the repository folder.
    ```
    cd meddly-backend
    ```
   
3. Run the application.
    ```
    docker compose up
    ```
    > You must have all the auth files on the src/credentials folder. For more info, see src/credentials/readme.md


## Usage
The application runs on http://localhost:11001/

By default, you can access the swagger documentation on the root path.

