import random
import string

from sqlalchemy import Column, String, DateTime, Float
from database import Base, SessionLocal
from models.utils import CRUD


class User(Base, CRUD):
    __tablename__ = "user"

    id = Column(String, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    invitation = Column(String, nullable=False, index=True)

    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    height = Column(Float, nullable=True)
    weight = Column(Float, nullable=True)
    sex = Column(String, nullable=True)
    birth = Column(DateTime, nullable=True)
    avatar = Column(String, nullable=True)

    def __init__(self, **kwargs):
        super().__init__(invitation=self.generate_code(), **kwargs)

    @staticmethod
    def generate_code():
        """
        Generates a 10-character code and checks that it does not exist in the database
        """
        with SessionLocal.begin() as session:
            def generate():
                generated_code = []
                for k in [3, 4, 3]:
                    generated_code.append(
                        "".join(random.choices(string.ascii_uppercase, k=k))
                    )
                generated_code = "-".join(generated_code).upper()
                return generated_code

            def is_repeated(code_to_check):
                code_is_repeated = session.query(User).filter(User.invitation == code_to_check).first() is not None
                return code_is_repeated

            code = generate()
            while is_repeated(code):
                code = generate()
            return code
