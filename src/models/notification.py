from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from config import translations
from models.utils import CRUD


class NotificationPreference(CRUD):
    __tablename__ = "notification_preference"
    user_id = Column(String, ForeignKey("user.id"), primary_key=True, index=True)
    user = relationship(
        "User", backref="notification_preferences_list", foreign_keys=[user_id]
    )
    notification_preference = Column(String, primary_key=True, index=True)
    __mapper_args__ = {"polymorphic_on": notification_preference}

    EMAIL = "email"
    SMS = "sms"
    WHATSAPP = "whatsapp"
    PUSH = "push"
    OPTIONS = [EMAIL, SMS, WHATSAPP, PUSH]

    def __str__(self):
        return f"{self.notification_preference}"

    def validate(self):
        if self.notification_preference not in self.OPTIONS:
            raise translations["errors"]["notifications"]["not_valid"]

    def send_notification(self, message):
        pass


class WhatsappNotification(NotificationPreference):
    __mapper_args__ = {"polymorphic_identity": NotificationPreference.WHATSAPP}


class EmailNotification(NotificationPreference):
    __mapper_args__ = {"polymorphic_identity": NotificationPreference.EMAIL}


class SMSNotification(NotificationPreference):
    __mapper_args__ = {"polymorphic_identity": NotificationPreference.SMS}


class PushNotification(NotificationPreference):
    __mapper_args__ = {"polymorphic_identity": NotificationPreference.PUSH}
