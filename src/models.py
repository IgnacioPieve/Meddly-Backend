from fastapi import HTTPException
from sqlalchemy import Column, DateTime, Integer, func
from starlette import status

from database import Base


class CRUD(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.current_timestamp(),
    )


def raise_errorcode(status_code):
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail={"code": status_code}
    )
