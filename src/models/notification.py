import requests
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from config import SENDGRID_CONFIG, WHATSAPP_API_KEY, translations
from models.utils import CRUD


class NotificationPreference(CRUD):
    __tablename__ = "notification_preference"
    user_id = Column(String(255), ForeignKey("user.id"), primary_key=True, index=True)
    user = relationship(
        "User", backref="notification_preferences_list", foreign_keys=[user_id]
    )
    notification_preference = Column(String(255), primary_key=True, index=True)
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
        raise Exception("NotImplementedException")


class WhatsappNotification(NotificationPreference):
    __mapper_args__ = {"polymorphic_identity": NotificationPreference.WHATSAPP}

    def send_notification(self, message):
        headers = {
            'Authorization': f'Bearer {WHATSAPP_API_KEY}',
            'Content-Type': 'application/json'
        }
        body = {
            'messaging_product': 'whatsapp',
            'to': self.user.phone,
            'type': 'template',
            'template': {
                'name': message.whatsapp()['template_id'],
                'language': {'code': 'en'},
                "components": [
                    {
                        "type": "body",
                        "parameters": message.whatsapp()['template_data']
                    }
                ]
            }
        }
        requests.post('https://graph.facebook.com/v13.0/100370432826961/messages', headers=headers, json=body)


class EmailNotification(NotificationPreference):
    __mapper_args__ = {"polymorphic_identity": NotificationPreference.EMAIL}

    def send_notification(self, message):
        message_constructor = Mail(
            from_email=SENDGRID_CONFIG["email"], to_emails=self.user.email
        )
        message_constructor.dynamic_template_data = message.email()["template_data"]
        message_constructor.template_id = message.email()["template_id"]
        sg = SendGridAPIClient(SENDGRID_CONFIG["api_key"])
        sg.send(message_constructor)


class SMSNotification(NotificationPreference):
    __mapper_args__ = {"polymorphic_identity": NotificationPreference.SMS}


class PushNotification(NotificationPreference):
    __mapper_args__ = {"polymorphic_identity": NotificationPreference.PUSH}
