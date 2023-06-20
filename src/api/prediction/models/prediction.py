from sqlalchemy import JSON, Boolean, Column, String
from sqlalchemy.sql import expression

from models import CRUD


class Prediction(CRUD):
    __abstract__ = True

    prediction = Column(JSON, nullable=False)
    verified = Column(Boolean, server_default=expression.false(), nullable=False)
    real_disease = Column(String, nullable=True)
