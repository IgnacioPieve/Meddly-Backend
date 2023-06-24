from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from models import CRUD


class NotificationPreference(CRUD):
    __tablename__ = "notification_preference"

    id = None
    user_id = Column(String(255), ForeignKey("user.id"), primary_key=True, index=True)
    user = relationship(
        "User", backref="notification_preferences_list", foreign_keys=[user_id]
    )
    notification_preference = Column(String(255), primary_key=True, index=True)
    __mapper_args__ = {"polymorphic_on": notification_preference}

    EMAIL = "email"
    WHATSAPP = "whatsapp"
    PUSH = "push"
    OPTIONS = [EMAIL, WHATSAPP, PUSH]


class WhatsappNotification(NotificationPreference):
    __mapper_args__ = {"polymorphic_identity": NotificationPreference.WHATSAPP}


class EmailNotification(NotificationPreference):
    __mapper_args__ = {"polymorphic_identity": NotificationPreference.EMAIL}


class PushNotification(NotificationPreference):
    __mapper_args__ = {"polymorphic_identity": NotificationPreference.PUSH}
