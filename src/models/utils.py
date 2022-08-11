import datetime
import random
import string

from sqlalchemy import Column, DateTime
from sqlalchemy.orm import Session

from database import SessionLocal, Base


class CRUD(Base):
    __abstract__ = True
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    def __init__(self, db: Session, *criterion, **kwargs):
        self.db = db
        self.criterion = criterion
        super().__init__(**kwargs)

    def validate(self):
        pass

    def get(self):
        object_class = self.__class__
        result: object_class = (
            self.db.query(object_class).filter(*self.criterion).first()
        )
        if result:
            result.db = self.db
        return result

    def get_all(self):
        object_class = self.__class__
        result = []
        for item in self.db.query(object_class).filter(*self.criterion).all():
            item: object_class
            item.db = self.db
            result.append(item)
        return result

    def create(self):
        self.validate()
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        self.db.add(self)
        self.db.commit()
        self.db.refresh(self)
        return self

    def save(self):
        self.validate()
        self.updated_at = datetime.datetime.now()
        self.db.commit()
        self.db.refresh(self)
        return self

    def destroy(self):
        self.db.delete(self)
        self.db.commit()
        return True


def generate_code():
    from models.user import User

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
            code_is_repeated = (
                session.query(User).filter(User.invitation == code_to_check).first()
                is not None
            )
            return code_is_repeated

        code = generate()
        while is_repeated(code):
            code = generate()
        return code
