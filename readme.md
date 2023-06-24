# Meddly ❤️‍🩹
[![Push image to DockerHub](https://github.com/Meddly-Health/Backend/actions/workflows/BuildAndPushDockerImage.yml/badge.svg)](https://github.com/Meddly-Health/Backend/actions/workflows/BuildAndPushDockerImage.yml)
[![Tests](https://github.com/Meddly-Health/Backend/actions/workflows/Tests.yaml/badge.svg)](https://github.com/Meddly-Health/Backend/actions/workflows/Tests.yaml)
> Meddly is a medical application that uses artificial intelligence to generate self-diagnosis based on symptoms.

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

You can see the 
