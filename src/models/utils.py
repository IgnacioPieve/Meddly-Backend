import datetime

from sqlalchemy import Column, DateTime


class CRUD:
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    def create(self, db):
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        db.add(self)
        db.commit()
        return db.refresh(self)

    def save(self, db):
        self.updated_at = datetime.datetime.now()
        db.commit()
        return db.refresh(self)

    def destroy(self, db):
        db.delete(self)
        return db.commit()
