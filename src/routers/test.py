import requests
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/test", tags=["Test"])


@router.get("/status")
def get_status():
    """Get status of messaging server."""
    return {"status": "running"}
