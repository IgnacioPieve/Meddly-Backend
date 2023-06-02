import requests
from firebase_admin import firestore, messaging
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from api.notification.exceptions import ERROR502
from config import SENDGRID_CONFIG, WHATSAPP_API_KEY
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

    def __str__(self):
        return f"{self.notification_preference}"

    def validate(self):
        if self.notification_preference not in self.OPTIONS:
            raise ERROR502

    def send_notification(self, message):
        raise Exception("NotImplementedException")


class WhatsappNotification(NotificationPreference):
    __mapper_args__ = {"polymorphic_identity": NotificationPreference.WHATSAPP}

    def send_notification(self, message):
        message_data = [{"type": "text", "text": message.whatsapp()["message"]}]
        headers = {
            "Authorization": f"Bearer {WHATSAPP_API_KEY}",
            "Content-Type": "application/json",
        }
        body = {
            "messaging_product": "whatsapp",
            "to": self.user.phone,
            "type": "template",
            "template": {
                "name": "generic_message",
                "language": {"code": "es"},
                "components": [{"type": "body", "parameters": message_data}],
            },
        }
        response = requests.post(
            "https://graph.facebook.com/v15.0/100370432826961/messages",
            headers=headers,
            json=body,
        )
        print(
            f"Message Sent via Whatsapp to {self.user.phone}. Response: {response.text}"
        )


class EmailNotification(NotificationPreference):
    __mapper_args__ = {"polymorphic_identity": NotificationPreference.EMAIL}

    def send_notification(self, message):
        message_constructor = Mail(
            from_email=SENDGRID_CONFIG["email"],
            to_emails=self.user.email,
        )
        message_constructor.template_id = "d-5e634cd5cd6548b4b440f188c1d2a40a"
        message_constructor.dynamic_template_data = {
            "hi_message": f"Hola, {self.user.name}"
            if hasattr(self.user, "name")
            else "Hola!",
            "message": message.email()["message"],
            "subject": message.email()["subject"],
        }
        sg = SendGridAPIClient(SENDGRID_CONFIG["api_key"])
        response = sg.send(message_constructor)
        print(
            f"Email Sent via Email (SendGrid) to {self.user.email}. Response: {response.__dict__}"
        )


class PushNotification(NotificationPreference):
    __mapper_args__ = {"polymorphic_identity": NotificationPreference.PUSH}

    def send_notification(self, message):
        db = firestore.client()
        doc_ref = db.collection("user").document(self.user_id)
        doc = doc_ref.get()
        if doc.exists:
            device = doc.to_dict().get("device", None)
            if device:
                message = messaging.Message(
                    notification=messaging.Notification(
                        title=message.push()["title"],
                        body=message.push()["message"],
                    ),
                    token=device,
                )
                response = messaging.send(message)
                print(f"Message Sent via Push to {self.user_id}. Response {response}")
            else:
                print(f"No device token found for {self.user_id} in Firestore.")
        else:
            print(f"No user found for {self.user_id} in Firestore.")
