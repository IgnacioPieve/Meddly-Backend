import uvicorn
import os

# Environ variables for local development.
os.environ['DB_URL'] = 'sqlite:///database.db'
os.environ['ENV_NAME'] = 'local-dev'

# Run server
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
